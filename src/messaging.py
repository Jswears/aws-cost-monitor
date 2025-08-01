from twilio.rest import Client
import os
from dotenv import load_dotenv
from config import get_secret

# Load environment variables from .env file
# load_dotenv()

# Fetch Twilio secrets from AWS Secrets Manager
secrets = get_secret('TwilioSecrets')


def get_twilio_credentials():
    if secrets:
        try:
            return {
                'account_sid': secrets['TWILIO_ACCOUNT_SID'],
                'auth_token': secrets['TWILIO_AUTH_TOKEN'],
                'whatsapp_from': secrets['TWILIO_WHATSAPP_FROM'],
                'whatsapp_to': secrets['WHATSAPP_TO']
            }
        except KeyError as e:
            print(f"Missing key in secrets: {e}")
            return None
    else:
        print("No secrets found. Please check your AWS Secrets Manager configuration.")
        return None


def send_whatsapp_message(instances):
    credentials = get_twilio_credentials()
    if not credentials:
        print("Failed to retrieve Twilio credentials.")
        return

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
            credentials['account_sid'],
            credentials['auth_token']
        )
        message = client.messages.create(
            body=message,
            from_=credentials['whatsapp_from'],
            to=credentials['whatsapp_to'],
        )
        print(f"WhatsApp message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
