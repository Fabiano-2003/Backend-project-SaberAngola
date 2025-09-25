# Backend Services e Utils

## Implementação de Serviços e Utilitários

1. Auth Service
```python
# apps/users/services.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from datetime import datetime, timedelta

User = get_user_model()

class AuthService:
    @staticmethod
    def generate_verification_token(user):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, settings.SECRET_KEY, algorithm='HS256')
        
        user.verification_token = token
        user.save()
        return token
    
    @staticmethod
    def verify_email(token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user = User.objects.get(id=payload['user_id'])
            user.is_verified = True
            user.verification_token = ''
            user.save()
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return False
    
    @staticmethod
    def send_verification_email(user):
        token = AuthService.generate_verification_token(user)
        context = {
            'user': user,
            'verify_url': f"{settings.FRONTEND_URL}/verify-email?token={token}"
        }
        
        html_message = render_to_string(
            'email/verify_email.html',
            context
        )
        
        send_mail(
            subject='Verifique seu email - SaberAngola',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message
        )
```

2. Payment Service
```python
# apps/payments/services.py
import uuid
from decimal import Decimal
from django.conf import settings
from .models import Payment, Invoice
from datetime import datetime, timedelta

class PaymentService:
    @staticmethod
    def generate_transaction_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_invoice_number():
        prefix = datetime.now().strftime('%Y%m')
        count = Invoice.objects.filter(
            invoice_number__startswith=prefix
        ).count()
        return f"{prefix}-{str(count + 1).zfill(4)}"
    
    @staticmethod
    def process_payment(payment: Payment):
        if payment.status != 'pending':
            return
        
        try:
            # Integração com gateway de pagamento aqui
            payment.status = 'completed'
            payment.save()
            
            # Criar fatura
            due_date = datetime.now() + timedelta(days=30)
            Invoice.objects.create(
                payment=payment,
                invoice_number=PaymentService.generate_invoice_number(),
                due_date=due_date
            )
            
        except Exception as e:
            payment.status = 'failed'
            payment.save()
            raise e
```

3. Document Service
```python
# apps/documents/services.py
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
```

4. Notification Service
```python
# apps/notifications/services.py
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Notification

class NotificationService:
    @staticmethod
    def create_notification(user, title, message, notification_type='info'):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )
    
    @staticmethod
    def get_unread_count(user):
        return Notification.objects.filter(
            user=user,
            read=False
        ).count()
    
    @staticmethod
    def clean_old_notifications(days=30):
        cutoff_date = datetime.now() - timedelta(days=days)
        Notification.objects.filter(
            Q(created_at__lt=cutoff_date),
            Q(read=True) | Q(notification_type='info')
        ).delete()
```

5. Cache Service
```python
# apps/core/services.py
from django.core.cache import cache
from django.conf import settings
from typing import Any, Optional
import hashlib
import json

class CacheService:
    @staticmethod
    def generate_key(prefix: str, *args: Any) -> str:
        """Generate a cache key based on prefix and arguments"""
        key_parts = [prefix] + [str(arg) for arg in args]
        key_string = ':'.join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        return cache.get(key)
    
    @staticmethod
    def set(
        key: str,
        value: Any,
        timeout: Optional[int] = None
    ) -> None:
        """Set value in cache with optional timeout"""
        if timeout is None:
            timeout = settings.CACHE_TIMEOUT
        cache.set(key, value, timeout)
    
    @staticmethod
    def delete(key: str) -> None:
        """Delete value from cache"""
        cache.delete(key)
    
    @staticmethod
    def get_or_set(
        key: str,
        default_func: callable,
        timeout: Optional[int] = None
    ) -> Any:
        """Get value from cache or set it if not exists"""
        value = cache.get(key)
        if value is None:
            value = default_func()
            CacheService.set(key, value, timeout)
        return value
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> None:
        """Invalidate all keys matching pattern"""
        keys = cache.keys(pattern)
        if keys:
            cache.delete_many(keys)
```