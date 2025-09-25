from django.db import models
from django.conf import settings
import uuid


class Template(models.Model):
    CATEGORIES = [
        # Declarações
        ('declaracao_simples', 'Declaração Simples'),
        ('declaracao_laboral', 'Declaração Laboral/Financeira'),
        ('declaracao_complexa', 'Declaração Complexa'),
        
        # Contratos
        ('contrato_simples', 'Contrato Simples'),
        ('contrato_servicos', 'Contrato de Prestação de Serviços'),
        ('contrato_complexo', 'Contrato Complexo'),
        
        # Faturas
        ('fatura_simples', 'Fatura Simples'),
        ('fatura_comercial', 'Fatura Comercial'),
        ('documento_auxiliar', 'Documento Auxiliar'),
        
        # Currículos
        ('cv_basico', 'CV Básico'),
        ('cv_profissional', 'CV Profissional'),
        ('cv_multilingue', 'CV Multilíngue'),
        
        # Categorias antigas (manter compatibilidade)
        ('contract', 'Contrato'),
        ('invoice', 'Factura'),
        ('report', 'Relatório'),
        ('certificate', 'Certificado'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    subcategory = models.CharField(max_length=100, blank=True, default='')  # Para especificar tipo específico dentro da categoria
    price_kz = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Preço em Kwanzas
    fields = models.JSONField(default=dict)  # Template field definitions
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return str(self.name)


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
        
    def __str__(self) -> str:
        return str(self.name)
