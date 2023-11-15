import boto3
import json
import os
from datetime import datetime
from werkzeug.datastructures import FileStorage

from app import app

s3 = boto3.client("s3")
sns = boto3.client("sns")


def rename_file(filename: str):
    """
    Add timestamp to filename
    """
    uploaded_date = datetime.utcnow()

    name, extension = os.path.splitext(filename)
    return f"{uploaded_date.strftime('%Y%m%d%H%M%S')}_{name}.{extension}"


def upload_file(file: FileStorage) -> str:
    """
    Upload the file to s3
    """
    filename = rename_file(file.filename)
    s3.upload_fileobj(
        file,
        app.config["S3_BUCKET_NAME"],
        filename,
        ExtraArgs={
            "ContentType": file.content_type,
        },
    )
    return f"{app.config['S3_BUCKET_BASE_URL']}/{file.filename}"


def delete_file(file: FileStorage) -> str:
    """
    Delete the file from s3
    """
    s3.delete_object(
        app.config["S3_BUCKET_NAME"],
        file.filename,
    )
    return f"{file.filename} deleted"


def notify_preprocessor(s3_url: str) -> None:
    """
    Send a message to the SNS topic that the preprocessor is subscribed to,
    containing the s3 url of the newly uploaded file.

    create_topic is idempotent and will only create a new topic the first time.
    The topic could also be created via terraform, CloudFormation etc.

    """
    topic_arn = sns.create_topic(
        Name='NewFileUploadTopic'
    )
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps({"payload": {"s3_url": s3_url}})
    )
