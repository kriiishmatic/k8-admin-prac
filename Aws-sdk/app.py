from flask import Flask
import boto3
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

REGION = os.getenv("AWS_REGION", "us-east-1")
SECRET_NAME = os.getenv("SECRET_NAME", "roboshop/dev/mysql_password")


def get_secret():
    client = boto3.client("secretsmanager", region_name=REGION)

    response = client.get_secret_value(
        SecretId=SECRET_NAME
    )

    return response["SecretString"]


@app.route("/")
def home():
    try:
        secret = get_secret()

        logging.info(f"Retrieved Secret : {secret}")

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


@app.route("/health")
def health():
    return {
        "status": "UP"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )