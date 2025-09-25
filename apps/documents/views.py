from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def new_version(self, request, pk=None):
        document = self.get_object()
        
        # Validate input data using serializer
        serializer = DocumentVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get last version with proper ordering
        last_version = document.documentversion_set.order_by('-version').first()
        
        # Create new version
        new_version = serializer.save(
            document=document,
            version=last_version.version + 1 if last_version else 1,
            created_by=request.user
        )
        
        return Response(
            DocumentVersionSerializer(new_version).data,
            status=status.HTTP_201_CREATED
        )