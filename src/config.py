import boto3
import os
import json


def get_secret(secret_name):
    secret_name = os.environ.get(secret_name, 'TwilioSecrets')
    region_name = "eu-central-1"

    session = boto3.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get('SecretString')
        if secret_string:
            return json.loads(secret_string)
        else:
            raise ValueError("Secret string is empty")
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
