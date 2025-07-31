# ☁️ AWS EC2 Cost Monitor (Python + CloudWatch + WhatsApp Alerts)

A Python-based tool that scans your AWS EC2 instances, checks average CPU usage over the past 7 days via CloudWatch, identifies idle instances, and sends automated WhatsApp alerts using Twilio.

---

## 🎯 Goal

Scan an AWS account to detect potentially idle EC2 instances based on average CPU usage and notify the user via WhatsApp for cost-saving opportunities.

---

## ✅ Features

- 🔍 List EC2 instances and their states
- 📊 Fetch 7-day average CPU from CloudWatch
- 💤 Identify idle instances (e.g., CPU < 5%)
- 📝 Save structured report to `output/ec2_report_<timestamp>.json`
- 💬 WhatsApp alerts using Twilio Sandbox API
- 🧩 CLI arguments for region and CPU threshold
- 🔐 Uses `.env` for secret management

---

## 📦 Tech Stack

- Python 3
- AWS Boto3 SDK
- AWS EC2 + CloudWatch
- Twilio API (WhatsApp)
- `argparse`, `dotenv`, `json`
- [`uv`](https://github.com/astral-sh/uv) for fast virtualenv + dependency management

---

## ⚙️ CLI Arguments

| Argument      | Description                     | Default        |
| ------------- | ------------------------------- | -------------- |
| `--region`    | AWS region to scan              | `eu-central-1` |
| `--threshold` | CPU threshold to mark as "idle" | `5.0`          |

---

## 🚀 Example Usage

```bash
python3 ec2_monitor.py --region us-west-2 --threshold 3.5
```

---

## 🔧 Installation

### 1. Clone the Repo

```bash
git clone https://github.com/Jswears/aws-cost-monitor.git
cd aws-cost-monitor
```

### 2. Install Dependencies

#### 🌀 Option A: Using `uv` (recommended)

```bash
uv venv
source .venv/bin/activate
uv add boto3 twilio python-dotenv
```

#### 🧪 Option B: Using `pip`

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔐 Setup

### 1. Configure AWS CLI

```bash
aws configure
```

### 2. Prepare Twilio WhatsApp Sandbox

- Sign up at [twilio.com](https://www.twilio.com/)
- Join the [Twilio WhatsApp sandbox](https://www.twilio.com/whatsapp)
- Link your phone by sending the join code via WhatsApp

### 3. Create `.env` File

Use the `.env.example` as a reference:

```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+YOUR_PHONE_NUMBER
```

> ⚠️ Do not commit your `.env` file — keep it in your `.gitignore`.

---

## 📝 Output Example

```json
{
  "InstanceId": "i-1234567890abcdef0",
  "State": "running",
  "Type": "t2.micro",
  "LaunchTime": "2025-07-21T12:30:45Z",
  "AverageCPUUtilization": 2.3,
  "Idle": true
}
```

---

## 🧠 What I Learned

- Using AWS SDK (Boto3) for EC2 and CloudWatch
- Metric-based decision making for cloud cost optimization
- Building CLI tools with `argparse`
- Secure alerting integration with Twilio and WhatsApp
- Managing Python environments and dependencies with `uv`
- Clean code structure, error handling, and modularization

---

## 📈 Coming Soon

- Email and/or SNS alerts
- Lambda deployment option
- Scheduled execution with cron or GitHub Actions
- Support for other idle resources (RDS, EBS, etc.)

---

## 🗂️ .gitignore (Recommended)

```
.venv/
.env
__pycache__/
output/
```

---

## 👤 Author

**Joaquín S.**
GitHub: [@Jswears](https://github.com/Jswears)
LinkedIn: [linkedin.com/in/joaquinswears](https://www.linkedin.com/in/joaquinswears)

---

## 🪪 License

MIT License
