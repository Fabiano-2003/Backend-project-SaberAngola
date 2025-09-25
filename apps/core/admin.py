from django.contrib import admin
from django.utils.html import format_html
from .models import Setting

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_preview', 'is_public', 'created_at', 'updated_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('key', 'value', 'description')
    ordering = ('key',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Configuração', {
            'fields': ('key', 'value', 'description')
        }),
        ('Opções', {
            'fields': ('is_public',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def value_preview(self, obj):
        value = str(obj.value)
        if len(value) > 50:
            return f"{value[:50]}..."
        return value
    value_preview.short_description = 'Valor'
    
    def public_display(self, obj):
        if obj.is_public:
            return format_html('<span style="color: green;">✓ Público</span>')
        return format_html('<span style="color: orange;">◐ Privado</span>')
    public_display.short_description = 'Visibilidade'