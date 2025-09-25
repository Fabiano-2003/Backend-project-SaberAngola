from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = ('id', 'user', 'user_username', 'title', 'message', 'notification_type', 
                 'is_read', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('user', 'title', 'message', 'notification_type')


class NotificationSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'title', 'notification_type', 'is_read', 'created_at')