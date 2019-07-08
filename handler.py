import json

import boto3
from botocore.exceptions import ClientError


client = boto3.client("ses", region_name="eu-west-1")

TEMPLATE = """
From: {name} <{email}>

Message: {message}
"""


def send_mail(event, context):
    data = event["body"]

    try:
        response = client.send_email(
            Destination={"ToAddresses": ["p.karkut@lunarwings.dev"]},
            Message={
                "Body": {"Text": {"Charset": "utf8", "Data": TEMPLATE.format(**data)}},
                "Subject": {"Charset": "utf8", "Data": data["subject"]},
            },
            Source="contact@lunarwings.dev",
        )
    except ClientError as e:
        response = {"statusCode": 500, "body": repr(e)}
    except KeyError:
        response = {"statusCode": 409}
    else:
        response = {"statusCode": 204}

    return response
