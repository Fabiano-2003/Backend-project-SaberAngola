# Observabilidade e Health Checks - SaberAngola

Este documento detalha a implementação de observabilidade e health checks no projeto SaberAngola, incluindo logs, métricas, monitoramento e verificações de saúde do sistema.

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Health Checks](#2-health-checks)
3. [Logging](#3-logging)
4. [Métricas](#4-métricas)
5. [Monitoramento](#5-monitoramento)
6. [Alertas](#6-alertas)
7. [Rastreamento](#7-rastreamento)
8. [Dashboard](#8-dashboard)
9. [Boas Práticas](#9-boas-práticas)
10. [Exemplos Práticos](#10-exemplos-práticos)

## 1. Visão Geral

A observabilidade do SaberAngola é construída em várias camadas:

- Health Checks para verificação de status
- Logs estruturados para debugging
- Métricas para performance
- Tracing para análise de problemas
- Alertas para notificações
- Dashboards para visualização

### 1.1. Arquitetura

```
[Aplicação] → [Logs (ELK)] → [Métricas (Prometheus)] → [Visualização (Grafana)]
                ↓                      ↓                         ↓
           [Log Shipping]        [Alertmanager]            [Dashboards]
                ↓                      ↓                         ↓
           [Elasticsearch]      [Notificações]             [Reports]
```

## 2. Health Checks

### 2.1. Endpoint Principal

```python
# health/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class HealthCheckView(APIView):
    permission_classes = []
    
    def get(self, request):
        checks = {
            'database': self._check_database(),
            'redis': self._check_redis(),
            'celery': self._check_celery(),
            's3': self._check_s3(),
            'payment_gateways': self._check_payment_gateways()
        }
        
        status = 'healthy' if all(checks.values()) else 'unhealthy'
        
        return Response({
            'status': status,
            'timestamp': timezone.now(),
            'version': settings.APP_VERSION,
            'checks': checks
        })
    
    def _check_database(self):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return True
        except Exception as e:
            logger.error(f'Database health check failed: {str(e)}')
            return False
```

### 2.2. Verificações Específicas

```python
# health/checks.py
class ServiceHealthCheck:
    def check_redis(self):
        try:
            redis_client.ping()
            return True
        except RedisError:
            return False
    
    def check_s3(self):
        try:
            s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
            return True
        except ClientError:
            return False
    
    def check_celery(self):
        try:
            i = celery_app.control.inspect()
            return bool(i.active())
        except Exception:
            return False
```

## 3. Logging

### 3.1. Configuração

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(timestamp)s %(level)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/saberangola.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'json',
        }
    },
    'loggers': {
        'saberangola': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
```

### 3.2. Middleware de Logging

```python
# middleware.py
import logging
import time
import uuid

logger = logging.getLogger('saberangola.requests')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request
        logger.info('Request started', extra={
            'request_id': request_id,
            'method': request.method,
            'path': request.path,
            'user_id': getattr(request.user, 'id', None)
        })
        
        response = self.get_response(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info('Request finished', extra={
            'request_id': request_id,
            'status_code': response.status_code,
            'duration': duration
        })
        
        return response
```

## 4. Métricas

### 4.1. Configuração Prometheus

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Requests
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Latência
request_latency = Histogram(
    'request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# Usuários ativos
active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Documentos gerados
documents_generated = Counter(
    'documents_generated_total',
    'Total documents generated',
    ['type']
)

# Transações
payment_transactions = Counter(
    'payment_transactions_total',
    'Total payment transactions',
    ['status', 'gateway']
)
```

### 4.2. Middleware de Métricas

```python
# middleware.py
from prometheus_client import Counter, Histogram
import time

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.latency = Histogram(
            'http_request_latency_seconds',
            'HTTP request latency',
            ['method', 'endpoint']
        )
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        
        # Record latency
        self.latency.labels(
            method=request.method,
            endpoint=request.path
        ).observe(time.time() - start_time)
        
        return response
```

## 5. Monitoramento

### 5.1. Configuração Grafana

```yaml
# grafana/dashboards/saberangola.json
{
  "dashboard": {
    "title": "SaberAngola Overview",
    "panels": [
      {
        "title": "Requests per Second",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(request_latency_seconds_sum[5m]) / rate(request_latency_seconds_count[5m])",
            "legendFormat": "{{endpoint}}"
          }
        ]
      }
    ]
  }
}
```

## 6. Alertas

### 6.1. Regras de Alerta

```yaml
# prometheus/alerts.yml
groups:
  - name: saberangola
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}"

      - alert: SlowResponses
        expr: rate(request_latency_seconds_sum[5m]) / rate(request_latency_seconds_count[5m]) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow response times detected"
```

### 6.2. Notificações

```python
# notifications/alerts.py
class AlertNotifier:
    def __init__(self):
        self.channels = {
            'slack': SlackNotifier(),
            'email': EmailNotifier()
        }
    
    def notify(self, alert, channel='slack'):
        notifier = self.channels.get(channel)
        if notifier:
            notifier.send(alert)
```

## 7. Rastreamento

### 7.1. Configuração Sentry

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/1234567",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment=settings.ENVIRONMENT
)
```

### 7.2. Middleware de Tracing

```python
# middleware.py
from opentelemetry import trace

class TracingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.tracer = trace.get_tracer(__name__)
    
    def __call__(self, request):
        with self.tracer.start_as_current_span(
            name=f"{request.method} {request.path}",
            kind=trace.SpanKind.SERVER,
        ) as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", request.path)
            
            response = self.get_response(request)
            
            span.set_attribute("http.status_code", response.status_code)
            return response
```

## 8. Dashboard

### 8.1. API de Métricas

```python
# metrics/views.py
class MetricsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        metrics = {
            'active_users': self._get_active_users(),
            'document_stats': self._get_document_stats(),
            'payment_stats': self._get_payment_stats(),
            'system_health': self._get_system_health()
        }
        return Response(metrics)
    
    def _get_active_users(self):
        return {
            'total': User.objects.count(),
            'active_today': User.objects.filter(
                last_login__date=timezone.now().date()
            ).count()
        }
```

## 9. Boas Práticas

### 9.1. Logs Estruturados

```python
# utils/logging.py
def log_structured(logger, event, **kwargs):
    """
    Log eventos de forma estruturada
    """
    log_data = {
        'event': event,
        'timestamp': timezone.now().isoformat(),
        'environment': settings.ENVIRONMENT,
        **kwargs
    }
    
    logger.info(event, extra=log_data)
```

### 9.2. Métricas Customizadas

```python
# metrics/custom.py
class BusinessMetrics:
    def __init__(self):
        self.document_creation_time = Histogram(
            'document_creation_seconds',
            'Time spent creating documents',
            ['type', 'template']
        )
        
        self.payment_amount = Counter(
            'payment_amount_total',
            'Total payment amount',
            ['currency', 'gateway']
        )
```

## 10. Exemplos Práticos

### 10.1. Monitoramento de Endpoint

```python
# views.py
@method_decorator(monitor_endpoint)
class DocumentView(APIView):
    def post(self, request):
        with logger.auto_trace() as span:
            span.set_tag('document_type', request.data.get('type'))
            
            try:
                document = self.create_document(request.data)
                logger.info('Document created', extra={
                    'document_id': document.id,
                    'user_id': request.user.id
                })
                return Response(status=201)
            except Exception as e:
                logger.error('Document creation failed', exc_info=True)
                raise
```

### 10.2. Health Check Customizado

```python
# health/custom_checks.py
class ApplicationHealthCheck:
    def check_external_apis(self):
        results = {}
        apis = {
            'payment': 'https://api.emis.ao/health',
            'storage': 'https://s3.amazonaws.com/health'
        }
        
        for name, url in apis.items():
            try:
                response = requests.get(url, timeout=5)
                results[name] = response.status_code == 200
            except Exception:
                results[name] = False
        
        return results
```

## Conclusão

O sistema de observabilidade do SaberAngola é:

- **Abrangente:** Cobre todos os aspectos críticos do sistema
- **Proativo:** Detecta problemas antes que afetem usuários
- **Detalhado:** Fornece informações precisas para debugging
- **Escalável:** Cresce com a aplicação
- **Configurável:** Adaptável a diferentes necessidades
- **Seguro:** Protege dados sensíveis

Para mais informações sobre configurações específicas ou implementações avançadas, consulte a documentação das ferramentas ou entre em contato com a equipe de infraestrutura.