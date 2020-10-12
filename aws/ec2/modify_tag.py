import boto3


region = 'us-west-2'
ip_addresses = """
"""

schedule = 'new_value'

boto3.setup_default_session(region_name=region)
client = boto3.client('ec2')

response = client.describe_instances(
        Filters=[{'Name': 'ip-address',
                  'Values': list(filter(lambda x: x, ip_addresses.split('\n')))}])

instance_ids = []
for re in response['Reservations']:
    for i in re['Instances']:
        instance_ids.append(i['InstanceId'])

client.create_tags(
    Resources=instance_ids,
    Tags=[{'Key': 'Schedule', 'Value': schedule}])
