import boto3
from typing import Iterator

from usage import get_metric_values, analyze


def get_ec2_metrics(client, metric: str, instance_id: str,
                    period: int = 300, unit: str = 'Percent',
                    interval_hours: int = 24) -> Iterator[float]:
    return get_metric_values(
        client, 'AWS/EC2', metric,
        {'Name': 'InstanceId', 'Value': instance_id},
        period, unit, interval_hours)


def main():
    instance_id = 'i-xxx'
    metric_name = 'CPUUtilization'
    metric_threshold = 1
    total_threshold = 100
    ratio_threshold = 0.05

    client = boto3.client('cloudwatch')

    values = get_ec2_metrics(client, metric_name, instance_id)
    result = analyze(values, metric_threshold)

    if result.num_total > total_threshold:
        if result.above_ratio < ratio_threshold:
            print(f'{metric_name} is too low. instance-id: {instance_id}. average: {result.average}')
        else:
            print(f'{metric_name} is moderate. instance-id: {instance_id}. average: {result.average}')
    else:
        print(f'number of values is too few to judge. metric-name: {metric_name}. instance-id: {instance_id}')


if __name__ == '__main__':
    main()
