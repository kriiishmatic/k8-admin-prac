from flask import Flask
import boto3
import os
import logging
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

REGION = os.getenv("AWS_REGION", "us-east-1")
SECRET_NAME = os.getenv("SECRET_NAME", "roboshop/dev/mysql_password")


def get_secret():

    client = boto3.client(
        "secretsmanager",
        region_name=REGION
    )

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    return json.loads(response["SecretString"])


def get_identity():

    client = boto3.client(
        "sts",
        region_name=REGION
    )

    return client.get_caller_identity()


@app.route("/")
def home():

    return {
        "application": "AWS SDK Secret Reader",
        "status": "Running",
        "available_endpoints": [
            "/health",
            "/identity",
            "/secret"
        ]
    }


@app.route("/health")
def health():

    return {
        "status": "UP"
    }


@app.route("/identity")
def identity():

    try:

        identity = get_identity()

        logging.info(identity)

        return {
            "status": "SUCCESS",
            "identity": identity
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "status": "FAILED",
            "error": str(e)
        }, 500


@app.route("/secret")
def secret():

    try:

        secret = get_secret()

        logging.info(secret)

        return {
            "status": "SUCCESS",
            "secret": secret
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "status": "FAILED",
            "error": str(e)
        }, 500


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080
    )