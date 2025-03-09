import json
import os
import requests
import boto3
import datetime
import jwt

def lambda_handler(event, context):
    nlb_url = os.environ.get("NLB_BASE_URL") # "http://a0f1930b83c3a42fba244bbbf1fec19d-183ddb5ee5b3c08f.elb.us-east-1.amazonaws.com:3001"
    secret_key = get_jwt_secret()

    try:
        document_id = event.get("document_id")

        if not document_id:
            token = generate_jwt_token(secret_key, False)

            return generate_success_response(False, token)

        # Chamada para o NLB para buscar o cliente - API publicada no cluster EKS
        response = requests.get(f"{nlb_url}/customers/{document_id}")
        response.raise_for_status()

        if response.status_code == 404:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Client not found"})
            }

        client_info = response.json()

        token = generate_jwt_token(secret_key, True, client_info)

        return generate_success_response(True, token)
            
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def get_jwt_secret():
    secret_name = "jwt_secret"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret = client.get_secret_value(SecretId=secret_name)
    secret_string = json.loads(secret['SecretString'])
    return secret_string['key']

def generate_jwt_token(secret_key: str, identified_customer: bool, customerInfo = None):
    if customerInfo is not None:
        payload = {
            "name": customerInfo.get("name"),
            "document_id": customerInfo.get("document_id"),
            "identified_customer": identified_customer,
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
        }
    else:
        payload = {
            "identified_customer": identified_customer,
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
        }

    return jwt.encode(payload, secret_key, algorithm="HS256")

def generate_success_response(identifed_customer: bool, token: str):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "identified_customer": identifed_customer,
            "token": token
        })
    }
