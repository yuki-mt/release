import boto3
from typing import Optional
import os
from argparse import ArgumentParser, Namespace
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SUBJECT = 'title'
SENDER = "YOUR NAME <no-reply@foo.com>"
SES_REGION = 'us-west-2'


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--recipient', '-r', type=str,
                        required=True)
    parser.add_argument('--attachment_path', '-a', type=str)
    return parser.parse_args()


def send_email(recipient: str, body: str, file_path: Optional[str]):
    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = recipient
    msg.attach(MIMEText(body))

    if file_path is not None:
        with open(file_path, "rb") as attachment:
            part = MIMEApplication(attachment.read())
            part.add_header("Content-Disposition",
                            "attachment",
                            filename=os.path.basename(file_path))
        msg.attach(part)

    client = boto3.client("ses", region_name=SES_REGION)
    return client.send_raw_email(
        Source=SENDER,
        Destinations=[recipient],
        RawMessage={"Data": msg.as_string()}
    )


def main():
    args = get_args()
    with open(os.path.join(os.path.dirname(__file__), 'body.txt')) as f:
        body = f.read()
    send_email(args.recipient, body, args.attachment_path)


if __name__ == '__main__':
    main()
