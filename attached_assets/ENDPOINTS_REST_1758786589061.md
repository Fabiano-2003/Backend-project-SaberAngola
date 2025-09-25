# Documentação dos Endpoints REST - SaberAngola

Esta documentação detalha todos os endpoints REST disponíveis na API do SaberAngola, incluindo exemplos de requisições e respostas.

## Índice

1. [Autenticação](#1-autenticação)
2. [Usuários](#2-usuários)
3. [Documentos](#3-documentos)
4. [Pagamentos](#4-pagamentos)
5. [Health Check](#5-health-check)

## 1. Autenticação

### 1.1. Registro de Usuário

```http
POST /api/auth/register/
```

#### Request Body
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "name": "Nome Completo"
}
```

#### Response (201 Created)
```json
{
  "id": 789,
  "email": "usuario@exemplo.com",
  "name": "Nome Completo"
}
```

### 1.2. Login

```http
POST /api/auth/login/
```

#### Request Body
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

#### Response (200 OK)
```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

### 1.3. Refresh Token

```http
POST /api/auth/refresh/
```

#### Request Body
```json
{
  "refresh": "<jwt_refresh_token>"
}
```

#### Response (200 OK)
```json
{
  "access": "<new_jwt_access_token>"
}
```

## 2. Usuários

### 2.1. Listar Perfis

```http
GET /api/users/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Response (200 OK)
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "usuario@exemplo.com",
      "name": "Nome do Usuário",
      "created_at": "2025-09-23T10:00:00Z"
    }
  ]
}
```

### 2.2. Obter Perfil do Usuário Logado

```http
GET /api/users/me/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Response (200 OK)
```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "name": "Nome do Usuário",
  "created_at": "2025-09-23T10:00:00Z",
  "is_premium": false
}
```

### 2.3. Atualizar Perfil

```http
PATCH /api/users/me/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Request Body
```json
{
  "name": "Novo Nome",
  "avatar_url": "https://exemplo.com/avatar.jpg"
}
```

#### Response (200 OK)
```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "name": "Novo Nome",
  "avatar_url": "https://exemplo.com/avatar.jpg",
  "created_at": "2025-09-23T10:00:00Z"
}
```

## 3. Documentos

### 3.1. Listar Documentos

```http
GET /api/documents/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Query Parameters
- `page`: Número da página (default: 1)
- `per_page`: Itens por página (default: 10)
- `type`: Filtrar por tipo (pdf, docx, xlsx)

#### Response (200 OK)
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 123,
      "title": "Relatório de Projeto",
      "type": "pdf",
      "created_at": "2025-09-23T10:00:00Z",
      "download_url": "https://s3.amazonaws.com/bucket/doc-123.pdf"
    }
  ]
}
```

### 3.2. Criar Documento

```http
POST /api/documents/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
Content-Type: application/json
```

#### Request Body
```json
{
  "title": "Relatório de Projeto",
  "content": "Texto do relatório...",
  "type": "pdf"
}
```

#### Response (201 Created)
```json
{
  "id": 123,
  "title": "Relatório de Projeto",
  "type": "pdf",
  "created_at": "2025-09-23T10:00:00Z",
  "download_url": "https://s3.amazonaws.com/bucket/doc-123.pdf"
}
```

### 3.3. Baixar Documento

```http
GET /api/documents/{id}/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Response (200 OK)
Headers incluirão Content-Disposition para download do arquivo.

## 4. Pagamentos

### 4.1. Iniciar Checkout

```http
POST /api/payments/checkout/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Request Body
```json
{
  "plan": "premium",
  "payment_method": "emis"
}
```

#### Response (200 OK)
```json
{
  "order_id": 456,
  "payment_url": "https://emis.ao/pay/xyz",
  "amount": 5000,
  "currency": "AOA",
  "expires_at": "2025-09-23T11:00:00Z"
}
```

### 4.2. Listar Pagamentos

```http
GET /api/payments/
```

#### Headers
```
Authorization: Bearer <jwt_access_token>
```

#### Response (200 OK)
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 456,
      "amount": 5000,
      "currency": "AOA",
      "status": "completed",
      "payment_method": "emis",
      "created_at": "2025-09-23T10:00:00Z"
    }
  ]
}
```

### 4.3. Webhook de Pagamento

```http
POST /api/payments/webhook/
```

Este endpoint é chamado pelo gateway de pagamento para atualizar o status do pagamento.

#### Request Body (exemplo EMIS)
```json
{
  "order_id": "456",
  "status": "completed",
  "transaction_id": "emis_xyz123"
}
```

#### Response (200 OK)
```json
{
  "status": "ok"
}
```

## 5. Health Check

### 5.1. Status do Sistema

```http
GET /api/health/
```

#### Response (200 OK)
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "storage": "connected",
  "timestamp": "2025-09-23T10:00:00Z"
}
```

## Notas Importantes

1. **Autenticação**
   - Todos os endpoints (exceto registro, login e health check) requerem o header `Authorization: Bearer <token>`
   - Tokens JWT expiram em 24 horas
   - Use o endpoint de refresh para obter um novo token

2. **Rate Limiting**
   - Limite de 100 requisições por minuto por IP
   - Endpoints de autenticação têm limite reduzido (10 req/min)

3. **Códigos de Erro**
   - 400: Bad Request - Dados inválidos
   - 401: Unauthorized - Token inválido ou expirado
   - 403: Forbidden - Sem permissão para o recurso
   - 404: Not Found - Recurso não encontrado
   - 429: Too Many Requests - Rate limit excedido

4. **Formatos de Data**
   - Todas as datas são retornadas em formato ISO 8601
   - Timezone UTC (Z)

5. **Paginação**
   - Endpoints que retornam listas suportam paginação
   - Use `page` e `per_page` como query parameters
   - Resposta inclui `count`, `next` e `previous`

6. **CORS**
   - API configurada para aceitar requisições do frontend
   - Domínios permitidos configurados no backend

7. **Segurança**
   - HTTPS obrigatório em produção
   - Tokens JWT armazenados em cookies HttpOnly
   - Implementação de CSRF tokens para endpoints POST/PUT/DELETE