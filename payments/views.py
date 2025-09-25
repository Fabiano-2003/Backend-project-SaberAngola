from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Plan, Subscription, Transaction
from .serializers import PlanSerializer, SubscriptionSerializer, TransactionSerializer
from .services import PaymentService
import uuid

User = get_user_model()


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = []


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Subscription.objects.none()
        return Subscription.objects.filter(user=self.request.user)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Transaction.objects.none()
        return Transaction.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    plan_id = request.data.get('plan_id')
    payment_method = request.data.get('payment_method', 'multicaixa')
    
    try:
        plan = Plan.objects.get(id=plan_id, is_active=True)
        
        # Check if user already has active subscription
        existing_sub = Subscription.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).first()
        
        if existing_sub:
            return Response({
                'error': 'Já possui uma subscrição ativa'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create subscription
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            status='PENDING'
        )
        
        # Create transaction
        transaction = Transaction.objects.create(
            user=request.user,
            subscription=subscription,
            amount=plan.price,
            payment_method=payment_method.upper(),
            reference=str(uuid.uuid4())[:8].upper(),
            status='PENDING'
        )
        
        # Process payment
        payment_service = PaymentService()
        payment_result = payment_service.process_payment(
            transaction=transaction,
            payment_method=payment_method
        )
        
        return Response({
            'subscription_id': subscription.id,
            'transaction_id': transaction.id,
            'payment_reference': transaction.reference,
            'payment_url': payment_result.get('payment_url'),
            'status': transaction.status
        }, status=status.HTTP_201_CREATED)
        
    except Plan.DoesNotExist:
        return Response({
            'error': 'Plano não encontrado'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([])
def payment_webhook(request):
    # Handle payment gateway webhooks
    payment_service = PaymentService()
    result = payment_service.handle_webhook(request.data)
    
    if result['success']:
        return Response({'status': 'processed'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid webhook'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    subscription = Subscription.objects.filter(
        user=request.user,
        status='ACTIVE'
    ).first()
    
    if subscription:
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
    else:
        return Response({
            'message': 'Nenhuma subscrição ativa encontrada'
        }, status=status.HTTP_404_NOT_FOUND)
