from django.db import models
from django.conf import settings
import uuid


class Plan(models.Model):
    TYPES = [
        ('free', 'Gratuito'),
        ('basic', 'Básico'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=30)
    currency = models.CharField(max_length=3, default='AOA')
    interval = models.CharField(max_length=20, default='month')
    features = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'{self.name} - {self.price} {self.currency}'


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Ativa'),
        ('PENDING', 'Pendente'),
        ('CANCELLED', 'Cancelada'),
        ('EXPIRED', 'Expirada')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{str(self.user.email)} - {self.plan.name}'


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('PROCESSING', 'Processando'),
        ('COMPLETED', 'Completada'),
        ('FAILED', 'Falha'),
        ('REFUNDED', 'Reembolsada')
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='AOA')
    payment_method = models.CharField(max_length=50)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    gateway_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Transaction {self.id} - {self.amount} {self.currency}'
