import json
import os
import requests
import boto3
import datetime
import jwt

def lambda_handler(event, context):
    try:
        if event.get("body", None) is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid request body"})
            }
            
        try :
            event_body = json.loads(event.get("body", None))
        except:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid request body"})
            }            

        return generate_token_for_customer(event_body.get("document", None))
            
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def generate_token_for_customer(document_id: str | None):
    nlb_url = os.environ.get("NLB_BASE_URL")

    if not document_id or document_id == "":
        token = generate_jwt_token(False)

        return generate_success_response(False, token)

    # Chamada para o NLB para buscar o cliente - API publicada no cluster EKS
    response = requests.get(f"{nlb_url}/customers/{document_id}")

    if response.status_code == 404:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Client not found"})
        }    
    elif not response.ok:
        return {
            "statusCode": response.status_code,
            "body": json.dumps({"error": "Service error"})
        }

    client_info = response.json()

    userInfo = {
        "name": client_info.get("name"),
        "identification_number": client_info.get("document_id")
    }

    token = generate_jwt_token(True, userInfo)

    return generate_success_response(True, token)

def generate_jwt_token(identified_user: bool, userInfo = None):
    secret_key = get_jwt_secret()

    if userInfo is not None:
        payload = {
            "name": userInfo.get("name"),
            "identification_number": userInfo.get("identification_number"),
            "identified_user": identified_user,
            "user_type": 'customer',
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
        }
    else:
        payload = {
            "identified_user": identified_user,
            "user_type": 'customer',
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
        }

    return jwt.encode(payload, secret_key, algorithm="HS256")

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

def generate_success_response(identified_user: bool, token: str):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "identified_user": identified_user,
            "token": token
        })
    }
