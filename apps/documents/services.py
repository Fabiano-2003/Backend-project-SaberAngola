import boto3
from django.conf import settings
from .models import Document
from datetime import datetime

class DocumentService:
    @staticmethod
    def upload_to_s3(file, path_prefix='documents'):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        
        filename = f"{path_prefix}/{datetime.now().strftime('%Y/%m/%d')}/{file.name}"
        
        s3.upload_fileobj(
            file,
            settings.AWS_STORAGE_BUCKET_NAME,
            filename,
            ExtraArgs={'ACL': 'private'}
        )
        
        return filename
    
    @staticmethod
    def generate_download_url(file_key, expires_in=3600):
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': file_key
            },
            ExpiresIn=expires_in
        )
        
        return url