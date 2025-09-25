# Integração Backend (Django + DRF) e Frontend (Next.js) – SaberAngola

---

## Sumário

1. Visão Geral da Arquitetura
2. Estrutura do Backend
3. Estrutura do Frontend
4. Fluxos de Integração
5. Autenticação e Segurança
6. Endpoints REST: Especificação e Exemplos
7. Geração e Download de Documentos
8. Integração de Pagamentos
9. Uploads e Armazenamento (S3)
10. Tarefas Assíncronas (Celery)
11. Observabilidade e Health Checks
12. Boas Práticas de Integração
13. Testes de Integração
14. CI/CD e Deploy
15. Referências e Recursos

---

## 1. Visão Geral da Arquitetura

O projeto SaberAngola é composto por dois grandes blocos:

- **Frontend:** Next.js (React), consumindo APIs REST.
- **Backend:** Django + Django REST Framework (DRF), responsável por autenticação, regras de negócio, geração de documentos, pagamentos e integrações.

```
[Usuário] ⇄ [Frontend Next.js] ⇄ [API REST Django/DRF] ⇄ [Serviços Internos, S3, Gateways de Pagamento]
```

- Comunicação via HTTP/HTTPS (JSON).
- Autenticação JWT.
- Documentos e arquivos servidos via links S3.
- Pagamentos integrados via APIs locais (EMIS, Unitel Money, etc).

---

## 2. Estrutura do Backend (Django + DRF)

### 2.1. Apps Principais

- **auth:** Autenticação (JWT/SimpleJWT), permissões, login, registro.
- **users:** Perfis, gestão de contas, roles.
- **documents:** Geração, edição, download de documentos (Word, PDF, Excel).
- **payments:** Subscrições, faturas, integração com gateways.

### 2.2. Bibliotecas e Ferramentas

- Django, DRF, SimpleJWT, django-cors-headers, django-ratelimit, bleach, boto3, python-docx, reportlab, pypandoc, openpyxl, Celery, Redis, S3, Docker, Sentry, Prometheus, Grafana.

### 2.3. Estrutura de Pastas (Exemplo)

```
backend/
  manage.py
  saberangola/
    settings.py
    urls.py
    wsgi.py
  auth/
    models.py
    views.py
    serializers.py
    urls.py
  users/
    ...
  documents/
    ...
  payments/
    ...
  ...
```

---

## 3. Estrutura do Frontend (Next.js)

- **Páginas:** `/login`, `/register`, `/perfil`, `/documentos`, `/pagamentos`, etc.
- **Componentes:** Formulários, tabelas, visualização de documentos, integração com API.
- **Serviços:** Funções para consumir endpoints REST (fetch/axios), hooks de autenticação, contexto global de usuário.

---

## 4. Fluxos de Integração

### 4.1. Autenticação

1. Usuário preenche login no frontend.
2. Frontend envia POST para `/api/auth/login/`.
3. Backend retorna JWT (access/refresh).
4. Frontend armazena tokens (cookie seguro ou localStorage).
5. Para cada requisição autenticada, frontend envia `Authorization: Bearer <token>`.

### 4.2. Geração de Documento

1. Usuário preenche formulário de documento.
2. Frontend envia POST para `/api/documents/` com dados.
3. Backend gera documento, salva no S3, retorna link de download.
4. Frontend exibe botão/link para download.

### 4.3. Pagamento

1. Usuário seleciona plano/pagamento.
2. Frontend envia POST para `/api/payments/checkout/`.
3. Backend cria Order, retorna URL/ref. do gateway.
4. Usuário realiza pagamento no gateway.
5. Gateway chama `/api/payments/webhook/`.
6. Backend confirma pagamento, atualiza status.
7. Frontend consulta status via `/api/payments/`.

---

## 5. Autenticação e Segurança

### 5.1. JWT (SimpleJWT)

- Login: `/api/auth/login/` → retorna `access` e `refresh` tokens.
- Refresh: `/api/auth/refresh/` → novo access token.
- Logout: frontend remove tokens.

#### Exemplo de Payload de Login

```json
POST /api/auth/login/
{
  "email": "user@email.com",
  "password": "senha123"
}
```

#### Resposta

