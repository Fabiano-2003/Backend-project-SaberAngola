from django.contrib import admin
from django.utils.html import format_html
from .models import Payment, Invoice

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'user__email', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Informações do Pagamento', {
            'fields': ('user', 'amount', 'payment_method')
        }),
        ('Status e Referência', {
            'fields': ('status', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def status_display(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'purple'
        }
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())
    status_display.short_description = 'Status'

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'payment', 'due_date', 'paid_date', 'has_pdf')
    list_filter = ('due_date', 'paid_date')
    search_fields = ('invoice_number', 'payment__transaction_id', 'payment__user__email')
    ordering = ('-due_date',)
    raw_id_fields = ('payment',)
    
    fieldsets = (
        ('Fatura', {
            'fields': ('payment', 'invoice_number')
        }),
        ('Datas', {
            'fields': ('due_date', 'paid_date')
        }),
        ('Arquivo', {
            'fields': ('pdf_file',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('payment', 'payment__user')
    
    def has_pdf(self, obj):
        if obj.pdf_file:
            return format_html('<span style="color: green;">✓ Sim</span>')
        return format_html('<span style="color: red;">✗ Não</span>')
    has_pdf.short_description = 'PDF'