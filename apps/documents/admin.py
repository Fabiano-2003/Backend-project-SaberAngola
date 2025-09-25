from django.contrib import admin
from django.utils.html import format_html
from .models import Document, DocumentVersion

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'document_type', 'status', 'created_at')
    list_filter = ('document_type', 'status', 'created_at')
    search_fields = ('title', 'owner__email', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('owner',)
    
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('title', 'description', 'owner')
        }),
        ('Conteúdo', {
            'fields': ('content', 'document_type', 'status', 'file')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('document__title', 'created_by__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('document', 'created_by')
    
    fieldsets = (
        ('Versão', {
            'fields': ('document', 'version', 'created_by')
        }),
        ('Conteúdo', {
            'fields': ('content',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('document', 'created_by')