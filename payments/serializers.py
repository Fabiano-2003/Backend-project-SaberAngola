from rest_framework import serializers
from .models import Plan, Subscription, Transaction


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'price', 'duration_days', 'features', 'is_active')


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_price = serializers.DecimalField(source='plan.price', read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = Subscription
        fields = ('id', 'plan', 'plan_name', 'plan_price', 'status', 'start_date', 'end_date', 'created_at')


class TransactionSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.CharField(source='subscription.plan.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ('id', 'subscription', 'subscription_plan', 'amount', 'payment_method', 
                 'reference', 'status', 'created_at', 'updated_at')