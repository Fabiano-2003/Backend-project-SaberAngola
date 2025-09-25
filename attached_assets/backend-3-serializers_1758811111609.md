# Backend Serializers

## Implementação dos Serializers

1. User Serializers
```python
# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_verified')
        read_only_fields = ('id', 'is_verified')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'avatar', 'bio', 'location', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user
```

2. Document Serializers
```python
# apps/documents/serializers.py
from rest_framework import serializers
from .models import Document, DocumentVersion

class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    
    class Meta:
        model = DocumentVersion
        fields = ('id', 'version', 'content', 'created_at', 'created_by')
        read_only_fields = ('id', 'version', 'created_at', 'created_by')

class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    versions = DocumentVersionSerializer(many=True, read_only=True, source='documentversion_set')
    
    class Meta:
        model = Document
        fields = (
            'id', 'title', 'description', 'content', 'document_type',
            'status', 'file', 'owner', 'versions', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'owner', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        user = self.context['request'].user
        document = Document.objects.create(owner=user, **validated_data)
        DocumentVersion.objects.create(
            document=document,
            version=1,
            content=validated_data['content'],
            created_by=user
        )
        return document
```

3. Payment Serializers
```python
# apps/payments/serializers.py
from rest_framework import serializers
from .models import Payment, Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            'id', 'invoice_number', 'due_date', 'paid_date',
            'pdf_file'
        )
        read_only_fields = ('id', 'invoice_number', 'pdf_file')

class PaymentSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer(read_only=True)
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Payment
        fields = (
            'id', 'user', 'amount', 'status', 'payment_method',
            'transaction_id', 'invoice', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'transaction_id',
            'created_at', 'updated_at'
        )
```

4. Notification Serializers
```python
# apps/notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'title', 'message', 'notification_type',
            'read', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Notification.objects.create(user=user, **validated_data)
```

5. Setting Serializers
```python
# apps/core/serializers.py
from rest_framework import serializers
from .models import Setting

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = (
            'id', 'key', 'value', 'description',
            'is_public', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_key(self, value):
        if ' ' in value:
            raise serializers.ValidationError(
                "Key cannot contain spaces"
            )
        return value.lower()

class PublicSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ('key', 'value')
        read_only_fields = ('key', 'value')
```