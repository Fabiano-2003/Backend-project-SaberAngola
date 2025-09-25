from rest_framework import serializers
from .models import Document, Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'description', 'category', 'fields', 'is_active', 'created_at')


class DocumentSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = Document
        fields = ('id', 'name', 'template', 'template_name', 'file_type', 'data', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')