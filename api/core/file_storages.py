# Specifies different backends for deployment and debug

from django.conf import settings
from django.core.files.storage import default_storage
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        super(S3MediaStorage, self).__init__(*args, **kwargs)
