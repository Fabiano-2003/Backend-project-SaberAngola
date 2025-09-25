from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_staff', 'is_premium', 'is_active', 'created_at', 'last_login_display', 'premium_status')
    list_filter = ('is_staff', 'is_premium', 'is_active', 'created_at', 'last_login', 'updated_at')
    search_fields = ('email', 'name', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['make_premium', 'remove_premium', 'activate_users', 'deactivate_users']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('name',)}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_premium', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    
    filter_horizontal = ('groups', 'user_permissions')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields
    
    def last_login_display(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%d/%m/%Y %H:%M')
        return 'Nunca'
    last_login_display.short_description = 'Último Login'
    last_login_display.admin_order_field = 'last_login'
    
    def premium_status(self, obj):
        if obj.is_premium:
            return format_html('<span style="color: gold;">✓ Premium</span>')
        return format_html('<span style="color: gray;">✗ Gratuito</span>')
    premium_status.short_description = 'Status Premium'
    premium_status.admin_order_field = 'is_premium'
    
    def make_premium(self, request, queryset):
        count = queryset.update(is_premium=True)
        self.message_user(request, f'{count} usuário(s) marcado(s) como premium.')
    make_premium.short_description = 'Marcar como Premium'
    
    def remove_premium(self, request, queryset):
        count = queryset.update(is_premium=False)
        self.message_user(request, f'{count} usuário(s) removido(s) do premium.')
    remove_premium.short_description = 'Remover Premium'
    
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} usuário(s) ativado(s).')
    activate_users.short_description = 'Ativar usuários'
    
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} usuário(s) desativado(s).')
    deactivate_users.short_description = 'Desativar usuários'
