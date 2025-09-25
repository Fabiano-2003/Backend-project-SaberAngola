from django.contrib import admin
from .models import Plan, Subscription, Transaction


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'currency', 'duration_days', 'is_active')
    list_filter = ('type', 'is_active', 'currency')
    search_fields = ('name', 'description')
    ordering = ('type', 'price')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Informações do Plano', {
            'fields': ('name', 'description', 'type')
        }),
        ('Preço e Duração', {
            'fields': ('price', 'currency', 'duration_days', 'interval')
        }),
        ('Funcionalidades', {
            'fields': ('features',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew')
    list_filter = ('status', 'auto_renew', 'plan__type', 'created_at')
    search_fields = ('user__email', 'user__name', 'plan__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Subscrição', {
            'fields': ('user', 'plan', 'status')
        }),
        ('Período', {
            'fields': ('start_date', 'end_date', 'auto_renew')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'currency', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'currency', 'created_at')
    search_fields = ('user__email', 'user__name', 'reference', 'gateway_reference')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'subscription')
    
    fieldsets = (
        ('Transação', {
            'fields': ('id', 'user', 'subscription', 'status')
        }),
        ('Valores', {
            'fields': ('amount', 'currency', 'payment_method')
        }),
        ('Referências', {
            'fields': ('reference', 'gateway_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'subscription', 'subscription__plan')
