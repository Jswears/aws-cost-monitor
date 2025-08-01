# ☁️ AWS EC2 Cost Monitor · Python + CloudWatch + WhatsApp Alerts

A Python-based tool that scans your AWS EC2 instances, checks average CPU usage over the past 7 days via CloudWatch, identifies idle instances, and sends automated WhatsApp alerts using Twilio.

---

## 🎯 Goal

Scan your AWS EC2 infrastructure to identify idle instances based on average CPU usage, then notify you via WhatsApp — helping reduce unnecessary costs.

---

## ✅ Features

- 🔍 Lists EC2 instances and their states
- 📊 Fetches 7-day average CPU from CloudWatch
- 💤 Detects idle instances (e.g., CPU < 5%)
- 📝 Saves structured reports to `output/` with timestamps
- 💬 Sends WhatsApp alerts using Twilio API
- 🧩 Supports CLI arguments for region and threshold
- 🔐 Loads secrets from `.env` locally or Secrets Manager in Lambda

---

## 📦 Tech Stack

- Python 3
- AWS Boto3 SDK
- AWS EC2 + CloudWatch
- SAM (Serverless Application Model) CLI
- Twilio API (WhatsApp)
- `argparse`, `dotenv`, `json`

---

## ⚙️ CLI Arguments

| Argument      | Description                     | Default        |
| ------------- | ------------------------------- | -------------- |
| `--region`    | AWS region to scan              | `eu-central-1` |
| `--threshold` | CPU threshold to mark as "idle" | `5.0`          |

---

## 🚀 Usage

### 🖥️ Local Execution

Ensure the report-saving lines in `main.py` are **uncommented**, and the `.env` loader in `messaging.py` is enabled.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python3 src/main.py --region eu-central-1 --threshold 5.0
```

---

### ☁️ Lambda Deployment

To deploy this as a serverless function using AWS SAM:

---

#### 1️⃣ Create Secrets in AWS Secrets Manager

First, make the script executable:

```bash
chmod +x create_secrets
```

Then store Twilio credentials securely:

```bash
./create_secrets <TWILIO_ACCOUNT_SID> <TWILIO_AUTH_TOKEN> <TWILIO_WHATSAPP_FROM> <WHATSAPP_TO>
```

---

#### 2️⃣ Install Python Dependencies for Lambda

```bash
pip install -r requirements.txt -t dependencies/python
```

---

#### 3️⃣ Build and Deploy via SAM CLI

```bash
sam build
sam deploy --guided
```

> 💡 Make sure your AWS CLI is configured with sufficient permissions.

---

## 🔧 Installation

### Prerequisites

- Python 3.12
- AWS CLI configured with EC2/CloudWatch access
- Twilio account with WhatsApp sandbox

---

### 1. Clone the Repo

```bash
git clone https://github.com/Jswears/aws-cost-monitor.git
cd aws-cost-monitor
```

### 2. Install Dependencies

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

---

### 2. Prepare Twilio WhatsApp Sandbox

- Sign up at [twilio.com](https://www.twilio.com/)
- Join the [Twilio WhatsApp sandbox](https://www.twilio.com/whatsapp)
- Link your phone using the join code via WhatsApp

---

### 3. Create `.env` File

```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+YOUR_PHONE_NUMBER
```

> ⚠️ **Do not commit your `.env` file.**

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

> 💡 Reports are saved to `output/` with timestamped filenames.

---

## 🧠 What I Learned

- Using AWS SDK (Boto3) for EC2 and CloudWatch
- Metric-based decision making for cloud cost optimization
- Building CLI tools with `argparse`
- Secure integration of Twilio + WhatsApp alerts
- Clean modular architecture and error handling

---

## 📈 Coming Soon

- ✅ Email and/or SNS alerts
- ✅ Support for S3-based report storage
- 🔄 Scheduled executions via cron or GitHub Actions
- 🗃️ Support for idle detection in other resources (RDS, EBS, etc.)

---

## 🗂️ .gitignore (Recommended)

```gitignore
venv/
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
