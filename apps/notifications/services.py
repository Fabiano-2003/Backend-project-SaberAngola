from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Notification

class NotificationService:
    @staticmethod
    def create_notification(user, title, message, notification_type='info'):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type
        )
    
    @staticmethod
    def get_unread_count(user):
        return Notification.objects.filter(
            user=user,
            read=False
        ).count()
    
    @staticmethod
    def clean_old_notifications(days=30):
        cutoff_date = timezone.now() - timedelta(days=days)
        Notification.objects.filter(
            Q(created_at__lt=cutoff_date),
            Q(read=True) | Q(notification_type='info')
        ).delete()