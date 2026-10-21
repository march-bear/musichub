from app.data.object_storage import PROJECTS_BUCKET
from app.settings import settings


class StorageService:
    def __init__(self, s3, s3_public):
        self.s3 = s3
        self.s3_public = s3_public

    def save_file(self, file, key):
        self.s3.upload_file(file, PROJECTS_BUCKET, key)

    def get_file_url(self, key):
        return self.s3_public.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Key" : key,
                "Bucket": PROJECTS_BUCKET,
            },
            ExpiresIn=settings.RUSTFS_URL_EXPIRES_IN_TIME,
        )
