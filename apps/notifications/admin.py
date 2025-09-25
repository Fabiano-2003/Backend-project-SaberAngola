from django.contrib import admin
from django.utils.html import format_html
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'notification_type', 'read', 'created_at')
    list_filter = ('notification_type', 'read', 'created_at')
    search_fields = ('title', 'message', 'user__email', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Notificação', {
            'fields': ('user', 'title', 'message')
        }),
        ('Configurações', {
            'fields': ('notification_type', 'read')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def type_display(self, obj):
        colors = {
            'info': 'blue',
            'success': 'green',
            'warning': 'orange',
            'error': 'red'
        }
        color = colors.get(obj.notification_type, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_notification_type_display())
    type_display.short_description = 'Tipo'