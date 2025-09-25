# Boas Práticas de Integração - SaberAngola

Este documento detalha as melhores práticas para integração entre o backend Django e o frontend Next.js no projeto SaberAngola.

## Sumário

1. [Padrões de API REST](#1-padrões-de-api-rest)
2. [Segurança](#2-segurança)
3. [Performance](#3-performance)
4. [Tratamento de Erros](#4-tratamento-de-erros)
5. [Versionamento](#5-versionamento)
6. [Cache](#6-cache)
7. [Documentação](#7-documentação)
8. [Autenticação e Autorização](#8-autenticação-e-autorização)
9. [Testes](#9-testes)
10. [Monitoramento](#10-monitoramento)
11. [Desenvolvimento](#11-desenvolvimento)
12. [Deploy](#12-deploy)
13. [Validação de Dados](#13-validação-de-dados)
14. [Frontend](#14-frontend)
15. [Anexos e Exemplos](#15-anexos-e-exemplos)

## 1. Padrões de API REST

### 1.1. Nomenclatura de Endpoints

- Use substantivos no plural
- Mantenha consistência
- Evite verbos nos URLs
- Use kebab-case para URLs
- Use camelCase para parâmetros

✅ Bom:
```
GET /api/users
GET /api/documents
POST /api/payment-transactions
```

❌ Ruim:
```
GET /api/getUser
GET /api/all_documents
POST /api/createPayment
```

### 1.2. Métodos HTTP

Use os métodos HTTP apropriados:
- GET: Leitura
- POST: Criação
- PUT: Atualização total
- PATCH: Atualização parcial
- DELETE: Remoção

### 1.3. Status Codes

Use códigos HTTP apropriados:
- 200: Sucesso
- 201: Criado
- 204: Sem conteúdo
- 400: Erro do cliente
- 401: Não autorizado
- 403: Proibido
- 404: Não encontrado
- 500: Erro do servidor

### 1.4. Query Parameters

- Paginação: `?page=1&per_page=10`
- Filtros: `?status=active&type=premium`
- Ordenação: `?sort=created_at&order=desc`
- Busca: `?search=termo`

### 1.5. Responses

```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total": 100
  },
  "links": {
    "self": "/api/resources?page=1",
    "next": "/api/resources?page=2",
    "prev": null
  }
}
```

## 2. Segurança

### 2.1. HTTPS

```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 2.2. CORS

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://saberangola.ao",
    "https://admin.saberangola.ao"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
```

### 2.3. Rate Limiting

```python
# throttling.py
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class CustomAnonThrottle(AnonRateThrottle):
    rate = '100/hour'

class CustomUserThrottle(UserRateThrottle):
    rate = '1000/hour'
```

### 2.4. Sanitização de Input

```python
# utils/sanitizers.py
import bleach

def sanitize_html(content):
    allowed_tags = ['p', 'b', 'i', 'u', 'em', 'strong']
    allowed_attrs = {'a': ['href', 'title']}
    
    return bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        strip=True
    )
```

## 3. Performance

### 3.1. Otimização de Queries

```python
# views.py
from django.db.models import Prefetch

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.select_related('user')\
        .prefetch_related(
            Prefetch('tags'),
            Prefetch('comments', queryset=Comment.objects.select_related('user'))
        )
```

### 3.2. Paginação

```python
# pagination.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'per_page'
    max_page_size = 1000
```

### 3.3. Cache

```python
# views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15))  # 15 minutos
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)
```

## 4. Tratamento de Erros

### 4.1. Exceções Customizadas

```python
# exceptions.py
from rest_framework.exceptions import APIException

class BusinessLogicError(APIException):
    status_code = 400
    default_detail = 'Erro na lógica de negócio'
    default_code = 'business_logic_error'

class ResourceLimitExceeded(APIException):
    status_code = 429
    default_detail = 'Limite de recursos excedido'
    default_code = 'resource_limit_exceeded'
```

### 4.2. Manipulador de Exceções

```python
# exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': {
                'code': response.status_code,
                'message': response.data.get('detail', str(exc)),
                'type': exc.__class__.__name__
            }
        }
    
    return response
```

### 4.3. Logging de Erros

```python
# middleware.py
import logging

logger = logging.getLogger('saberangola.errors')

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.error('Erro não tratado', exc_info=True, extra={
                'path': request.path,
                'method': request.method,
                'user_id': getattr(request.user, 'id', None)
            })
            raise
```

## 5. Versionamento

### 5.1. URLs Versionadas

```python
# urls.py
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),
]
```

### 5.2. Controle de Versão

```python
# versioning.py
from rest_framework.versioning import URLPathVersioning

class CustomVersioning(URLPathVersioning):
    default_version = 'v1'
    allowed_versions = ['v1', 'v2']
    version_param = 'version'
```

## 6. Cache

### 6.1. Redis Cache

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 6.2. Cache Decorator

```python
# decorators.py
from functools import wraps
from django.core.cache import cache

def cache_result(timeout=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(cache_key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
            
            return result
        return wrapper
    return decorator
```

## 7. Documentação

### 7.1. Swagger/OpenAPI

```python
# urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SaberAngola API",
        default_version='v1',
        description="API do SaberAngola",
        contact=openapi.Contact(email="dev@saberangola.ao"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
```

### 7.2. Docstrings

```python
# views.py
class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciamento de documentos.
    
    list:
    Retorna lista paginada de documentos
    
    create:
    Cria um novo documento
    
    retrieve:
    Retorna detalhes de um documento específico
    
    update:
    Atualiza um documento existente
    
    delete:
    Remove um documento
    """
```

## 8. Autenticação e Autorização

### 8.1. JWT Handler

```python
# auth/handlers.py
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
```

### 8.2. Permissões Customizadas

```python
# permissions.py
from rest_framework import permissions

class IsPremiumUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_premium

class IsDocumentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
```

## 9. Testes

### 9.1. Testes de API

```python
# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status

class DocumentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_document(self):
        data = {
            'title': 'Test Document',
            'content': 'Test content'
        }
        response = self.client.post('/api/documents/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### 9.2. Factory Boy

```python
# tests/factories.py
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    is_active = True
```

## 10. Monitoramento

### 10.1. Métricas

```python
# metrics.py
from prometheus_client import Counter, Histogram

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

request_latency = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)
```

### 10.2. Middleware de Performance

```python
# middleware.py
import time

class PerformanceMonitoringMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        
        duration = time.time() - start_time
        request_latency.labels(
            endpoint=request.path
        ).observe(duration)
        
        return response
```

## 11. Desenvolvimento

### 11.1. Ambiente de Desenvolvimento

```python
# settings/dev.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### 11.2. Configuração Docker

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.dev
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DATABASE_URL=postgres://user:pass@db:5432/saberangola
```

## 12. Deploy

### 12.1. Configuração de Produção

```python
# settings/prod.py
DEBUG = False
ALLOWED_HOSTS = ['.saberangola.ao']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 12.2. Checklist de Deploy

```python
# deploy/checklist.py
def pre_deploy_checks():
    checks = [
        check_database_migrations(),
        check_static_files(),
        check_environment_variables(),
        check_dependencies(),
        check_security_settings()
    ]
    return all(checks)
```

## 13. Validação de Dados

### 13.1. Serializers

```python
# serializers.py
from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'created_at']
        read_only_fields = ['created_at']
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                'Título deve ter pelo menos 3 caracteres'
            )
        return value
```

### 13.2. Validators

```python
# validators.py
from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    pattern = r'^\+244\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Número de telefone deve estar no formato +244XXXXXXXXX'
        )
```

## 14. Frontend

### 14.1. Serviços API

```typescript
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Handle token expiration
    }
    return Promise.reject(error)
  }
)
```

### 14.2. Hooks Customizados

```typescript
// hooks/useApi.ts
import { useState } from 'react'
import api from '@/services/api'

export function useApi<T>(endpoint: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      const response = await api.get<T>(endpoint)
      setData(response.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return { data, loading, error, fetchData }
}
```

## 15. Anexos e Exemplos

### 15.1. Exemplos de Integração

#### Backend (Django)

```python
# views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_document(request):
    try:
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Exception as e:
        logger.error('Erro ao criar documento', exc_info=True)
        return Response(
            {'error': 'Erro interno do servidor'},
            status=500
        )
```

#### Frontend (Next.js)

```typescript
// pages/documents/new.tsx
export default function NewDocument() {
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (data: FormData) => {
    try {
      setLoading(true)
      await api.post('/documents/', data)
      router.push('/documents')
    } catch (error) {
      toast.error('Erro ao criar documento')
    } finally {
      setLoading(false)
    }
  }

  return (
    <DocumentForm onSubmit={handleSubmit} loading={loading} />
  )
}
```

### 15.2. Checklist de Integração

✅ Autenticação e Autorização
- [ ] Implementar JWT
- [ ] Configurar refresh tokens
- [ ] Definir permissões
- [ ] Implementar logout

✅ Endpoints
- [ ] Documentar com OpenAPI
- [ ] Implementar versionamento
- [ ] Definir padrões de URL
- [ ] Configurar rate limiting

✅ Segurança
- [ ] Configurar HTTPS
- [ ] Implementar CORS
- [ ] Sanitizar inputs
- [ ] Configurar CSP

✅ Performance
- [ ] Implementar cache
- [ ] Otimizar queries
- [ ] Configurar paginação
- [ ] Monitorar métricas

### 15.3. Melhores Práticas

1. **Padronização**
   - Use convenções de nomenclatura consistentes
   - Mantenha documentação atualizada
   - Siga padrões REST

2. **Segurança**
   - Sempre use HTTPS
   - Implemente rate limiting
   - Valide todos os inputs
   - Use tokens seguros

3. **Performance**
   - Cache quando possível
   - Otimize queries
   - Minimize payload
   - Use paginação

4. **Manutenibilidade**
   - Código limpo e documentado
   - Testes automatizados
   - Logging adequado
   - Monitoramento

5. **Experiência do Usuário**
   - Feedback claro
   - Tratamento de erros
   - Loading states
   - Validação client-side

### 15.4. Considerações Finais

Este documento serve como guia completo para integração entre backend e frontend no projeto SaberAngola. Siga estas práticas para garantir:

- Código de qualidade
- Sistema seguro
- Alta performance
- Boa manutenibilidade
- Experiência positiva para usuários

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento.