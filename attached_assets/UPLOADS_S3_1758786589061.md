# Uploads e Armazenamento (S3) - SaberAngola

Este documento detalha o sistema de upload e armazenamento de arquivos usando Amazon S3 no projeto SaberAngola, incluindo configuração, implementação e boas práticas.

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Configuração do S3](#2-configuração-do-s3)
3. [Implementação Backend](#3-implementação-backend)
4. [Implementação Frontend](#4-implementação-frontend)
5. [Gerenciamento de Arquivos](#5-gerenciamento-de-arquivos)
6. [Segurança e Boas Práticas](#6-segurança-e-boas-práticas)
7. [URLs Pré-assinadas](#7-urls-pré-assinadas)
8. [Processamento de Imagens](#8-processamento-de-imagens)
9. [Monitoramento e Logs](#9-monitoramento-e-logs)
10. [Exemplos Práticos](#10-exemplos-práticos)

## 1. Visão Geral

O sistema de armazenamento do SaberAngola utiliza Amazon S3 para:
- Upload de documentos gerados
- Armazenamento de avatares de usuários
- Backups de dados
- Arquivos temporários
- Templates de documentos

### 1.1. Características Principais

- Upload direto para S3
- URLs pré-assinadas para downloads seguros
- Processamento de imagens sob demanda
- Organização por pastas lógicas
- Backup automático
- Controle de acesso granular

## 2. Configuração do S3

### 2.1. Configuração do Bucket

```python
# settings.py
AWS_ACCESS_KEY_ID = 'sua_access_key'
AWS_SECRET_ACCESS_KEY = 'sua_secret_key'
AWS_STORAGE_BUCKET_NAME = 'saberangola-storage'
AWS_S3_REGION_NAME = 'af-south-1'  # África do Sul
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'private'
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Configurações de Cache
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Estrutura de pastas
MEDIA_ROOT = 'media/'
DOCUMENTS_ROOT = 'documents/'
TEMPLATES_ROOT = 'templates/'
BACKUP_ROOT = 'backups/'
```

### 2.2. CORS Configuration

```json
{
    "CORSRules": [
        {
            "AllowedOrigins": ["https://saberangola.ao"],
            "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
            "AllowedHeaders": ["*"],
            "ExposeHeaders": ["ETag"],
            "MaxAgeSeconds": 3000
        }
    ]
}
```

## 3. Implementação Backend

### 3.1. Serviço de Upload

```python
# storage/services.py
import boto3
from botocore.exceptions import ClientError

class S3Service:
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_file(self, file_obj, key, content_type=None):
        try:
            extra_args = {'ContentType': content_type} if content_type else {}
            self.s3.upload_fileobj(
                file_obj,
                self.bucket,
                key,
                ExtraArgs=extra_args
            )
            return self._generate_url(key)
        except ClientError as e:
            logging.error(f"Erro no upload: {str(e)}")
            raise
    
    def _generate_url(self, key, expires_in=3600):
        try:
            url = self.s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': key
                },
                ExpiresIn=expires_in
            )
            return url
        except ClientError as e:
            logging.error(f"Erro ao gerar URL: {str(e)}")
            raise
```

### 3.2. Modelos Django

```python
# storage/models.py
from django.db import models
from django.utils.text import slugify
import uuid

class StoredFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    original_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=512)
    content_type = models.CharField(max_length=100)
    size = models.BigIntegerField()
    uploaded_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def extension(self):
        return self.original_name.split('.')[-1].lower()
    
    def generate_s3_key(self):
        slug = slugify(self.original_name.rsplit('.', 1)[0])
        return f"{settings.MEDIA_ROOT}{self.id}/{slug}.{self.extension}"
```

### 3.3. Views

```python
# storage/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class FileUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        file_obj = request.FILES['file']
        
        stored_file = StoredFile.objects.create(
            original_name=file_obj.name,
            content_type=file_obj.content_type,
            size=file_obj.size,
            uploaded_by=request.user
        )
        
        s3_key = stored_file.generate_s3_key()
        stored_file.s3_key = s3_key
        stored_file.save()
        
        s3_service = S3Service()
        url = s3_service.upload_file(
            file_obj,
            s3_key,
            content_type=file_obj.content_type
        )
        
        return Response({
            'id': stored_file.id,
            'url': url
        })
    
    @action(detail=True, methods=['get'])
    def download_url(self, request, pk=None):
        stored_file = self.get_object()
        s3_service = S3Service()
        url = s3_service._generate_url(stored_file.s3_key)
        return Response({'url': url})
```

## 4. Implementação Frontend

### 4.1. Componente de Upload

```typescript
// components/FileUpload.tsx
import { useState } from 'react'
import axios from 'axios'

interface UploadProps {
  onSuccess: (url: string) => void
  onError: (error: string) => void
}

export const FileUpload: React.FC<UploadProps> = ({ onSuccess, onError }) => {
  const [uploading, setUploading] = useState(false)
  
  const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return
    
    const formData = new FormData()
    formData.append('file', file)
    
    setUploading(true)
    try {
      const response = await axios.post('/api/files/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      onSuccess(response.data.url)
    } catch (error) {
      onError('Erro no upload do arquivo')
      console.error('Upload error:', error)
    } finally {
      setUploading(false)
    }
  }
  
  return (
    <div>
      <input
        type="file"
        onChange={handleUpload}
        disabled={uploading}
      />
      {uploading && <p>Enviando arquivo...</p>}
    </div>
  )
}
```

### 4.2. Hook de Gerenciamento de Arquivos

```typescript
// hooks/useFileManagement.ts
import { useState } from 'react'
import axios from 'axios'

export const useFileManagement = () => {
  const [files, setFiles] = useState<StoredFile[]>([])
  
  const uploadFile = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await axios.post('/api/files/upload/', formData)
    return response.data
  }
  
  const getDownloadUrl = async (fileId: string) => {
    const response = await axios.get(`/api/files/${fileId}/download_url/`)
    return response.data.url
  }
  
  const deleteFile = async (fileId: string) => {
    await axios.delete(`/api/files/${fileId}/`)
  }
  
  return { files, uploadFile, getDownloadUrl, deleteFile }
}
```

## 5. Gerenciamento de Arquivos

### 5.1. Lifecycle Rules

```json
{
    "Rules": [
        {
            "ID": "DeleteTempFiles",
            "Prefix": "temp/",
            "Status": "Enabled",
            "ExpirationInDays": 1
        },
        {
            "ID": "MoveOldFiles",
            "Prefix": "documents/",
            "Status": "Enabled",
            "Transition": {
                "Days": 90,
                "StorageClass": "STANDARD_IA"
            }
        }
    ]
}
```

### 5.2. Backup Strategy

```python
# storage/backup.py
class S3Backup:
    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_key = f"{settings.BACKUP_ROOT}{timestamp}/"
        
        # Backup logic here
        
        return backup_key
    
    def restore_backup(self, backup_key):
        # Restore logic here
        pass
```

## 6. Segurança e Boas Práticas

### 6.1. Validação de Arquivos

```python
# storage/validators.py
class FileValidator:
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf']
    
    def validate(self, file):
        if file.size > self.MAX_SIZE:
            raise ValidationError('Arquivo muito grande')
        
        if file.content_type not in self.ALLOWED_TYPES:
            raise ValidationError('Tipo de arquivo não permitido')
```

### 6.2. Controle de Acesso

```python
# storage/permissions.py
class FileAccessPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.uploaded_by == request.user
```

## 7. URLs Pré-assinadas

### 7.1. Geração de URLs

```python
# storage/utils.py
def generate_presigned_post(key, expires_in=3600):
    s3_client = boto3.client('s3')
    
    conditions = [
        {'bucket': settings.AWS_STORAGE_BUCKET_NAME},
        ['content-length-range', 0, 10485760],  # 0-10MB
    ]
    
    presigned_post = s3_client.generate_presigned_post(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        Conditions=conditions,
        ExpiresIn=expires_in
    )
    
    return presigned_post
```

## 8. Processamento de Imagens

### 8.1. Redimensionamento

```python
# storage/image_processing.py
from PIL import Image
from io import BytesIO

class ImageProcessor:
    def resize_image(self, image_data, max_size=(800, 800)):
        img = Image.open(BytesIO(image_data))
        img.thumbnail(max_size)
        
        output = BytesIO()
        img.save(output, format=img.format)
        return output.getvalue()
```

## 9. Monitoramento e Logs

### 9.1. Logging

```python
# storage/logging.py
import logging

logger = logging.getLogger('storage')

class StorageLogger:
    def log_upload(self, file_info):
        logger.info(
            'Upload: %s, Size: %s, Type: %s',
            file_info.original_name,
            file_info.size,
            file_info.content_type
        )
    
    def log_error(self, error):
        logger.error('Storage error: %s', str(error))
```

## 10. Exemplos Práticos

### 10.1. Upload de Avatar

```python
# users/services.py
class UserAvatarService:
    def update_avatar(self, user, image_file):
        processor = ImageProcessor()
        processed_image = processor.resize_image(image_file.read())
        
        s3_key = f"avatars/{user.id}.jpg"
        s3_service = S3Service()
        
        url = s3_service.upload_file(
            BytesIO(processed_image),
            s3_key,
            content_type='image/jpeg'
        )
        
        user.avatar_url = url
        user.save()
        return url
```

### 10.2. Download de Documento

```python
# documents/services.py
class DocumentDownloadService:
    def get_download_url(self, document):
        s3_service = S3Service()
        return s3_service._generate_url(
            document.s3_key,
            expires_in=300  # 5 minutos
        )
```

## Conclusão

O sistema de armazenamento S3 do SaberAngola é:

- **Seguro:** Implementação de melhores práticas de segurança
- **Escalável:** Preparado para crescimento do volume de dados
- **Eficiente:** Processamento otimizado de arquivos
- **Confiável:** Backup e redundância de dados
- **Flexível:** Suporte a diversos tipos de arquivos
- **Monitorável:** Logs e métricas detalhados

Para mais informações sobre casos específicos ou configurações avançadas, consulte a documentação da AWS ou entre em contato com a equipe de infraestrutura.