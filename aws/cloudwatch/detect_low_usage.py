import boto3
from pytz import timezone
from datetime import datetime, timedelta
from typing import Iterator, NamedTuple


def get_metric_values(client, metric: str, instance_id: str,
                      period: int = 300, unit='Percent',
                      interval_hours: int = 24) -> Iterator[float]:
    now = datetime.now(timezone('UTC'))
    start_at = now - timedelta(hours=interval_hours)
    max_datapoints = 1000
    query = {
        'Id': 'm1',
        'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/EC2',
                'MetricName': metric,
                'Dimensions': [
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ]
            },
            'Period': period,
            'Stat': 'Average',
            'Unit': unit
        },
        'ReturnData': True
    }
    response = client.get_metric_data(
        MetricDataQueries=[query],
        MaxDatapoints=max_datapoints,
        StartTime=start_at,
        EndTime=now
    )
    for v in response['MetricDataResults'][0]['Values']:
        yield v

    next_token = response.get('NextToken')
    while next_token is not None:
        response = client.get_metric_data(
            MetricDataQueries=[query],
            MaxDatapoints=max_datapoints,
            StartTime=start_at,
            EndTime=now,
            NextToken=next_token
        )
        next_token = response.get('NextToken')
        for v in response['MetricDataResults'][0]['Values']:
            yield v


class AnalysisResult(NamedTuple):
    above_ratio: float
    num_total: int
    average: float


def analyze(values: Iterator[float], threshold: float) -> AnalysisResult:
    num_total = 0
    num_above_thresholds = 0
    sum_value = 0.0

    for v in values:
        num_total += 1
        sum_value += v
        if v > threshold:
            num_above_thresholds += 1
    return AnalysisResult(above_ratio=num_above_thresholds / num_total,
                          num_total=num_total,
                          average=sum_value / num_total)


def main():
    instance_id = 'i-xxx'
    metric_name = 'CPUUtilization'
    metric_threshold = 1
    total_threshold = 100
    ratio_threshold = 0.05

    client = boto3.client('cloudwatch')

    values = get_metric_values(client, metric_name, instance_id)
    result = analyze(values, metric_threshold)
    print(result)

    if result.num_total > total_threshold:
        if result.above_ratio < ratio_threshold:
            print(f'{metric_name} is too low. instance-id: {instance_id}. average: {result.average}')
        else:
            print(f'{metric_name} is moderate. instance-id: {instance_id}. average: {result.average}')
    else:
        print(f'number of values is too few to judge. metric-name: {metric_name}. instance-id: {instance_id}')


if __name__ == '__main__':
    main()
