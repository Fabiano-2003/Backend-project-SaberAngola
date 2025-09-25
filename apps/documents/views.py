from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Document, DocumentVersion

# Placeholder views - will be implemented according to backend-4-views.md
User = get_user_model()

class DocumentListCreateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Document list view placeholder'})

class DocumentDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        return Response({'message': 'Document detail view placeholder'})

class TemplateListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Template list view placeholder'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_document(request):
    return Response({'message': 'Generate document placeholder'})