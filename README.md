# AWS Cost Monitor (Junior Project)

## Goal

Scan an AWS account to identify potentially idle or wasteful resources, such as EC2 instances.

## Features

- List EC2 instances and their states.
- Fetch average CPU usage from CloudWatch.
- Flag idle instances (e.g. CPU < 5% for 7 days).
- Save report to `output/ec2_report.json`.
- Command-line interface for easy execution.
- Send WhatsApp notifications for idle instances using Twilio.

## 🧠 CLI Arguments

| Option        | Description                        |
| ------------- | ---------------------------------- |
| `--region`    | AWS region (default: eu-central-1) |
| `--threshold` | Idle CPU threshold (default: 5.0%) |

## 🚀 Example Usage

```bash
python3 ec2_monitor.py --region us-west-1 --threshold 3.5
```

## How to Run

1. **Set Up AWS Credentials**  
   Use the AWS CLI to configure your credentials if not already done:

```bash
aws configure
```

2. **Prepare Twilio for Notifications**

- Create a Twilio account.
- Set up the WhatsApp sandbox for sending notifications.

3. **Configure Environment Variables**

- Create a `.env` file or export the required variables directly.
- Refer to `.env.example` for the necessary variables.

4. **Run the Script**  
   Execute the script using Python:

```bash
python3 ec2_monitor.py
```

## Output Example

```json
{
  "InstanceId": "i-1234567890abcdef0",
  "State": "running",
  "CPU": 3.2,
  "Idle": true
}
```

## Tech

- Python3
- Boto3
