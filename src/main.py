from ec2_utils import scan_ec2_instances, check_ec2_state
from messaging import send_whatsapp_message
# from reporting import save_ec2_instances_report
from args import args
import os


def run_monitor(region, threshold):
    os.environ['AWS_REGION'] = region

    instances = scan_ec2_instances(region)
    check_ec2_state(instances, threshold)
    # save_ec2_instances_report(instances) # Uncomment if you want to save the report
    send_whatsapp_message(instances)
    return instances


# === CLI mode ===
if __name__ == "__main__":
    run_monitor(args.region, args.threshold)


# === Lambda handler ===
def lambda_handler(event, context):
    region = event.get('region', 'eu-central-1')
    threshold = event.get('threshold', 80)
    return {"statusCode": 200, "body": run_monitor(region, threshold)}
