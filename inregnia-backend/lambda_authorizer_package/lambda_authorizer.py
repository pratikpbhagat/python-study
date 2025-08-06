import json
import os
import re
import urllib.request

from jose import jwt, jwk

COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID', 'us-east-1_gPvqgtPeg')
COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-1')
COGNITO_APP_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '26topv8a1c2hfi2170pgb41n83')

JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
with urllib.request.urlopen(JWKS_URL) as response:
    jwks = json.loads(response.read())['keys']


def extract_token_from_cookie(headers):
    cookie_header = headers.get('cookie') or headers.get('Cookie')
    if not cookie_header:
        return None
    match = re.search(r'access_token=([^;]+)', cookie_header)
    return match.group(1) if match else None


def lambda_handler(event, context):
    token = extract_token_from_cookie(event['headers'])

    if not token:
        print("No token found in cookie")
        return generate_policy("unauthorized", "Deny")

    try:
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        key = next((k for k in jwks if k['kid'] == kid), None)

        if not key:
            raise Exception("Public key not found in JWKS")

        public_key = jwk.construct(key)

        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=COGNITO_APP_CLIENT_ID
        )

        # Optional: Check token_use
        if decoded_token.get('token_use') != 'access':
            raise Exception("Invalid token_use")

        print("Token verified successfully")
        return generate_policy(decoded_token['sub'], "Allow", decoded_token)

    except Exception as e:
        print(f"Authorization failed: {e}")
        return generate_policy("unauthorized", "Deny")


def generate_policy(principal_id, effect, context=None):
    policy = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "execute-api:Invoke",
                "Effect": effect,
                "Resource": "*"
            }]
        }
    }
    if context:
        policy['context'] = {k: str(v) for k, v in context.items()}
    return policy
