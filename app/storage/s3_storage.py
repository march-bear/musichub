from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.util.exceptions import StorageException


def create_s3_client(endpoint_url: str, access_key: str, secret_key: str):
    return boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="us-east-1",
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            connect_timeout=5,
            read_timeout=30,
            retries={"max_attempts": 10, "mode": "standard"},
        ),
    )


class S3Storage:
    def __init__(self, client, presign_client, bucket: str, url_expires_in: int):
        self._client = client
        self._public_client = presign_client
        self._bucket = bucket
        self._url_expires_in = url_expires_in


    def ensure_bucket(self):
        try:
            self._client.head_bucket(Bucket=self._bucket)
        except ClientError as err:
            if err.response["Error"]["Code"] in ("404", "NoSuchKey", "NotFound"):
                return None
            self._client.create_bucket(Bucket=self._bucket)


    def put_file(self, file_path: Path, key: str):
        try:
            self._client.upload_file(file_path, self._bucket, key)
        except ClientError as err:
            raise StorageException() from err


    def delete(self, key: str):
        try:
            self._client.delete_object(Bucket=self._bucket, Key=key)  # идемпотентно
        except ClientError as err:
            raise StorageException() from err


    def get_url(self, key: str):
        return self._public_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Key": key, "Bucket": self._bucket},
            ExpiresIn=self._url_expires_in,
        )