import os
import datetime
import json

output_dir = '/tmp'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


def save_ec2_instances_report(instances):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'ec2_report_{timestamp}.json')
    try:
        with open(output_file, 'w') as f:
            json.dump(instances, f, indent=4)
        print(f"EC2 instances report saved to {output_file}")
    except Exception as e:
        print(f"Error saving EC2 instances report: {e}")
