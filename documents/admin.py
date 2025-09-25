from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone
from .models import Template, Document


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'price_kz', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at', 'subcategory')
    search_fields = ('name', 'description', 'category', 'subcategory')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['activate_templates', 'deactivate_templates', 'set_price_200', 'set_price_300']
    
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
    
    def price_display(self, obj):
        return format_html('<strong>{} KZ</strong>', obj.price_kz)
    price_display.short_description = 'Preço'
    price_display.admin_order_field = 'price_kz'
    
    def documents_count(self, obj):
        count = obj.document_set.count()
        if count > 0:
            return format_html('<span style="color: green;">{} documento(s)</span>', count)
        return format_html('<span style="color: gray;">0 documentos</span>')
    documents_count.short_description = 'Documentos Gerados'
    
    def activate_templates(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} template(s) ativado(s).')
    activate_templates.short_description = 'Ativar templates'
    
    def deactivate_templates(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} template(s) desativado(s).')
    deactivate_templates.short_description = 'Desativar templates'
    
    def set_price_200(self, request, queryset):
        count = queryset.update(price_kz=200)
        self.message_user(request, f'{count} template(s) com preço definido para 200 KZ.')
    set_price_200.short_description = 'Definir preço para 200 KZ'
    
    def set_price_300(self, request, queryset):
        count = queryset.update(price_kz=300)
        self.message_user(request, f'{count} template(s) com preço definido para 300 KZ.')
    set_price_300.short_description = 'Definir preço para 300 KZ'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'file_type', 'status', 'created_at')
    list_filter = ('file_type', 'status', 'created_at', 'template__category')
    search_fields = ('name', 'user__email', 'user__name', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('user',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['mark_as_completed', 'mark_as_failed', 'reprocess_documents']
    
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
    
    def user_display(self, obj):
        return f'{obj.user.name} ({obj.user.email})'
    user_display.short_description = 'Usuário'
    user_display.admin_order_field = 'user__name'
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue', 
            'completed': 'green',
            'failed': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def file_link(self, obj):
        if obj.file_url:
            return format_html('<a href="{}" target="_blank">📄 Baixar</a>', obj.file_url)
        return '❌ Sem arquivo'
    file_link.short_description = 'Arquivo'
    
    def mark_as_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f'{count} documento(s) marcado(s) como completado(s).')
    mark_as_completed.short_description = 'Marcar como completado'
    
    def mark_as_failed(self, request, queryset):
        count = queryset.update(status='failed')
        self.message_user(request, f'{count} documento(s) marcado(s) como falhados.')
    mark_as_failed.short_description = 'Marcar como falhado'
    
    def reprocess_documents(self, request, queryset):
        count = queryset.update(status='pending')
        self.message_user(request, f'{count} documento(s) marcado(s) para reprocessamento.')
    reprocess_documents.short_description = 'Reprocessar documentos'
