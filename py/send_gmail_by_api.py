# 1. Gmail APIの有効化とcredentials.jsonの取得を先にする:
# https://qiita.com/muuuuuwa/items/822c6cffedb9b3c27e21
# 2. Install packages
# poetry add google-api-python-client google-auth-httplib2 google-auth-oauthlib
# 3. create token and send email
# python send_gmail_by_api.py --create_token
# 4. from the next time, use the created token to send email
# python send_gmail_by_api.py

import pickle
import os.path
from typing import Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import base64
from email import encoders
from email.mime.text import MIMEText


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--secret_path', type=str, default='credentials.json')
    parser.add_argument('--token_path', type=str, default='token.pickle')
    parser.add_argument('--from_address', '-f', type=str, required=True)
    parser.add_argument('--to_address', '-t', type=str, required=True)
    parser.add_argument('--attachment_path', '-a', type=str)
    parser.add_argument('--create_token', action='store_true')
    return parser.parse_args()


def create_token(secret_path: str, token_path: str) -> Credentials:
    scope = ['https://www.googleapis.com/auth/gmail.send']
    flow = InstalledAppFlow.from_client_secrets_file(secret_path, scope)
    creds = flow.run_console()
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
    return creds


def get_credential(token_path: str) -> Credentials:
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    else:
        raise FileNotFoundError(
            'Token file not found. Run with --create_token option '
            'or change value of --token_path'
        )
    if not creds.valid and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds


def create_message(from_addr: str, to_addr: str, subject: str, body: str,
                   attachment_path: Optional[str]) -> dict:
    message = MIMEMultipart()
    message['From'] = from_addr
    message['To'] = to_addr
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    if attachment_path is not None:
        with open(attachment_path, 'rb') as f:
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload(f.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(attachment_path))
        message.attach(payload)
    encoded_msg = message.as_string().encode()
    return {'raw': base64.urlsafe_b64encode(encoded_msg).decode()}


def main():
    args = get_args()
    if args.create_token:
        cred = create_token(args.secret_path, args.token_path)
    else:
        cred = get_credential(args.token_path)
    service = build('gmail', 'v1', credentials=cred)
    message = create_message(args.from_address, args.to_address, '件名だ',
                             'ほんぶん\nｆ', args.attachment_path)
    service.users().messages().send(userId='me', body=message).execute()


if __name__ == '__main__':
    main()
