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
    content = models.TextField(default='')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='article')
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