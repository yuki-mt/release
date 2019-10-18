from pytz import timezone
from datetime import datetime, timedelta
from typing import Iterator, NamedTuple, Dict


def get_metric_values(client, namespace: str, metric: str,
                      dimension: Dict[str, str],
                      period: int, unit: str,
                      interval_hours: int) -> Iterator[float]:
    now = datetime.now(timezone('UTC'))
    start_at = now - timedelta(hours=interval_hours)
    max_datapoints = 1000
    query = {
        'Id': 'm1',
        'MetricStat': {
            'Metric': {
                'Namespace': namespace,
                'MetricName': metric,
                'Dimensions': [dimension]
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
    if num_total == 0:
        return AnalysisResult(0.0, 0, 0.0)
    return AnalysisResult(above_ratio=num_above_thresholds / num_total,
                          num_total=num_total,
                          average=sum_value / num_total)
