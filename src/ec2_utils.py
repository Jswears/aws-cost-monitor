import datetime
import boto3
from args import args


ec2_client = boto3.client('ec2', region_name=args.region)
cloudwatch_client = boto3.client('cloudwatch', region_name=args.region)


def check_ec2_state(instances, threshold):
    if not instances:
        print("No EC2 instances found.")
        return

    for instance in instances:
        cpu = get_average_cpu_utilization(instance['InstanceId'])
        instance['AverageCPUUtilization'] = cpu

        if instance['State'] != 'running':
            instance['Idle'] = False
            print(f"Instance {instance['InstanceId']} is not running.")
            continue

        if cpu is not None and cpu < threshold:
            instance['Idle'] = True
            print(f"Instance {instance['InstanceId']} is idle (CPU: {cpu}%)")
        else:
            instance['Idle'] = False
            print(f"Instance {instance['InstanceId']} is active (CPU: {cpu}%)")


def get_average_cpu_utilization(instance_id):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=7)  # Last 7 days

    try:
        print(f"Fetching CPU utilization for instance {instance_id}...")
        metrics = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start,
            EndTime=end,
            Period=3600,
            Statistics=['Average']
        )

        datapoints = metrics['Datapoints']
        if not datapoints:
            print(f"No CPU utilization data found for instance {instance_id}.")
            return None

        average_cpu = sum(dp['Average'] for dp in datapoints) / len(datapoints)
        return round(average_cpu, 2)
    except Exception as e:
        print(
            f"Error fetching CPU utilization for instance {instance_id}: {e}")
        return None


def scan_ec2_instances(region):
    try:
        print(f"Scanning EC2 instances in region {region}...")
        ec2_client = boto3.client('ec2', region_name=region)
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                instance_info = {
                    'InstanceId': instance.get('InstanceId'),
                    'State': instance.get('State', {}).get('Name'),
                    'Type': instance.get('InstanceType'),
                    'LaunchTime': instance.get('LaunchTime').isoformat() if instance.get('LaunchTime') else None
                }
                instances.append(instance_info)
        print(f"EC2 instances scanned successfully in region {region}.")
        return instances
    except Exception as e:
        print(f"Error scanning EC2 instances in region {region}: {e}")
        return []
