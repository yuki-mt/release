import boto3
import re
from typing import Iterator, Tuple, NamedTuple, List

from usage import get_metric_values, analyze, AnalysisResult


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


def is_low_usage(result: AnalysisResult,
                 total_threshold: int,
                 ratio_threshold: float) -> bool:
    return result.num_total > total_threshold and result.above_ratio < ratio_threshold


class LowUsageJob(NamedTuple):
    name: str
    gpu_util: float
    gpu_mem_util: float


def get_low_usage_jobs(total_threshold: int,
                       ratio_threshold: float,
                       interval_hours: int) -> List[LowUsageJob]:
    client = boto3.client('cloudwatch')
    low_jobs = []
    for job_name, num_gpu in get_inprogress_jobs():
        metric_threshold = 50 * num_gpu
        gpu_values = get_sg_metrics(client, 'GPUUtilization', job_name,
                                    interval_hours=interval_hours)
        gpu_result = analyze(gpu_values, metric_threshold)
        if is_low_usage(gpu_result, total_threshold, ratio_threshold):
            gpu_mem_values = get_sg_metrics(client, 'GPUMemoryUtilization', job_name,
                                            interval_hours=interval_hours)
            gpu_mem_result = analyze(gpu_mem_values, metric_threshold)
            if is_low_usage(gpu_mem_result, total_threshold, ratio_threshold):
                low_jobs.append(LowUsageJob(job_name, gpu_result.average, gpu_mem_result.average))
    return low_jobs


def main():
    total_threshold = 50
    ratio_threshold = 0.05
    interval_hours = 1

    for job in get_low_usage_jobs(total_threshold, ratio_threshold, interval_hours):
        print('JobName:', job.name)
        print(f'Averaged GPUUtilization in {interval_hours} hours:', job.gpu_util)
        print(f'Averaged GPUMemoryUtilization in {interval_hours} hours:', job.gpu_mem_util)


if __name__ == '__main__':
    main()
