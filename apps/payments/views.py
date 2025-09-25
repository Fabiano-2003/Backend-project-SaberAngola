from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Payment, Invoice

# Placeholder views - will be implemented according to backend-4-views.md
User = get_user_model()

class PlanListView(generics.GenericAPIView):
    def get(self, request):
        return Response({'message': 'Plan list view placeholder'})

class SubscriptionListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Subscription list view placeholder'})

class TransactionListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Transaction list view placeholder'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    return Response({'message': 'Create subscription placeholder'})

@api_view(['POST'])
@permission_classes([])
def payment_webhook(request):
    return Response({'message': 'Payment webhook placeholder'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    return Response({'message': 'Subscription status placeholder'})