from django.db import models
from django.conf import settings
import uuid


class Template(models.Model):
    CATEGORIES = [
        ('contract', 'Contrato'),
        ('invoice', 'Factura'),
        ('report', 'Relatório'),
        ('certificate', 'Certificado'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    fields = models.JSONField(default=dict)  # Template field definitions
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('xlsx', 'Excel'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Completado'),
        ('failed', 'Falha'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    template = models.ForeignKey(Template, on_delete=models.PROTECT, null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    data = models.JSONField(default=dict)  # Template data used for generation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    file_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.name
