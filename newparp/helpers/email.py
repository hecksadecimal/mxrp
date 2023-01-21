import os
import boto3
from botocore.exceptions import ClientError
from flask import g, render_template, url_for
from uuid import uuid4
from sentry_sdk import capture_exception

expiry_times = {
    "welcome": 86400,
    "verify": 86400,
    "reset": 600,
}

subjects = {
    "welcome": "Welcome to MxRP!",
    "verify": "Verify your e-mail address",
    "reset": "Reset your password",
}

keys = {
    "welcome": "verify",
    "verify": "verify",
    "reset": "reset",
}


def send_email(action, email_address):
    email_token = str(uuid4())
    g.redis.setex(
        ":".join([keys[action], str(g.user.id), email_address]),
        expiry_times[action],
        email_token,
    )
    AWS_REGION = "us-east-1"
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
    SUBJECT = subjects[action]
    SENDER = "Mixed Roleplay <no-reply@mxrp.chat>"
    RECIPIENT = email_address
    BODY_TEXT = render_template("email/%s_plain.html" % action, user=g.user, email_address=email_address, email_token=email_token)
    BODY_HTML = render_template("email/%s.html" % action, user=g.user, email_address=email_address, email_token=email_token)
    CHARSET = "UTF-8"

    client = boto3.client('ses',
                          region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_KEY
                          )

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        pass

