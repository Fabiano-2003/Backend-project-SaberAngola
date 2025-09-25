from django.contrib import admin
from .models import Template, Document


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price_kz', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'category')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'category', 'subcategory')
        }),
        ('Configurações', {
            'fields': ('price_kz', 'is_active')
        }),
        ('Campos do Template', {
            'fields': ('fields',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'file_type', 'status', 'created_at')
    list_filter = ('file_type', 'status', 'created_at', 'template__category')
    search_fields = ('name', 'user__email', 'user__name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('id', 'name', 'user', 'template')
        }),
        ('Configurações', {
            'fields': ('file_type', 'status')
        }),
        ('Dados e Arquivo', {
            'fields': ('data', 'file_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'template')
