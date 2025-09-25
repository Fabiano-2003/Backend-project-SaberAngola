# Estrutura Detalhada do Backend - SaberAngola

## Índice

1. [Visão Geral](#1-visão-geral)
2. [Estrutura do Projeto](#2-estrutura-do-projeto)
3. [Apps Django](#3-apps-django)
4. [Modelos de Dados](#4-modelos-de-dados)
5. [APIs e Views](#5-apis-e-views)
6. [Serializadores](#6-serializadores)
7. [Serviços](#7-serviços)
8. [Configurações](#8-configurações)
9. [Utilitários](#9-utilitários)
10. [Tarefas Assíncronas](#10-tarefas-assíncronas)

## 1. Visão Geral

O backend do SaberAngola é construído com Django + Django REST Framework (DRF), seguindo as melhores práticas de desenvolvimento Python e padrões REST.

### 1.1. Tecnologias Principais

- **Django**: Framework web
- **Django REST Framework**: APIs REST
- **SimpleJWT**: Autenticação JWT
- **Celery**: Tarefas assíncronas
- **Redis**: Cache e broker de mensagens
- **PostgreSQL**: Banco de dados principal
- **Amazon S3**: Armazenamento de arquivos

### 1.2. Arquitetura

```plaintext
[Cliente] → [Nginx] → [Gunicorn] → [Django App] → [PostgreSQL/Redis/S3]
```

## 2. Estrutura do Projeto

```plaintext
backend/
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
├── saberangola/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── auth/
│   ├── users/
│   ├── documents/
│   └── payments/
├── core/
│   ├── models.py
│   ├── managers.py
│   └── utils.py
└── tests/
    ├── conftest.py
    └── test_*.py
```

## 3. Apps Django

### 3.1. Auth App (apps/auth/)

```plaintext
auth/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
├── permissions.py
└── tests/
```

#### 3.1.1. Funcionalidades

- Registro de usuário
- Login/Logout
- Recuperação de senha
- Refresh de token JWT
- Permissões customizadas

#### 3.1.2. Models

```python
class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3.2. Users App (apps/users/)

```plaintext
users/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
└── tests/
```

#### 3.2.1. Funcionalidades

- Perfis de usuário
- Preferências
- Histórico de atividades
- Gestão de conta

#### 3.2.2. Models

```python
class Profile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

class Activity(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
```

### 3.3. Documents App (apps/documents/)

```plaintext
documents/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
├── services/
│   ├── __init__.py
│   ├── generator.py
│   ├── converter.py
│   └── storage.py
└── tests/
```

#### 3.3.1. Funcionalidades

- Geração de documentos
- Conversão entre formatos
- Upload/Download
- Histórico de documentos
- Templates

#### 3.3.2. Models

```python
class Document(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10)  # pdf, docx, xlsx
    status = models.CharField(max_length=20)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Template(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    content = models.TextField()
    is_premium = models.BooleanField(default=False)
```

### 3.4. Payments App (apps/payments/)

```plaintext
payments/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── urls.py
├── views.py
├── services/
│   ├── __init__.py
│   ├── emis.py
│   ├── unitel.py
│   └── africell.py
└── tests/
```

#### 3.4.1. Funcionalidades

- Planos e subscrições
- Processamento de pagamentos
- Webhooks de gateways
- Faturas e recibos

#### 3.4.2. Models

```python
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    features = models.JSONField()

class Subscription(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Transaction(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    gateway = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 4. Modelos de Dados

### 4.1. Relacionamentos entre Models

```plaintext
UserAccount
  ↓
  ├──→ Profile (1:1)
  ├──→ Document (1:N)
  ├──→ Subscription (1:N)
  └──→ Transaction (1:N)

Plan
  ↓
  └──→ Subscription (1:N)

Template
  ↓
  └──→ Document (1:N)
```

### 4.2. Migrations

```plaintext
migrations/
├── auth/
│   ├── 0001_initial.py
│   └── ...
├── users/
│   ├── 0001_initial.py
│   └── ...
├── documents/
│   ├── 0001_initial.py
│   └── ...
└── payments/
    ├── 0001_initial.py
    └── ...
```

## 5. APIs e Views

### 5.1. Auth Views

```python
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
```

### 5.2. Document Views

```python
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        document = self.get_object()
        task = generate_document.delay(document.id)
        return Response({'task_id': task.id})
```

### 5.3. Payment Views

```python
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan = get_object_or_404(Plan, id=request.data['plan_id'])
        payment = create_payment(request.user, plan)
        return Response(payment.to_dict())

class WebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        handle_webhook.delay(request.data)
        return Response({'status': 'received'})
```

## 6. Serializadores

### 6.1. User Serializers

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'is_premium']
        read_only_fields = ['is_premium']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio', 'phone', 'address']
```

### 6.2. Document Serializers

```python
class DocumentSerializer(serializers.ModelSerializer):
    download_url = serializers.URLField(read_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'type', 'status', 'file_url', 
                 'download_url', 'created_at']
        read_only_fields = ['status', 'file_url', 'download_url']
```

## 7. Serviços

### 7.1. Document Generation

```python
class DocumentGenerator:
    def generate_pdf(self, data):
        # Usar reportlab para gerar PDF
        pass
        
    def generate_docx(self, data):
        # Usar python-docx para gerar DOCX
        pass
        
    def generate_xlsx(self, data):
        # Usar openpyxl para gerar XLSX
        pass
```

### 7.2. Payment Processing

```python
class PaymentProcessor:
    def create_payment(self, user, plan):
        # Criar pagamento no gateway
        pass
        
    def process_webhook(self, data):
        # Processar callback do gateway
        pass
```

## 8. Configurações

### 8.1. Base Settings

```python
# settings/base.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'corsheaders',
    'storages',
    
    # Local
    'apps.auth',
    'apps.users',
    'apps.documents',
    'apps.payments',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# AWS Settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
```

### 8.2. Celery Settings

```python
# celery.py

app = Celery('saberangola')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Task routes
app.conf.task_routes = {
    'apps.documents.tasks.generate_document': {'queue': 'documents'},
    'apps.payments.tasks.process_payment': {'queue': 'payments'},
}
```

## 9. Utilitários

### 9.1. Custom Managers

```python
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
```

### 9.2. Custom Permissions

```python
class IsPremiumUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_premium
```

## 10. Tarefas Assíncronas

### 10.1. Document Tasks

```python
@shared_task(bind=True)
def generate_document(self, document_id):
    document = Document.objects.get(id=document_id)
    generator = DocumentGenerator()
    
    try:
        file_url = generator.generate(document.type, document.data)
        document.file_url = file_url
        document.status = 'completed'
        document.save()
    except Exception as e:
        document.status = 'failed'
        document.save()
        raise self.retry(exc=e)
```

### 10.2. Payment Tasks

```python
@shared_task
def process_webhook(data):
    processor = PaymentProcessor()
    try:
        processor.process_webhook(data)
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise
```

## Apêndice A: Dependências

```plaintext
# requirements/base.txt

django==5.0.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
celery==5.3.0
redis==4.6.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
boto3==1.28.0
python-docx==0.8.11
reportlab==4.0.4
openpyxl==3.1.2
pypandoc==1.11
pillow==10.0.0
```

## Apêndice B: Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar Celery worker
celery -A saberangola worker -l info

# Iniciar Celery beat
celery -A saberangola beat -l info

# Coletar arquivos estáticos
python manage.py collectstatic

# Rodar testes
python manage.py test
```

## Apêndice C: Ambiente de Desenvolvimento

```yaml
# docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=saberangola
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      
  redis:
    image: redis:7
    ports:
      - "6379:6379"
    
  celery:
    build: .
    command: celery -A saberangola worker -l info
    volumes:
      - .:/app
    depends_on:
      - redis
      
volumes:
  postgres_data:
```

---

Este documento detalha a estrutura completa do backend do SaberAngola, incluindo todos os componentes, configurações e exemplos de código. Use-o como referência para desenvolvimento e manutenção do sistema.