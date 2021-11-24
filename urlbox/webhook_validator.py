import datetime
import json
import hmac
import re
from hashlib import sha256
from urlbox import InvalidHeaderSignatureError

TIMESTAMP_REGEX = "^t=[0-9]+$"
SIGNATURE_REGEX = "^sha256=[0-9a-zA-Z]+$"
WEBHOOK_AGE_MAX_MINUTES = 5


def call(header_signature, payload, api_secret):
    """
      Returns True or raises a InvalidHeaderSignatureError depending upon if the header signature is part of a valid UrlBox webhook request.

      :param header_signature: x-urlbox-signature header from the Urlbox request to the client's webhook endpoint.

      :param payload: json body of the webhook request.

      :param api_secret: Your API secret found in your Urlbox
      Dashboard`https://urlbox.io/dashboard/api`

      This function parses the signature value to determine if it's part of a valid Urlbox webhook request.
    """

    try:
        timestamp, signature = header_signature.split(",")
    except ValueError as e:
        raise (InvalidHeaderSignatureError())

    _check_timestamp(timestamp)
    _check_signature(signature, timestamp, payload, api_secret)

    return True


def _check_signature(raw_signature, timestamp, payload, api_secret):
    if not re.search(SIGNATURE_REGEX, raw_signature):
        raise (InvalidHeaderSignatureError("Invalid signature"))


def _check_timestamp(timestamp):
    if not re.search(TIMESTAMP_REGEX, timestamp):
        raise (InvalidHeaderSignatureError("Invalid timestamp"))

    timestamp = int(timestamp.split("=")[1])

    _check_webhook_creation_time(timestamp)


def _check_webhook_creation_time(timestamp):
    header_datetime = datetime.datetime.utcfromtimestamp(timestamp)

    current_datetime = datetime.datetime.utcnow()

    webhook_posted = current_datetime - header_datetime
    webhook_posted_minutes_ago = webhook_posted.total_seconds() / 60

    if webhook_posted_minutes_ago > WEBHOOK_AGE_MAX_MINUTES:
        raise (InvalidHeaderSignatureError("Invalid timestamp"))