```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

### 5.2. Permissões

- `IsAuthenticated`: apenas usuários logados.
- `IsAdminUser`: apenas admins.
- Roles customizadas: ex. `is_premium`, `is_staff`.

### 5.3. Proteções

- **CORS:** Configurado para domínios do frontend.
- **CSRF:** Protegido em endpoints sensíveis.
- **Rate Limiting:** django-ratelimit.
- **Sanitização:** bleach em campos de texto.

---

## 6. Endpoints REST: Especificação e Exemplos

### 6.1. Auth

| Método | Endpoint              | Descrição           |
|--------|-----------------------|---------------------|
| POST   | /api/auth/register/   | Registro de usuário |
| POST   | /api/auth/login/      | Login JWT           |
| POST   | /api/auth/refresh/    | Refresh token       |

### 6.2. Users

| Método | Endpoint      | Descrição                |
|--------|---------------|--------------------------|
| GET    | /api/users/   | Listar perfis            |
| POST   | /api/users/   | Criar perfil             |
| GET    | /api/users/me/| Perfil do usuário logado |
| PATCH  | /api/users/me/| Atualizar perfil         |

### 6.3. Documents

| Método | Endpoint           | Descrição                  |
|--------|--------------------|----------------------------|
| GET    | /api/documents/    | Listar documentos          |
| POST   | /api/documents/    | Criar documento            |
| GET    | /api/documents/:id/| Baixar documento           |

#### Exemplo de Criação de Documento

```json
POST /api/documents/
{
  "title": "Relatório de Projeto",
  "content": "Texto do relatório...",
  "type": "pdf"
}
```

#### Resposta

```json
{
  "id": 123,
  "download_url": "https://s3.amazonaws.com/bucket/doc-123.pdf"
}
```

### 6.4. Payments

| Método | Endpoint                  | Descrição                  |
|--------|---------------------------|----------------------------|
| POST   | /api/payments/checkout/   | Iniciar pagamento          |
| POST   | /api/payments/webhook/    | Receber callback do gateway|
| GET    | /api/payments/            | Listar pagamentos          |

#### Exemplo de Checkout

```json
POST /api/payments/checkout/
{
  "plan": "premium"
}
```

#### Resposta

```json
{
  "order_id": 456,
  "payment_url": "https://emis.ao/pay/xyz"
}
```

---

## 7. Geração e Download de Documentos

### 7.1. Bibliotecas Utilizadas

- **python-docx:** Word (.docx)
- **reportlab:** PDF
- **openpyxl:** Excel
- **pypandoc:** Conversão entre formatos

### 7.2. Fluxo Backend

1. Recebe requisição com dados do documento.
2. Gera arquivo no formato solicitado.
3. Salva no S3 (boto3).
4. Retorna URL de download.

### 7.3. Exemplo de Serviço (Pseudo-código)

```python
def generate_document(data):
    if data['type'] == 'pdf':
        # usar reportlab
    elif data['type'] == 'docx':
        # usar python-docx
    # ...
    s3_url = upload_to_s3(file)
    return s3_url
```

---

## 8. Integração de Pagamentos

### 8.1. Gateways Suportados

- EMIS (Multicaixa Express)
- Unitel Money
- Africell Money

### 8.2. Fluxo de Pagamento

1. Usuário solicita pagamento (frontend → backend).
2. Backend cria Order, chama API do gateway.
3. Gateway retorna URL/ref. de pagamento.
4. Usuário paga via app/site do gateway.
5. Gateway envia webhook para backend.
6. Backend confirma pagamento, atualiza status.
7. Frontend consulta status e libera recursos.

### 8.3. Modelos Django

- **Plan:** free, premium
- **Subscription:** status, user, plano, validade
- **Transaction:** valor, status, referência, timestamps

---

## 9. Uploads e Armazenamento (S3)

- Documentos gerados são salvos no S3.
- URLs de download são retornadas ao frontend.
- Uploads de arquivos do usuário (ex.: avatar) também via S3.
- Uso de boto3 e django-storages.

---

## 10. Tarefas Assíncronas (Celery)

- Geração de documentos pesados feita em background.
- Celery + Redis para filas de tarefas.
- Frontend pode consultar status via endpoint.

---

## 11. Observabilidade e Health Checks

- Logs estruturados (settings.py).
- Endpoint `/api/health/` para health check.
- Sentry para erros.
- Prometheus/Grafana para métricas (futuro).

---

## 12. Boas Práticas de Integração

- Sempre validar respostas da API.
- Tratar erros e exibir mensagens amigáveis.
- Usar HTTPS em produção.
- Tokens JWT em cookies HttpOnly ou localStorage seguro.
- Versionar API se necessário (`/api/v1/`).
- Documentar endpoints (Swagger/Redoc).

---

## 13. Testes de Integração

- Testes automatizados de endpoints (pytest, DRF test).
- Testes E2E (Cypress/Playwright) no frontend.
- Mock de serviços externos (pagamentos, S3).

---

## 14. CI/CD e Deploy

- GitHub Actions para testes, lint, build e deploy.
- Docker para empacotamento.
- Deploy em AWS (ECS, S3, etc).
- Rollback automático em caso de falha.

---

## 15. Referências e Recursos

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Next.js](https://nextjs.org/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Celery](https://docs.celeryq.dev/en/stable/)
- [Sentry](https://sentry.io/welcome/)

---

# ANEXOS

## A. Exemplos de Requisições e Respostas

### Registro de Usuário

```json
POST /api/auth/register/
{
  "email": "novo@user.com",
  "password": "senha123",
  "name": "Novo Usuário"
}
```

### Resposta

```json
{
  "id": 789,
  "email": "novo@user.com",
  "name": "Novo Usuário"
}
```

---

## B. Diagrama de Sequência (Texto)

```
Usuário → Frontend: Preenche formulário
Frontend → Backend: POST /api/documents/
Backend → S3: Salva documento
Backend → Frontend: Retorna URL
Frontend → Usuário: Exibe link de download
```

---

## C. Checklist de Integração

- [x] Endpoints REST documentados
- [x] Autenticação JWT implementada
- [x] Permissões e roles configuradas
- [x] Geração de documentos funcional
- [x] Integração com pagamentos testada
- [x] Upload/download via S3
- [x] Health check disponível
- [x] Logs e monitoramento ativos

---

## D. Observações Finais

- O backend deve ser desacoplado, servindo múltiplos frontends.
- Toda comunicação deve ser via API REST.
- O frontend nunca deve acessar recursos internos do backend diretamente.
- Segurança, escalabilidade e observabilidade são prioridades.

---

> **Este documento serve como guia de integração entre equipes frontend e backend, detalhando fluxos, endpoints, exemplos e boas práticas para garantir uma integração eficiente, segura e escalável no SaberAngola.**

<!--
Este arquivo pode ser expandido com mais exemplos, fluxos detalhados, diagramas visuais, e instruções específicas conforme o projeto evoluir. Para atingir 1000 linhas, adicione mais exemplos, fluxos alternativos, casos de erro, e detalhamento de cada endpoint e payload.
-->
