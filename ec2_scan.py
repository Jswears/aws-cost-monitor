import os
import boto3
import json

ec2_client = boto3.client('ec2')

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def scan_ec2_instances():
    try:
        print("Scanning EC2 instances...")
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_info = {
                    'InstanceId': instance['InstanceId'],
                    'State': instance['State']['Name'],
                    'Type': instance['InstanceType'],
                    'LaunchTime': instance['LaunchTime'].isoformat()
                }
                instances.append(instance_info)
        print("EC2 instances scanned successfully.")
        return instances
    except Exception as e:
        print(f"Error scanning EC2 instances: {e}")
        return []


def check_ec2_state(instances):
    if not instances:
        print("No EC2 instances found.")
        return

    for instance in instances:
        if instance['State'] == 'running':
            print(f"Instance {instance['InstanceId']} is running.")
        else:
            print(f"Instance {instance['InstanceId']} is not running.")


def save_ec2_instances_report(instances):
    output_file = os.path.join(output_dir, 'ec2_report.json')
    try:
        with open(output_file, 'w') as f:
            json.dump(instances, f, indent=4)
        print(f"EC2 instances report saved to {output_file}")
    except Exception as e:
        print(f"Error saving EC2 instances report: {e}")


def main():
    instances = scan_ec2_instances()
    check_ec2_state(instances)
    save_ec2_instances_report(instances)


if __name__ == "__main__":
    main()
