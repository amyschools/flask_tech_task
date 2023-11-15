import os

# only placeholders for now
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_ACCESS_SECRET = os.environ.get("AWS_ACCESS_SECRET")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BUCKET_BASE_URL = os.environ.get("S3_BUCKET_BASE_URL")
