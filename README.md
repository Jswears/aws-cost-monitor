# AWS Cost Monitor (Junior Project)

## Goal

Scan an AWS account to identify potentially idle or wasteful resources, such as EC2 instances.

## Features

- List EC2 instances and their states.
- Fetch average CPU usage from CloudWatch.
- Flag idle instances (e.g. CPU < 5% for 7 days).
- Save report to `output/ec2_report.json`.

## How to Run

```bash
aws configure # Set up your AWS credentials if not already done
python3 ec2_scan.py
```

## Output Example

```json
        {
            "InstanceId": "i-1234567890abcdef0",
            "State": "running",
            "CPU": 3.2,
            "Idle": true
        },
```

## Tech

- Python3
- Boto3
