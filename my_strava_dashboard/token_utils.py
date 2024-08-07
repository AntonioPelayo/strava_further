import json
import os
import time

from stravalib import Client

TOKEN_FILE = 'tokens.json'

def access_token_expired(token_info):
    return time.time() > token_info['APP_ACCESS_TOKEN_EXPIRES_AT']

def load_token_info(token_file=TOKEN_FILE):
    if not os.path.exists(token_file):
        print(f"Token file {token_file} not found.")
        exit(1)

    with open(token_file, 'r') as f:
        token_info = json.load(f)

    if access_token_expired(token_info):
        token_info = refresh_token(token_info, token_file)

    return token_info

def refresh_token(token_info, token_file=TOKEN_FILE):
    client = Client()
    refresh_res = client.refresh_access_token(
        client_id=token_info['APP_CLIENT_ID'],
        client_secret=token_info['APP_CLIENT_SECRET'],
        refresh_token=token_info['APP_REFRESH_TOKEN']
    )

    token_info['APP_ACCESS_TOKEN'] = refresh_res['access_token']
    token_info['APP_ACCESS_TOKEN_EXPIRES_AT'] = refresh_res['expires_at']

    with open(token_file, 'w') as f:
        json.dump(token_info, f, indent=4)

    return token_info
