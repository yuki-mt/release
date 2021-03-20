"""
SESでメール受信するときのLambdaのコード。
受信のアクションはS3 -> Lambda
Ref: https://dev.classmethod.jp/articles/receiving-email-with-amazon-ses/
"""
from email.parser import BytesParser
from email import policy
import boto3
import json
import urllib.request

BUCKET_NAME = 'xxx'


def notify(text: str):
    webhook_url = 'https://hooks.slack.com/services/xxx/xxx/xxx'
    payload = {
        "channel": "#general",
        "username": "my user",
        "icon_emoji": ":ghost:",
        'text': text
    }
    req = urllib.request.Request(webhook_url,
                                 json.dumps(payload).encode())
    with urllib.request.urlopen(req) as res:
        res.read()


def lambda_handler(event, context):
    ses_info = event['Records'][0]['ses']
    mail_info = ses_info['mail']
    subject = mail_info['commonHeaders']['subject'].encode('unicode-escape')\
        .decode('unicode-escape')
    message_id = ses_info['mail']['messageId']

    base_text = (f"From: {mail_info['source']}\n"
                 f"To: {', '.join(mail_info['destination'])}\n"
                 f"Subject: {subject}\n")
    if 'FAIL' in [
            ses_info['receipt']['spamVerdict']['status'],
            ses_info['receipt']['virusVerdict']['status'],
            ses_info['receipt']['spfVerdict']['status'],
            ses_info['receipt']['dkimVerdict']['status']]:
        text = base_text + 'Email failed one of the security tests.'
        notify(text)
        raise Exception(text)

    bucket = boto3.resource('s3').Bucket(BUCKET_NAME)
    raw_email = bucket.Object(message_id).get()['Body'].read()
    msg = BytesParser(policy=policy.SMTP).parsebytes(raw_email)

    plain = ''
    try:
        plain = msg.get_body(preferencelist=('plain'))
        plain = ''.join(plain.get_content().splitlines(keepends=True))
    except Exception:
        text = base_text + 'No plain text'
        notify(text)
        raise Exception(text)

    notify(f'{base_text} Body:\n{plain}')
