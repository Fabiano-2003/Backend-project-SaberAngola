from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Document, Template
from .serializers import DocumentSerializer, TemplateSerializer
from .utils import DocumentGenerator
import json

User = get_user_model()


class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Document.objects.none()
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Document.objects.none()
        return Document.objects.filter(user=self.request.user)


class TemplateListView(generics.ListAPIView):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_document(request):
    template_id = request.data.get('template_id')
    format_type = request.data.get('format', 'pdf')
    data = request.data.get('data', {})
    
    try:
        template = Template.objects.get(id=template_id, is_active=True)
        generator = DocumentGenerator()
        
        if format_type.lower() == 'pdf':
            file_content = generator.generate_pdf(template, data)
            content_type = 'application/pdf'
            filename = f'{template.name}.pdf'
        elif format_type.lower() == 'docx':
            file_content = generator.generate_docx(template, data)
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            filename = f'{template.name}.docx'
        elif format_type.lower() == 'xlsx':
            file_content = generator.generate_xlsx(template, data)
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            filename = f'{template.name}.xlsx'
        else:
            return Response({'error': 'Formato não suportado'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save document record
        document = Document.objects.create(
            user=request.user,
            template=template,
            name=f"{template.name} - {format_type.upper()}",
            file_type=format_type.upper(),
            data=json.dumps(data)
        )
        
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
        
    except Template.DoesNotExist:
        return Response({'error': 'Template não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
