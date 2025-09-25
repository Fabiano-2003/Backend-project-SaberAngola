from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.PlanListView.as_view(), name='plan-list'),
    path('subscriptions/', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('subscribe/', views.create_subscription, name='create-subscription'),
    path('webhook/', views.payment_webhook, name='payment-webhook'),
    path('status/', views.subscription_status, name='subscription-status'),
]