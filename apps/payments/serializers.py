from rest_framework import serializers
from .models import Payment, Invoice
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Payment
        fields = ('id', 'user', 'user_username', 'amount', 'status', 'payment_method', 
                 'transaction_id', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('amount', 'payment_method')


class InvoiceSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    payment_amount = serializers.DecimalField(source='payment.amount', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = Invoice
        fields = ('id', 'user', 'user_username', 'payment', 'payment_amount', 'invoice_number', 
                 'amount', 'tax_amount', 'total_amount', 'status', 'due_date', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class InvoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('payment', 'amount', 'tax_amount', 'due_date')