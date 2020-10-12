"""
SageMakerのGPU training jobのうち、使用率がthreshold_per_gpu % 以下のJobを列挙する
"""

import boto3
import re
from typing import Iterator, Tuple, NamedTuple, List

from usage import get_metric_values


def get_sg_metrics(client, metric: str, job_name: str,
                   period: int = 60, unit: str = 'Percent',
                   interval_hours: int = 1) -> Iterator[float]:
    return get_metric_values(
        client, '/aws/sagemaker/TrainingJobs', metric,
        {'Name': 'Host', 'Value': f'{job_name}/algo-1'},
        period, unit, interval_hours)


def get_inprogress_jobs() -> Iterator[Tuple[str, int]]:
    search_filter = {'Filters': [{"Name": "TrainingJobStatus",
                                  "Operator": "Equals",
                                  "Value": 'InProgress'}]}
    client = boto3.client('sagemaker')
    response = client.search(Resource='TrainingJob',
                             SearchExpression=search_filter,
                             MaxResults=100)

    for r in response['Results']:
        job = r['TrainingJob']
        gpu_info = re.search(r'ml\.p(\d)\.(\d+)?xlarge',
                             job['ResourceConfig']['InstanceType'])
        if gpu_info is None:
            continue
        # ref: https://aws.amazon.com/jp/sagemaker/pricing/instance-types/
        num_gpu = int(int(gpu_info.group(2)) / (int(gpu_info.group(1)) - 1))

        yield job['TrainingJobName'], num_gpu


def is_low_usage(values: List[float],
                 total_threshold: int,
                 threshold: float) -> Tuple[bool, float]:
    length = len(values)
    avg = sum(values) / length
    return length > total_threshold and avg < threshold, avg


class LowUsageJob(NamedTuple):
    name: str
    gpu_util: float
    gpu_mem_util: float


def get_low_usage_jobs(total_threshold: int,
                       threshold_per_gpu: float,
                       interval_hours: int) -> List[LowUsageJob]:
    client = boto3.client('cloudwatch')
    low_jobs = []
    for job_name, num_gpu in get_inprogress_jobs():
        metric_threshold = threshold_per_gpu * num_gpu
        gpu_values = get_sg_metrics(client, 'GPUUtilization', job_name,
                                    interval_hours=interval_hours)
        is_gpu_low, gpu_avg = is_low_usage(list(gpu_values), total_threshold, metric_threshold)
        if is_gpu_low:
            gpu_mem_values = get_sg_metrics(client, 'GPUMemoryUtilization', job_name,
                                            interval_hours=interval_hours)
            is_mem_low, mem_avg = is_low_usage(list(gpu_mem_values), total_threshold, metric_threshold)
            if is_mem_low:
                low_jobs.append(LowUsageJob(job_name, gpu_avg, mem_avg))
    return low_jobs


def main():
    total_threshold = 50
    interval_hours = 1
    threshold_per_gpu = 10

    for job in get_low_usage_jobs(total_threshold, threshold_per_gpu, interval_hours):
        print('JobName:', job.name)
        print(f'Averaged GPUUtilization in {interval_hours} hours:', job.gpu_util)
        print(f'Averaged GPUMemoryUtilization in {interval_hours} hours:', job.gpu_mem_util)


if __name__ == '__main__':
    main()
