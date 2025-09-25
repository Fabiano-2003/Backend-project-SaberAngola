from .models import Payment, Invoice
from django.utils import timezone
from datetime import timedelta


class PaymentService:
    @staticmethod
    def process_payment(payment):
        """
        Process payment logic with proper error handling
        """
        if payment.status != 'pending':
            raise ValueError(f'Payment {payment.id} is not in pending status')
        
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
                
                # Create invoice only after successful payment
                invoice = PaymentService._create_invoice(payment)
                
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
    
    @staticmethod
    def _create_invoice(payment):
        """
        Create invoice for successful payment
        """
        tax_rate = 0.14  # 14% IVA in Angola
        tax_amount = payment.amount * tax_rate
        total_amount = payment.amount + tax_amount
        
        invoice = Invoice.objects.create(
            user=payment.user,
            payment=payment,
            invoice_number=f'INV-{payment.id:06d}-{timezone.now().strftime("%Y%m%d")}',
            amount=payment.amount,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status='paid',
            due_date=timezone.now().date() + timedelta(days=30)
        )
        
        return invoice