from app.data.object_storage import TRACKS_BUCKET
from app.settings import settings


class StorageService:
    def __init__(self, s3, s3_public):
        self.s3 = s3
        self.s3_public = s3_public

    def save_file(self, file, key):
        self.s3.upload_file(file, TRACKS_BUCKET, key)

    def get_file_url(self, key):
        return self.s3_public.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Key" : key,
                "Bucket": TRACKS_BUCKET,
            },
            ExpiresIn=settings.EXPIRES_IN_TIME,
        )
