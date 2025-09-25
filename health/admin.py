from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.core.cache import cache
from django.conf import settings
import logging


class SystemStatusAdmin(admin.ModelAdmin):
    """
    Admin personalizado para monitoramento do sistema.
    Não há um modelo específico, mas fornece uma interface para visualizar
    o status do sistema, logs e métricas importantes.
    """
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff


# Registrar uma visualização customizada para monitoramento
class MonitoringProxy(models.Model):
    """Modelo proxy para criar uma seção de monitoramento no admin"""
    
    class Meta:
        managed = False
        verbose_name = "Status do Sistema"
        verbose_name_plural = "Monitoramento do Sistema"
        app_label = 'health'


@admin.register(MonitoringProxy)
class MonitoringAdmin(admin.ModelAdmin):
    """Interface de monitoramento no Django Admin"""
    
    def changelist_view(self, request, extra_context=None):
        # Adicionar contexto personalizado com estatísticas do sistema
        extra_context = extra_context or {}
        
        # Importar modelos aqui para evitar problemas de circular import
        from authentication.models import User
        from documents.models import Document, Template
        from payments.models import Transaction, Subscription
        
        # Estatísticas básicas
        stats = {
            'total_users': User.objects.count(),
            'premium_users': User.objects.filter(is_premium=True).count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'total_documents': Document.objects.count(),
            'pending_documents': Document.objects.filter(status='pending').count(),
            'completed_documents': Document.objects.filter(status='completed').count(),
            'total_templates': Template.objects.count(),
            'active_templates': Template.objects.filter(is_active=True).count(),
            'total_transactions': Transaction.objects.count(),
            'completed_transactions': Transaction.objects.filter(status='COMPLETED').count(),
            'active_subscriptions': Subscription.objects.filter(status='ACTIVE').count(),
        }
        
        extra_context['stats'] = stats
        
        return super().changelist_view(request, extra_context)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


# Personalização do site admin
admin.site.site_header = "SaberAngola - Administração"
admin.site.site_title = "SaberAngola Admin"
admin.site.index_title = "Painel Administrativo"