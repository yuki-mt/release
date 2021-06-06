# detail: https://qiita.com/eito_2/items/ef77e44955e43f31ba78
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import argparse
import os
from typing import Optional


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', '-e', type=str, required=True)
    parser.add_argument('--password', '-p', type=str, required=True)
    parser.add_argument('--to_address', '-t', type=str, required=True)
    parser.add_argument('--attachment_path', '-a', type=str)
    return parser.parse_args()


def login(email: str, password: str) -> SMTP:
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(email, password)
    return smtp


def build_content(from_addr: str, to_addr: str, subject: str, body: str,
                  attachment_path: Optional[str]) -> MIMEMultipart:
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
    return message


def main():
    args = get_args()
    smtp = login(args.email, args.password)
    msg = build_content(args.email, args.to_address, '件名', 'a\nb',
                        args.attachment_path)
    smtp.send_message(msg)
    smtp.close()


if __name__ == '__main__':
    main()
