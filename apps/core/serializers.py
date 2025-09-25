from rest_framework import serializers
from .models import Setting


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('id', 'key', 'value', 'value_type', 'description', 'is_public', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class SettingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value', 'value_type', 'description', 'is_public')


class PublicSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value', 'value_type', 'description')