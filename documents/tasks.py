from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Document
from .utils import DocumentGenerator
import json


@shared_task
def generate_document_async(document_id, template_id, data, format_type):
    """
    Asynchronous document generation task
    """
    try:
        from .models import Template
        
        template = Template.objects.get(id=template_id)
        generator = DocumentGenerator()
        
        if format_type.lower() == 'pdf':
            file_content = generator.generate_pdf(template, data)
        elif format_type.lower() == 'docx':
            file_content = generator.generate_docx(template, data)
        elif format_type.lower() == 'xlsx':
            file_content = generator.generate_xlsx(template, data)
        else:
            raise ValueError(f'Formato não suportado: {format_type}')
        
        # Update document with generated content
        document = Document.objects.get(id=document_id)
        # Save file content to storage (S3 or local)
        # Implementation depends on storage backend
        
        return {
            'success': True,
            'document_id': document_id,
            'message': 'Documento gerado com sucesso'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@shared_task
def send_document_notification(user_email, document_name):
    """
    Send email notification when document is ready
    """
    try:
        send_mail(
            subject=f'Documento {document_name} está pronto',
            message=f'O seu documento {document_name} foi gerado com sucesso e está disponível para download.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': str(e)}