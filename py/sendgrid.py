import http.client
from typing import Optional
import json
import os
from argparse import ArgumentParser, Namespace
import base64


API_KEY = os.environ['SENDGRID_API_KEY']
SENDER = "Your Name"
SENDER_EMAIL = "info@foo.com"
SUBJECT = '題名'


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--to_name', '-n', type=str,
                        required=True)
    parser.add_argument('--to_email', '-e', type=str,
                        required=True)
    parser.add_argument('--attachment_path', '-a', type=str)
    parser.add_argument('--file_type', '-f', type=str,
                        default='application/pdf')
    return parser.parse_args()


def send_email(to_name: str, to_email: str, body: str,
               file_type: str, file_path: Optional[str]):
    payload = {
        "personalizations": [{
            "to": [{"email": to_email, "name": to_name}],
            "subject": SUBJECT
        }],
        "from": {"email": SENDER_EMAIL, "name": SENDER},
        "reply_to": {"email": SENDER_EMAIL, "name": SENDER},
        "content": [{"type": "text/plain", "value": body}],
    }
    if file_path is not None:
        with open(file_path, 'rb') as f:
            file_body = base64.b64encode(f.read()).decode()
        payload['attachments'] = [{
            'content': file_body,
            'type': file_type,
            'filename': os.path.basename(file_path)
        }]
    headers = {
        'authorization': f"Bearer {API_KEY}",
        'content-type': "application/json"
    }

    conn = http.client.HTTPSConnection("api.sendgrid.com")
    conn.request("POST", "/v3/mail/send", json.dumps(payload), headers)
    res = conn.getresponse()
    print(res.read().decode("utf-8"))
    conn.close()


def main():
    args = get_args()
    # with open(os.path.join(os.path.dirname(__file__), 'body.txt')) as f:
    #     body = f.read()
    body = 'body text'
    send_email(args.to_name, args.to_email, body,
               args.file_type, args.attachment_path)


if __name__ == '__main__':
    main()
