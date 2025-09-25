# Tarefas Assíncronas (Celery) - SaberAngola

Este documento detalha a implementação e uso do Celery para processamento assíncrono de tarefas no projeto SaberAngola.

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Configuração](#2-configuração)
3. [Tipos de Tarefas](#3-tipos-de-tarefas)
4. [Implementação Backend](#4-implementação-backend)
5. [Integração Frontend](#5-integração-frontend)
6. [Monitoramento e Logs](#6-monitoramento-e-logs)
7. [Boas Práticas](#7-boas-práticas)
8. [Tratamento de Erros](#8-tratamento-de-erros)
9. [Escalabilidade](#9-escalabilidade)
10. [Exemplos Práticos](#10-exemplos-práticos)

## 1. Visão Geral

O SaberAngola utiliza Celery para processamento assíncrono de:
- Geração de documentos complexos
- Envio de emails em massa
- Processamento de arquivos grandes
- Integrações com APIs externas
- Tarefas agendadas (periódicas)
- Backups automáticos

### 1.1. Arquitetura

```
[Django App] → [Redis (Broker)] → [Celery Workers] → [Redis (Results)]
```

### 1.2. Componentes Principais

- Celery: Sistema de filas e workers
- Redis: Message broker e armazenamento de resultados
- Flower: Monitoramento e administração
- Celery Beat: Agendamento de tarefas

## 2. Configuração

### 2.1. Configuração Básica

```python
# settings.py
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Luanda'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutos
```

### 2.2. Inicialização do Celery

```python
# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saberangola.settings')

app = Celery('saberangola')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

### 2.3. Configuração do Beat

```python
# settings.py
CELERY_BEAT_SCHEDULE = {
    'process-daily-reports': {
        'task': 'documents.tasks.generate_daily_reports',
        'schedule': crontab(hour=0, minute=0),
    },
    'cleanup-temp-files': {
        'task': 'storage.tasks.cleanup_temp_files',
        'schedule': crontab(hour='*/6'),  # A cada 6 horas
    },
}
```

## 3. Tipos de Tarefas

### 3.1. Tarefas Básicas

```python
# tasks.py
from celery import shared_task

@shared_task
def process_document(document_id):
    document = Document.objects.get(id=document_id)
    # Processamento do documento
    return {'status': 'completed', 'document_id': document_id}
```

### 3.2. Tarefas com Retry

```python
@shared_task(
    bind=True,
    max_retries=3,
    retry_backoff=True,
    retry_backoff_max=600
)
def process_payment(self, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        # Processamento do pagamento
    except Exception as exc:
        self.retry(exc=exc)
```

### 3.3. Tarefas Periódicas

```python
@shared_task
def cleanup_expired_documents():
    threshold = timezone.now() - timedelta(days=30)
    Document.objects.filter(
        created_at__lt=threshold,
        status='temporary'
    ).delete()
```

## 4. Implementação Backend

### 4.1. Serviço de Tarefas

```python
# services.py
class AsyncTaskService:
    def __init__(self):
        self.task_map = {
            'document': process_document,
            'payment': process_payment,
            'email': send_bulk_email
        }
    
    def execute_task(self, task_type, **kwargs):
        task = self.task_map.get(task_type)
        if not task:
            raise ValueError(f"Tipo de tarefa inválido: {task_type}")
        
        return task.delay(**kwargs)
    
    def get_task_status(self, task_id):
        task_result = AsyncResult(task_id)
        return {
            'task_id': task_id,
            'status': task_result.status,
            'result': task_result.result if task_result.ready() else None
        }
```

### 4.2. Views e Endpoints

```python
# views.py
class TaskViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def execute(self, request):
        service = AsyncTaskService()
        task = service.execute_task(
            request.data['task_type'],
            **request.data['params']
        )
        return Response({'task_id': task.id})
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        service = AsyncTaskService()
        status = service.get_task_status(pk)
        return Response(status)
```

## 5. Integração Frontend

### 5.1. Hook de Tarefas Assíncronas

```typescript
// hooks/useAsyncTask.ts
import { useState, useEffect } from 'react'
import axios from 'axios'

export const useAsyncTask = (taskId: string | null) => {
  const [status, setStatus] = useState<string | null>(null)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  
  useEffect(() => {
    if (!taskId) return
    
    const checkStatus = async () => {
      try {
        const response = await axios.get(`/api/tasks/${taskId}/status/`)
        setStatus(response.data.status)
        
        if (response.data.status === 'SUCCESS') {
          setResult(response.data.result)
        }
      } catch (err) {
        setError('Erro ao verificar status da tarefa')
      }
    }
    
    const interval = setInterval(checkStatus, 2000)
    return () => clearInterval(interval)
  }, [taskId])
  
  return { status, result, error }
}
```

### 5.2. Componente de Progresso

```typescript
// components/TaskProgress.tsx
import { useAsyncTask } from '@/hooks/useAsyncTask'

interface TaskProgressProps {
  taskId: string
  onComplete: (result: any) => void
}

export const TaskProgress: React.FC<TaskProgressProps> = ({
  taskId,
  onComplete
}) => {
  const { status, result, error } = useAsyncTask(taskId)
  
  useEffect(() => {
    if (status === 'SUCCESS' && result) {
      onComplete(result)
    }
  }, [status, result])
  
  return (
    <div>
      {status === 'PENDING' && <p>Processando...</p>}
      {status === 'SUCCESS' && <p>Concluído!</p>}
      {error && <p className="error">{error}</p>}
    </div>
  )
}
```

## 6. Monitoramento e Logs

### 6.1. Configuração do Flower

```python
# flower.py
from flower.utils.template import humanize

broker_api = 'redis://redis:6379/0'
basic_auth = ['admin:senha123']
port = 5555
```

### 6.2. Logging de Tarefas

```python
# tasks.py
import logging

logger = logging.getLogger('celery')

@shared_task
def process_task(task_data):
    logger.info(f'Iniciando tarefa: {task_data}')
    try:
        # Processamento
        logger.info('Tarefa concluída com sucesso')
    except Exception as e:
        logger.error(f'Erro na tarefa: {str(e)}')
        raise
```

## 7. Boas Práticas

### 7.1. Estrutura de Tarefas

```python
# tasks/base.py
class BaseTask(Task):
    abstract = True
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Notificar erro
        notify_error.delay(
            task_id=task_id,
            error=str(exc)
        )
    
    def on_success(self, retval, task_id, args, kwargs):
        # Log de sucesso
        log_success.delay(
            task_id=task_id,
            result=retval
        )
```

### 7.2. Chains e Groups

```python
# tasks/workflows.py
from celery import chain, group

def process_documents(document_ids):
    # Processamento paralelo
    tasks = group(
        process_document.s(doc_id)
        for doc_id in document_ids
    )
    
    # Encadeamento de tarefas
    workflow = chain(
        tasks,
        notify_completion.s()
    )
    
    return workflow()
```

## 8. Tratamento de Erros

### 8.1. Retry com Backoff

```python
@shared_task(
    autoretry_for=(RequestException,),
    retry_kwargs={'max_retries': 5},
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True
)
def call_external_api(endpoint, data):
    response = requests.post(endpoint, json=data)
    response.raise_for_status()
    return response.json()
```

### 8.2. Dead Letter Queue

```python
# settings.py
CELERY_TASK_ROUTES = {
    'tasks.critical.*': {
        'queue': 'critical',
        'delivery_mode': 'persistent',
    }
}

CELERY_TASK_QUEUES = {
    'critical': {
        'exchange': 'critical',
        'routing_key': 'critical.#',
        'queue_arguments': {'x-dead-letter-exchange': 'dlx'}
    }
}
```

## 9. Escalabilidade

### 9.1. Configuração de Workers

```python
# worker_config.py
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 200
worker_concurrency = 4
```

### 9.2. Priorização de Filas

```python
app.conf.task_queues = {
    'high': {
        'exchange': 'high',
        'routing_key': 'high.#',
        'queue_arguments': {'x-max-priority': 10}
    },
    'default': {
        'exchange': 'default',
        'routing_key': 'default.#'
    },
    'low': {
        'exchange': 'low',
        'routing_key': 'low.#'
    }
}
```

## 10. Exemplos Práticos

### 10.1. Geração de Documento

```python
# documents/tasks.py
@shared_task(bind=True)
def generate_complex_document(self, document_id):
    try:
        document = Document.objects.get(id=document_id)
        
        # Atualizar progresso
        self.update_state(
            state='PROGRESS',
            meta={'progress': 30}
        )
        
        # Gerar documento
        generated_file = DocumentGenerator().generate(document.data)
        
        # Upload para S3
        self.update_state(
            state='PROGRESS',
            meta={'progress': 70}
        )
        
        s3_url = upload_to_s3(generated_file)
        
        # Atualizar documento
        document.status = 'completed'
        document.file_url = s3_url
        document.save()
        
        return {
            'status': 'success',
            'document_id': document_id,
            'file_url': s3_url
        }
        
    except Exception as e:
        document.status = 'failed'
        document.save()
        raise
```

### 10.2. Processamento em Lote

```python
@shared_task
def process_batch(batch_id):
    batch = Batch.objects.get(id=batch_id)
    items = batch.items.all()
    
    # Criar subtarefas
    subtasks = []
    for item in items:
        task = process_item.delay(item.id)
        subtasks.append(task.id)
    
    # Atualizar batch com IDs das subtarefas
    batch.task_ids = subtasks
    batch.save()
    
    return {
        'batch_id': batch_id,
        'total_items': len(items),
        'subtasks': subtasks
    }
```

## Conclusão

O sistema de tarefas assíncronas do SaberAngola é:

- **Robusto:** Tratamento adequado de erros e retentativas
- **Escalável:** Configurado para alta performance
- **Monitorável:** Logs detalhados e dashboard Flower
- **Flexível:** Suporte a diferentes tipos de tarefas
- **Confiável:** Dead letter queues e persistência
- **Manutenível:** Código organizado e bem documentado

Para mais informações sobre configurações específicas ou casos de uso avançados, consulte a documentação do Celery ou entre em contato com a equipe de desenvolvimento.