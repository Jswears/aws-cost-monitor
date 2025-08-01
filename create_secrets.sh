#!/bin/bash

# Create a new secret in AWS Secrets Manager with Twilio credentials

if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <TWILIO_ACCOUNT_SID> <TWILIO_AUTH_TOKEN> <TWILIO_WHATSAPP_FROM> <WHATSAPP_TO>"
    exit 1
fi

TWILIO_ACCOUNT_SID=$1
TWILIO_AUTH_TOKEN=$2
TWILIO_WHATSAPP_FROM=$3
WHATSAPP_TO=$4

aws secretsmanager create-secret \
  --name TwilioSecrets \
  --secret-string "{
    \"TWILIO_ACCOUNT_SID\": \"$TWILIO_ACCOUNT_SID\",
    \"TWILIO_AUTH_TOKEN\": \"$TWILIO_AUTH_TOKEN\",
    \"TWILIO_WHATSAPP_FROM\": \"$TWILIO_WHATSAPP_FROM\",
    \"WHATSAPP_TO\": \"$WHATSAPP_TO\"
  }" \
  --description "Twilio secrets for messaging" \
  --region eu-central-1