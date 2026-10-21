import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.settings import settings

s3 = boto3.client(
    "s3",
    endpoint_url=f"http://{settings.OBJECT_STORAGE_HOST}:{settings.OBJECT_STORAGE_PORT}",
    aws_access_key_id=settings.OBJECT_STORAGE_ACCESS_KEY,
    aws_secret_access_key=settings.OBJECT_STORAGE_SECRET_KEY,
    region_name="us-east-1",
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)

s3_public = boto3.client(
    "s3",
    endpoint_url=settings.OBJECT_STORAGE_PUBLIC_URL,
    aws_access_key_id=settings.OBJECT_STORAGE_ACCESS_KEY,
    aws_secret_access_key=settings.OBJECT_STORAGE_SECRET_KEY,
    region_name="us-east-1",
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)

PROJECTS_BUCKET = "projects"
SOUNDS_BUCKET = "sounds"

buckets = [PROJECTS_BUCKET, SOUNDS_BUCKET]

for bucket in buckets:
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError:
        s3.create_bucket(Bucket=bucket)
