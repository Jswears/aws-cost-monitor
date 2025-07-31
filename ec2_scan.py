import datetime
import os
import boto3
import json
import argparse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_whatsapp_message(instances):
    idle_instances = [i for i in instances if i.get('Idle')]
    if not idle_instances:
        print("No idle instances to report.")
        return

    message = (
        "🚨 *Idle EC2 Instances Detected* 🚨\n\n"
        "The following EC2 instances are idle based on the CPU utilization threshold:\n\n"
    )
    for i in idle_instances:
        message += (
            f"• *Instance ID:* {i['InstanceId']}\n"
            f"  *CPU Utilization:* {i['AverageCPUUtilization']}%\n"
            f"  *State:* {i['State']}\n"
            f"  *Type:* {i['Type']}\n"
            f"  *Launch Time:* {i['LaunchTime']}\n\n"
        )
    message += "Please review these instances to optimize costs. 💡"

    # Send the message via WhatsApp
    print(f"Sending WhatsApp message:\n{message}")
    try:
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        message = client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_WHATSAPP_FROM'),
            to=os.getenv('WHATSAPP_TO') or ""
        )
        print(f"WhatsApp message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description='AWS EC2 Cost Monitor')
    parser.add_argument(
        '--region', type=str, default='eu-central-1', help='AWS region to use'
    )
    parser.add_argument('--threshold', type=float, default=5.0,
                        help='CPU utilization threshold for idle instances')
    args = parser.parse_args()
    return args


args = parse_args()

ec2_client = boto3.client('ec2', region_name=args.region)
cloudwatch_client = boto3.client('cloudwatch', region_name=args.region)

output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


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
        cpu = get_average_cpu_utilization(instance['InstanceId'])
        instance['AverageCPUUtilization'] = cpu

        if instance['State'] != 'running':
            instance['Idle'] = False
            print(f"Instance {instance['InstanceId']} is not running.")
            continue

        if cpu is not None and cpu < args.threshold:
            instance['Idle'] = True
            print(f"Instance {instance['InstanceId']} is idle (CPU: {cpu}%)")
        else:
            instance['Idle'] = False
            print(f"Instance {instance['InstanceId']} is active (CPU: {cpu}%)")


def save_ec2_instances_report(instances):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'ec2_report_{timestamp}.json')
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
    send_whatsapp_message(instances)


if __name__ == "__main__":
    main()
