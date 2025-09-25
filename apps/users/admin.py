from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Profile, Activity


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'phone', 'date_of_birth', 'created_at', 'has_profile_picture', 'age_display')
    list_filter = ('created_at', 'date_of_birth')
    search_fields = ('user__email', 'user__name', 'phone', 'bio', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações de Perfil', {
            'fields': ('profile_picture', 'bio', 'phone', 'address', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def user_display(self, obj):
        return f'{obj.user.name} ({obj.user.email})'
    user_display.short_description = 'Usuário'
    user_display.admin_order_field = 'user__name'
    
    def has_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<span style="color: green;">✓ Sim</span>')
        return format_html('<span style="color: red;">✗ Não</span>')
    has_profile_picture.short_description = 'Foto de Perfil'
    
    def age_display(self, obj):
        if obj.date_of_birth:
            today = timezone.now().date()
            age = today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))
            return f'{age} anos'
        return '-'
    age_display.short_description = 'Idade'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'action', 'timestamp', 'details_summary')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'user__name', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    raw_id_fields = ('user',)
    list_per_page = 50
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Ação', {
            'fields': ('user', 'action', 'timestamp')
        }),
        ('Detalhes', {
            'fields': ('details',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def user_display(self, obj):
        return f'{obj.user.name} ({obj.user.email})'
    user_display.short_description = 'Usuário'
    user_display.admin_order_field = 'user__name'
    
    def details_summary(self, obj):
        if obj.details:
            summary = str(obj.details)[:100]
            if len(str(obj.details)) > 100:
                summary += '...'
            return summary
        return '-'
    details_summary.short_description = 'Detalhes'
    
    def has_add_permission(self, request):
        return False  # Activities should be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Activities should be read-only
