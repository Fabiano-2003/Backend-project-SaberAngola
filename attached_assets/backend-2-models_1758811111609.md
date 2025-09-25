# Backend Modelos Base

## Implementação dos Modelos Principais

1. Modelo de Usuário
```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Profile of {self.user.email}'
```

2. Modelo de Documento
```python
# apps/documents/models.py
from django.db import models
from django.conf import settings

class Document(models.Model):
    DOCUMENT_TYPES = (
        ('article', 'Artigo'),
        ('thesis', 'Tese'),
        ('report', 'Relatório'),
        ('presentation', 'Apresentação'),
    )
    
    STATUS = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default='draft')
    file = models.FileField(upload_to='documents/', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class DocumentVersion(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    version = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('document', 'version')
        ordering = ['-version']
```

3. Modelo de Pagamento
```python
# apps/payments/models.py
from django.db import models
from django.conf import settings

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Payment {self.transaction_id}'

class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True)
    
    def __str__(self):
        return self.invoice_number
```

4. Modelo de Notificação
```python
# apps/notifications/models.py
from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = (
        ('info', 'Informação'),
        ('success', 'Sucesso'),
        ('warning', 'Aviso'),
        ('error', 'Erro'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPES, default='info')
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

5. Modelo de Configuração
```python
# apps/core/models.py
from django.db import models
from django.core.cache import cache

class Setting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_public:
            cache.set(f'setting_{self.key}', self.value, timeout=3600)
    
    @classmethod
    def get_value(cls, key):
        cached_value = cache.get(f'setting_{key}')
        if cached_value is not None:
            return cached_value
            
        try:
            setting = cls.objects.get(key=key)
            if setting.is_public:
                cache.set(f'setting_{key}', setting.value, timeout=3600)
            return setting.value
        except cls.DoesNotExist:
            return None
```