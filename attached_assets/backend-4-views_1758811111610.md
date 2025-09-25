# Backend Views

## Implementação das Views

1. Auth Views
```python
# apps/users/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer, RegisterSerializer
from .models import Profile

User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'register':
            return RegisterSerializer
        return UserSerializer
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

2. Document Views
```python
# apps/documents/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def new_version(self, request, pk=None):
        document = self.get_object()
        last_version = document.documentversion_set.first()
        
        new_version = DocumentVersion.objects.create(
            document=document,
            version=last_version.version + 1 if last_version else 1,
            content=request.data.get('content'),
            created_by=request.user
        )
        
        return Response(
            DocumentVersionSerializer(new_version).data,
            status=status.HTTP_201_CREATED
        )
```

3. Payment Views
```python
# apps/payments/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment, Invoice
from .serializers import PaymentSerializer, InvoiceSerializer
from .services import PaymentService

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        PaymentService.process_payment(payment)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        payment = self.get_object()
        PaymentService.process_payment(payment)
        return Response(
            PaymentSerializer(payment).data
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
```

4. Notification Views
```python
# apps/notifications/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(self.get_serializer(notification).data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(read=True)
        return Response({'status': 'success'})
```

5. Settings Views
```python
# apps/core/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Setting
from .serializers import SettingSerializer, PublicSettingSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SettingSerializer
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.AllowAny],
        serializer_class=PublicSettingSerializer
    )
    def public(self, request):
        settings = Setting.objects.filter(is_public=True)
        serializer = self.get_serializer(settings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        settings_data = request.data
        updated = []
        
        for item in settings_data:
            setting = Setting.objects.filter(key=item['key']).first()
            if setting:
                setting.value = item['value']
                setting.save()
                updated.append(setting)
        
        return Response(
            SettingSerializer(updated, many=True).data
        )
```