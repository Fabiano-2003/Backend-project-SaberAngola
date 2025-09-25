# Geração e Download de Documentos - SaberAngola

Este documento detalha o processo completo de geração e download de documentos na plataforma SaberAngola, incluindo fluxos, bibliotecas, configurações e exemplos de implementação.

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Bibliotecas e Dependências](#2-bibliotecas-e-dependências)
3. [Tipos de Documentos Suportados](#3-tipos-de-documentos-suportados)
4. [Fluxo de Geração de Documentos](#4-fluxo-de-geração-de-documentos)
5. [Implementação Backend](#5-implementação-backend)
6. [Integração Frontend](#6-integração-frontend)
7. [Armazenamento S3](#7-armazenamento-s3)
8. [Processamento Assíncrono](#8-processamento-assíncrono)
9. [Boas Práticas e Segurança](#9-boas-práticas-e-segurança)
10. [Exemplos de Código](#10-exemplos-de-código)

## 1. Visão Geral

O sistema de geração de documentos do SaberAngola permite criar diferentes tipos de documentos (PDF, Word, Excel) a partir de templates e dados fornecidos pelos usuários. Os documentos são gerados no backend, armazenados no S3 e disponibilizados para download via URLs assinadas.

### 1.1. Características Principais

- Geração dinâmica de documentos
- Múltiplos formatos suportados
- Processamento assíncrono para documentos grandes
- Armazenamento seguro no S3
- URLs de download com tempo limitado
- Suporte a templates personalizados

## 2. Bibliotecas e Dependências

### 2.1. Backend (Python)

```python
# requirements.txt
python-docx==0.8.11    # Documentos Word
reportlab==4.0.4       # PDFs
openpyxl==3.1.2       # Planilhas Excel
pypandoc==1.11        # Conversão entre formatos
boto3==1.28.36        # Integração com AWS S3
celery==5.3.4         # Processamento assíncrono
redis==5.0.1          # Backend Celery
```

### 2.2. Configuração Django

```python
# settings.py
INSTALLED_APPS = [
    ...
    'documents',
]

# Configuração S3
AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_key'
AWS_STORAGE_BUCKET_NAME = 'saberangola-documents'
AWS_S3_REGION_NAME = 'af-south-1'  # África do Sul
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
```

## 3. Tipos de Documentos Suportados

### 3.1. Formatos de Saída

- PDF (`.pdf`)
  - Relatórios
  - Certificados
  - Documentos formatados

- Word (`.docx`)
  - Templates editáveis
  - Documentos acadêmicos
  - Propostas

- Excel (`.xlsx`)
  - Planilhas de orçamento
  - Análises de dados
  - Relatórios financeiros

### 3.2. Templates

- Templates base armazenados no S3
- Suporte a variáveis dinâmicas
- Seções condicionais
- Tabelas e gráficos dinâmicos

## 4. Fluxo de Geração de Documentos

1. **Requisição do Usuário**
   - Frontend envia dados via API
   - Especifica tipo de documento e template

2. **Validação e Processamento**
   - Validação dos dados de entrada
   - Seleção do template apropriado
   - Início do processamento (síncrono/assíncrono)

3. **Geração do Documento**
   - Aplicação dos dados ao template
   - Renderização do documento
   - Conversão para formato final

4. **Armazenamento**
   - Upload para S3
   - Geração de URL assinada
   - Registro no banco de dados

5. **Resposta ao Usuário**
   - URL de download
   - Metadados do documento
   - Status de processamento

## 5. Implementação Backend

### 5.1. Modelos Django

```python
# documents/models.py
from django.db import models

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word'),
        ('xlsx', 'Excel'),
    ]
    
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=DOCUMENT_TYPES)
    file_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='processing')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
```

### 5.2. Serviço de Geração

```python
# documents/services.py
from .generators import PDFGenerator, WordGenerator, ExcelGenerator

class DocumentGenerationService:
    def __init__(self, document_type):
        self.generators = {
            'pdf': PDFGenerator(),
            'docx': WordGenerator(),
            'xlsx': ExcelGenerator()
        }
        self.generator = self.generators[document_type]
    
    def generate(self, template_data):
        document = self.generator.create(template_data)
        url = self._upload_to_s3(document)
        return url
    
    def _upload_to_s3(self, document):
        # Implementação do upload para S3
        pass
```

### 5.3. Views e Endpoints

```python
# documents/views.py
from rest_framework import viewsets
from .tasks import generate_document_task

class DocumentViewSet(viewsets.ModelViewSet):
    def create(self, request):
        data = request.data
        if data.get('is_async'):
            task = generate_document_task.delay(data)
            return Response({'task_id': task.id})
        
        service = DocumentGenerationService(data['type'])
        url = service.generate(data)
        return Response({'download_url': url})
```

## 6. Integração Frontend

### 6.1. Componente React

```typescript
// components/DocumentGenerator.tsx
import { useState } from 'react'
import axios from 'axios'

export const DocumentGenerator = () => {
  const [loading, setLoading] = useState(false)
  
  const generateDocument = async (data) => {
    setLoading(true)
    try {
      const response = await axios.post('/api/documents/', data)
      window.location.href = response.data.download_url
    } catch (error) {
      console.error('Erro na geração:', error)
    }
    setLoading(false)
  }
  
  return (
    // Interface do usuário
  )
}
```

### 6.2. Monitoramento de Progresso

```typescript
// hooks/useDocumentProgress.ts
export const useDocumentProgress = (taskId: string) => {
  const [progress, setProgress] = useState(0)
  
  useEffect(() => {
    const checkProgress = async () => {
      const status = await axios.get(`/api/documents/tasks/${taskId}`)
      setProgress(status.data.progress)
    }
    
    const interval = setInterval(checkProgress, 2000)
    return () => clearInterval(interval)
  }, [taskId])
  
  return progress
}
```

## 7. Armazenamento S3

### 7.1. Configuração do Bucket

- Bucket privado
- Lifecycle rules para documentos antigos
- CORS configurado para o frontend
- Encryption em repouso

### 7.2. URLs Assinadas

```python
# documents/utils.py
import boto3
from botocore.config import Config

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client(
        's3',
        config=Config(signature_version='s3v4')
    )
    
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        },
        ExpiresIn=expiration
    )
    
    return url
```

## 8. Processamento Assíncrono

### 8.1. Tarefas Celery

```python
# documents/tasks.py
from celery import shared_task
from .services import DocumentGenerationService

@shared_task
def generate_document_task(data):
    service = DocumentGenerationService(data['type'])
    url = service.generate(data)
    
    # Atualizar status no banco de dados
    document = Document.objects.get(id=data['document_id'])
    document.file_url = url
    document.status = 'completed'
    document.save()
    
    return url
```

### 8.2. Configuração Celery

```python
# celery.py
from celery import Celery

app = Celery('saberangola')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Africa/Luanda',
    enable_utc=True,
)
```

## 9. Boas Práticas e Segurança

### 9.1. Validação de Entrada

- Validar tipos de arquivo permitidos
- Limitar tamanho dos documentos
- Sanitizar dados de entrada
- Verificar permissões do usuário

### 9.2. Segurança

- URLs assinadas com tempo limitado
- Verificação de autorização
- Logs de acesso e geração
- Backup regular dos templates

### 9.3. Performance

- Cache de templates frequentes
- Processamento em background
- Compressão de arquivos grandes
- Otimização de imagens

## 10. Exemplos de Código

### 10.1. Gerador PDF

```python
# documents/generators/pdf.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class PDFGenerator:
    def create(self, data):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        
        # Adicionar conteúdo
        p.drawString(100, 100, data['title'])
        # ... mais conteúdo
        
        p.showPage()
        p.save()
        
        return buffer.getvalue()
```

### 10.2. Gerador Word

```python
# documents/generators/word.py
from docx import Document
from docx.shared import Inches

class WordGenerator:
    def create(self, data):
        doc = Document()
        doc.add_heading(data['title'], 0)
        
        # Adicionar conteúdo
        doc.add_paragraph(data['content'])
        
        buffer = BytesIO()
        doc.save(buffer)
        return buffer.getvalue()
```

### 10.3. Hook de Sucesso Frontend

```typescript
// hooks/useDocumentGeneration.ts
const useDocumentGeneration = () => {
  const onSuccess = (url: string) => {
    // Abrir em nova aba ou iniciar download
    window.open(url, '_blank')
    
    // Atualizar lista de documentos
    queryClient.invalidateQueries('documents')
    
    // Notificar usuário
    toast.success('Documento gerado com sucesso!')
  }
  
  return { onSuccess }
}
```

## Conclusão

O sistema de geração de documentos do SaberAngola é projetado para ser:

- **Escalável:** Processamento assíncrono para grandes volumes
- **Flexível:** Suporte a múltiplos formatos e templates
- **Seguro:** Armazenamento seguro e URLs assinadas
- **Eficiente:** Cache e otimizações de performance
- **Confiável:** Logs, monitoramento e backups

Para mais informações sobre implementações específicas ou casos de uso, consulte a documentação da API ou entre em contato com a equipe de desenvolvimento.