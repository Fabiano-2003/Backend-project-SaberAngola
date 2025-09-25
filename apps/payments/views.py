from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, APIException
from django.http import Http404
from .models import Payment, Invoice
from .serializers import PaymentSerializer, InvoiceSerializer
from .services import PaymentService

class PaymentRequiredError(APIException):
    status_code = 402
    default_detail = 'Payment Required'
    default_code = 'payment_required'

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        try:
            PaymentService.process_payment(payment)
        except ValueError as e:
            # Business logic errors (400)
            raise ValidationError(str(e))
        except Exception as e:
            # Payment gateway errors (402)
            payment.status = 'failed'
            payment.save()
            raise PaymentRequiredError(f'Payment processing failed: {str(e)}')
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        payment = self.get_object()
        try:
            result = PaymentService.process_payment(payment)
            return Response(
                {
                    'payment': PaymentSerializer(result['payment']).data,
                    'invoice': InvoiceSerializer(result['invoice']).data if 'invoice' in result else None,
                    'status': result['status']
                }
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Payment processing failed: {str(e)}'},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
    
    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        payment = self.get_object()
        try:
            invoice = payment.invoice
            return Response(InvoiceSerializer(invoice).data)
        except Invoice.DoesNotExist:
            return Response(
                {'detail': 'Invoice not found'},
                status=status.HTTP_404_NOT_FOUND
            )