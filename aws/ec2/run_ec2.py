from datetime import date
import random
import subprocess
from time import sleep
from typing import List, NamedTuple
import boto3


def main():
    """CHANGE HERE"""
    info = BasicInfo(
        project_name='p',
        person='...',
        region='oregon',
        deadline='2020/03/31',
        image='ubuntu 16',
        instance_type='t3.xlarge',
        num_instance=1,
        schedule_ptn='...',
        volume_size=1000,
        security_groups=[
            "sg-xxx",
        ],
        role_name='',
        key_name='')
    ssh_public_key_path = ''
    linux_user = '...'
    """/CHANGE HERE"""

    if 'ubuntu' in info.image.lower():
        default_linux_user = 'ubuntu'
    else:
        default_linux_user = 'ec2-user'
    info = modify_info(info)
    client = boto3.client('ec2', region_name=info.region)
    instance_ids = run_instances(client, info)
    print('instance IDs')
    print('\n'.join(instance_ids))
    print('================')
    print('wait for finish creatging...')
    sleep(40)
    attatch_eip(client, instance_ids)
    ips = list_ip(client, instance_ids)

    print('wait for enabling SSH...')
    sleep(20)
    setup_linux(ips, info.region, ssh_public_key_path,
                linux_user, default_linux_user)


class BasicInfo(NamedTuple):
    project_name: str
    person: str
    region: str
    deadline: str
    image: str
    instance_type: str
    num_instance: int
    schedule_ptn: str
    volume_size: int
    security_groups: List[str]
    role_name: str
    key_name: str
    subnet: str = ''


def modify_info(info: BasicInfo) -> BasicInfo:
    region_prefix = info.region[0].lower()
    key_name = info.key_name
    if region_prefix == 'o':
        region = 'us-west-2'
        if not info.key_name:
            key_name = 'Default_key_name'
        subnets = ['subnet-xx',
                   'subnet-xx']
    elif region_prefix == 't':
        region = 'ap-northeast-1'
        if not key_name:
            key_name = 'Default_key_name'
        subnets = ['subnet-xx',
                   'subnet-xx']
    else:
        raise ValueError('invalid region')

    if 'ubuntu' in info.image.lower() and '18' in info.image:
        image_id = 'ami-005bdb005fb00e791'
    elif 'ubuntu' in info.image.lower() and '16' in info.image:
        if info.instance_type == 'p2.xlarge':
            image_id = 'ami-04121e1f9d541d468'
        else:
            image_id = 'ami-0b37e9efc396e4c38'
    elif 'windows' in info.image.lower() and '2016' in info.image:
        image_id = 'ami-09380bd107b455fe7'
    elif 'redhat' in info.image.lower() and '7' in info.image:
        image_id = 'ami-096510cab1b6b2c6d'
    elif info.image.startswith('ami-'):
        image_id = info.image
    else:
        raise ValueError('invalid image')
    if not info.deadline:
        deadline = 'No deadline'
    else:
        deadline = info.deadline
    return info._replace(region=region, deadline=deadline, image=image_id,
                         key_name=key_name, subnet=random.choice(subnets))


def run_instances(client, info: BasicInfo) -> List[str]:
    tags = [
        ('Name', '{}-{}-{}'.format(info.person, info.project_name, date.today().strftime("%Y%m%d"))),
        ('DueDate', info.deadline),
        ('Person', info.person),
        ('Project', info.project_name),
    ]
    if info.schedule_ptn:
        tags.append(('Schedule', info.schedule_ptn))

    response = client.run_instances(
        BlockDeviceMappings=[{
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': info.volume_size,
                'VolumeType': 'gp2',
            },
        }],
        ImageId=info.image,
        InstanceType=info.instance_type,
        KeyName=info.key_name,
        MaxCount=info.num_instance,
        MinCount=info.num_instance,
        IamInstanceProfile={'Name': info.role_name},
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeleteOnTermination': True,
                'DeviceIndex': 0,
                'SubnetId': info.subnet,
                'Groups': info.security_groups,
            },
        ],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': k, 'Value': v} for k, v in tags]
        }],
    )

    return [i['InstanceId'] for i in response['Instances']]


def attatch_eip(client, instance_ids: List[str]):
    for i in instance_ids:
        allocation_id = client.allocate_address(Domain='vpc')['AllocationId']
        client.associate_address(AllocationId=allocation_id, InstanceId=i)


def list_ip(client, instance_ids: List[str]) -> List[str]:
    response = client.describe_instances(InstanceIds=instance_ids)
    public_ips = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            public_ips.append(instance['PublicIpAddress'])
    print('IP addresses are')
    print('\n'.join(public_ips))
    return public_ips


def setup_linux(ips: List[str], region: str, key_path: str,
                username: str, default_username: str):
    with open('../../ansible/user/hosts', 'w') as f:
        f.write('[targets]\n{}'.format('\n'.join(ips)))
    if region == 'us-west-2':
        key_file = '~/.ssh/oregon.pem'
    elif region == 'ap-northeast-1':
        key_file = '~/.ssh/tokyo.pem'
    else:
        raise ValueError('invalid region (in setup_linux)')

    cmd_fmt = ('cd ../../ansible/user && '
               f'ansible-playbook %s -u {default_username} --key-file {key_file}  '
               '-i hosts %s')

    def var_opt(k: str, v: str) -> str:
        return f'-e "{k}=\'{v}\'"'
    key_vars = ''
    if username:
        subprocess.run(cmd_fmt % ('user.yml', var_opt('username', username)), shell=True)
        key_vars = var_opt('username', username)
    else:
        key_vars = var_opt('username', default_username)
    key_vars += ' ' + var_opt('key_path', key_path)
    if username or key_path:
        subprocess.run(cmd_fmt % ('key.yml', key_vars), shell=True)

    print('=========send this message=============')
    for ip in ips:
        n = username or default_username
        print(f'username: {n}\nIP address: {ip}')
    print('=========/send this message=============')


if __name__ == '__main__':
    main()
