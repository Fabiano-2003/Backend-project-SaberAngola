from rest_framework import serializers
from .models import Document, DocumentVersion
from django.contrib.auth import get_user_model

User = get_user_model()


class DocumentSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    
    class Meta:
        model = Document
        fields = ('id', 'title', 'description', 'content', 'document_type', 'status', 
                 'file', 'owner', 'owner_username', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('title', 'description', 'content', 'document_type', 'file')


class DocumentVersionSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source='document.title', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = DocumentVersion
        fields = ('id', 'document', 'document_title', 'version', 'content', 
                 'created_at', 'created_by', 'created_by_username')
        read_only_fields = ('id', 'created_at')


class DocumentSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'document_type', 'status', 'created_at', 'updated_at')