from pytz import timezone
from datetime import datetime, timedelta
from typing import Iterator, Dict


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
