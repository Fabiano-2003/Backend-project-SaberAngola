import uuid
from decimal import Decimal
from django.conf import settings
from .models import Payment, Invoice
from datetime import datetime, timedelta
from django.utils import timezone


class PaymentService:
    @staticmethod
    def generate_transaction_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_invoice_number():
        prefix = timezone.now().strftime('%Y%m')
        count = Invoice.objects.filter(
            invoice_number__startswith=prefix
        ).count()
        return f"{prefix}-{str(count + 1).zfill(4)}"
    
    @staticmethod
    def process_payment(payment: Payment):
        if payment.status != 'pending':
            return
        
        try:
            # Update status to processing
            payment.status = 'processing'
            payment.save()
            
            # Simulate payment gateway integration
            # In real implementation, this would call external gateway
            success = PaymentService._simulate_gateway_call(payment)
            
            if success:
                # Payment successful
                payment.status = 'completed'
                payment.save()
                
                # Create invoice
                due_date = timezone.now().date() + timedelta(days=30)
                invoice = Invoice.objects.create(
                    user=payment.user,
                    payment=payment,
                    invoice_number=PaymentService.generate_invoice_number(),
                    amount=payment.amount,
                    tax_amount=payment.amount * Decimal('0.14'),  # 14% IVA
                    total_amount=payment.amount * Decimal('1.14'),
                    status='paid',
                    due_date=due_date
                )
                
                return {'status': 'success', 'payment': payment, 'invoice': invoice}
            else:
                # Payment failed
                payment.status = 'failed'
                payment.save()
                raise Exception('Payment gateway rejected the transaction')
                
        except Exception as e:
            # Ensure payment status is set to failed on any error
            payment.status = 'failed'
            payment.save()
            raise e
    
    @staticmethod
    def _simulate_gateway_call(payment):
        """
        Simulate external payment gateway call
        In production, replace with actual gateway integration
        """
        # Simulate 95% success rate for demo purposes
        import random
        return random.random() < 0.95