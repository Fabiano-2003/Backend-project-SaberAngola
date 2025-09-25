from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from datetime import datetime, timedelta

User = get_user_model()

class AuthService:
    @staticmethod
    def generate_verification_token(user):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, settings.SECRET_KEY, algorithm='HS256')
        
        user.verification_token = token
        user.save()
        return token
    
    @staticmethod
    def verify_email(token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user = User.objects.get(id=payload['user_id'])
            user.is_verified = True
            user.verification_token = ''
            user.save()
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            return False
    
    @staticmethod
    def send_verification_email(user):
        token = AuthService.generate_verification_token(user)
        context = {
            'user': user,
            'verify_url': f"{settings.FRONTEND_URL}/verify-email?token={token}"
        }
        
        html_message = render_to_string(
            'email/verify_email.html',
            context
        )
        
        send_mail(
            subject='Verifique seu email - SaberAngola',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message
        )