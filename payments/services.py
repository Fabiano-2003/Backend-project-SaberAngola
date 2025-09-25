import requests
import json
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Transaction, Subscription


class PaymentService:
    def __init__(self):
        self.multicaixa_api_url = getattr(settings, 'MULTICAIXA_API_URL', '')
        self.emis_api_url = getattr(settings, 'EMIS_API_URL', '')
    
    def process_payment(self, transaction, payment_method):
        if payment_method.lower() == 'multicaixa':
            return self._process_multicaixa_payment(transaction)
        elif payment_method.lower() == 'emis':
            return self._process_emis_payment(transaction)
        else:
            raise ValueError(f'Método de pagamento não suportado: {payment_method}')
    
    def _process_multicaixa_payment(self, transaction):
        # Implementação do Multicaixa Express
        # Esta é uma implementação simples - ajustar conforme API oficial
        
        payload = {
            'amount': float(transaction.amount),
            'reference': transaction.reference,
            'description': f'Subscrição {transaction.subscription.plan.name}',
            'callback_url': f'{settings.DOMAIN}/api/payments/webhook/'
        }
        
        try:
            # Simular resposta do Multicaixa para desenvolvimento
            # Em produção, fazer requisição real para API
            if settings.DEBUG:
                return {
                    'success': True,
                    'payment_url': f'https://multicaixa.ao/pay/{transaction.reference}',
                    'reference': transaction.reference
                }
            
            # Código real para produção
            # response = requests.post(self.multicaixa_api_url, json=payload)
            # return response.json()
            
        except Exception as e:
            transaction.status = 'FAILED'
            transaction.save()
            raise e
    
    def _process_emis_payment(self, transaction):
        # Implementação do EMIS
        # Ajustar conforme API oficial do EMIS
        
        payload = {
            'amount': float(transaction.amount),
            'reference': transaction.reference,
            'description': f'Subscrição {transaction.subscription.plan.name}',
            'callback_url': f'{settings.DOMAIN}/api/payments/webhook/'
        }
        
        try:
            # Simular resposta do EMIS para desenvolvimento
            if settings.DEBUG:
                return {
                    'success': True,
                    'payment_url': f'https://emis.ao/pay/{transaction.reference}',
                    'reference': transaction.reference
                }
            
            # Código real para produção
            # response = requests.post(self.emis_api_url, json=payload)
            # return response.json()
            
        except Exception as e:
            transaction.status = 'FAILED'
            transaction.save()
            raise e
    
    def handle_webhook(self, data):
        try:
            reference = data.get('reference')
            status = data.get('status')
            
            if not reference or not status:
                return {'success': False, 'error': 'Dados incompletos'}
            
            transaction = Transaction.objects.get(reference=reference)
            
            if status.upper() == 'COMPLETED':
                transaction.status = 'COMPLETED'
                # Ativar subscrição
                subscription = transaction.subscription
                subscription.status = 'ACTIVE'
                subscription.start_date = timezone.now()
                subscription.end_date = subscription.start_date + timedelta(days=subscription.plan.duration_days)
                subscription.save()
                
                # Atualizar status premium do usuário
                user = transaction.user
                user.is_premium = True
                user.save()
                
            elif status.upper() == 'FAILED':
                transaction.status = 'FAILED'
                subscription = transaction.subscription
                subscription.status = 'CANCELLED'
                subscription.save()
            
            transaction.save()
            return {'success': True}
            
        except Transaction.DoesNotExist:
            return {'success': False, 'error': 'Transação não encontrada'}
        except Exception as e:
            return {'success': False, 'error': str(e)}