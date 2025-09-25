# Testes de Integração - SaberAngola

## Sumário

1. Visão Geral
2. Configuração do Ambiente de Testes
3. Testes Backend (Django + DRF)
4. Testes Frontend (Next.js)
5. Testes E2E
6. Testes de Performance
7. CI/CD e Automação
8. Boas Práticas
9. Troubleshooting

---

## 1. Visão Geral

### 1.1. Objetivos dos Testes de Integração

- Validar a comunicação entre frontend e backend
- Garantir funcionamento correto dos fluxos principais
- Detectar problemas de integração precocemente
- Assegurar qualidade em ambientes similares à produção

### 1.2. Tipos de Testes Cobertos

- Testes de API (Backend)
- Testes de Interface (Frontend)
- Testes End-to-End (E2E)
- Testes de Performance
- Testes de Segurança

---

## 2. Configuração do Ambiente de Testes

### 2.1. Ambiente Backend

```python
# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client):
    User = get_user_model()
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )
    api_client.force_authenticate(user=user)
    return api_client
```

### 2.2. Ambiente Frontend

```typescript
// jest.setup.ts
import '@testing-library/jest-dom'
import { server } from './mocks/server'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

### 2.3. Variáveis de Ambiente

```env
# .env.test
NEXT_PUBLIC_API_URL=http://localhost:8000/api
DATABASE_URL=postgresql://test:test@localhost:5432/test_db
AWS_ACCESS_KEY_ID=test-key
AWS_SECRET_ACCESS_KEY=test-secret
AWS_BUCKET_NAME=test-bucket
```

---

## 3. Testes Backend (Django + DRF)

### 3.1. Testes de API

```python
# test_auth_api.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestAuthAPI:
    def test_login_success(self, api_client):
        url = reverse('auth:login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_invalid_credentials(self, api_client):
        url = reverse('auth:login')
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = api_client.post(url, data)
        assert response.status_code == 401
```

### 3.2. Testes de Documentos

```python
# test_documents_api.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestDocumentsAPI:
    def test_create_document(self, auth_client):
        url = reverse('documents:create')
        data = {
            'title': 'Test Document',
            'content': 'Test content',
            'type': 'pdf'
        }
        response = auth_client.post(url, data)
        assert response.status_code == 201
        assert 'download_url' in response.data

    def test_list_documents(self, auth_client):
        url = reverse('documents:list')
        response = auth_client.get(url)
        assert response.status_code == 200
        assert isinstance(response.data, list)
```

### 3.3. Testes de Pagamentos

```python
# test_payments_api.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestPaymentsAPI:
    def test_create_checkout(self, auth_client):
        url = reverse('payments:checkout')
        data = {
            'plan': 'premium'
        }
        response = auth_client.post(url, data)
        assert response.status_code == 201
        assert 'order_id' in response.data
        assert 'payment_url' in response.data

    def test_webhook_processing(self, api_client):
        url = reverse('payments:webhook')
        data = {
            'reference': 'test-ref-123',
            'status': 'completed'
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
```

---

## 4. Testes Frontend (Next.js)

### 4.1. Testes de Componentes

```typescript
// LoginForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { LoginForm } from '@/components/LoginForm'

describe('LoginForm', () => {
  it('should submit form with correct data', async () => {
    const mockOnSubmit = jest.fn()
    render(<LoginForm onSubmit={mockOnSubmit} />)

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' }
    })
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' }
    })
    fireEvent.click(screen.getByRole('button', { name: /login/i }))

    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    })
  })
})
```

### 4.2. Testes de Integração API

```typescript
// useAuth.test.tsx
import { renderHook, act } from '@testing-library/react-hooks'
import { useAuth } from '@/hooks/useAuth'

describe('useAuth', () => {
  it('should login user successfully', async () => {
    const { result } = renderHook(() => useAuth())

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123'
      })
    })

    expect(result.current.isAuthenticated).toBe(true)
    expect(result.current.user).toBeDefined()
  })
})
```

### 4.3. Mocks de API

```typescript
// mocks/handlers.ts
import { rest } from 'msw'

export const handlers = [
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        access: 'mock-access-token',
        refresh: 'mock-refresh-token'
      })
    )
  }),

  rest.get('/api/documents', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 1,
          title: 'Test Document',
          download_url: 'https://example.com/doc1.pdf'
        }
      ])
    )
  })
]
```

---

## 5. Testes E2E (Cypress)

### 5.1. Configuração

```javascript
// cypress.config.js
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    }
  }
})
```

### 5.2. Testes de Fluxo Completo

```javascript
// cypress/e2e/document-creation.cy.js
describe('Document Creation Flow', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password123')
  })

  it('should create and download a document', () => {
    cy.visit('/documents/new')
    
    cy.get('[data-cy="title-input"]')
      .type('Test Document')
    
    cy.get('[data-cy="content-input"]')
      .type('Test content')
    
    cy.get('[data-cy="type-select"]')
      .select('pdf')
    
    cy.get('[data-cy="submit-button"]')
      .click()
    
    cy.get('[data-cy="download-link"]')
      .should('be.visible')
      .and('have.attr', 'href')
      .and('include', 's3.amazonaws.com')
  })
})
```

### 5.3. Comandos Customizados

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.request({
    method: 'POST',
    url: '/api/auth/login',
    body: { email, password }
  }).then((response) => {
    window.localStorage.setItem(
      'auth',
      JSON.stringify(response.body)
    )
  })
})
```

---

## 6. Testes de Performance

### 6.1. Configuração k6

```javascript
// performance/login.js
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  vus: 10,
  duration: '30s',
}

export default function () {
  const payload = JSON.stringify({
    email: 'test@example.com',
    password: 'testpass123'
  })

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  }

  const res = http.post(
    'http://localhost:8000/api/auth/login',
    payload,
    params
  )

  check(res, {
    'status is 200': (r) => r.status === 200,
    'has access token': (r) => r.json('access') !== undefined,
  })

  sleep(1)
}
```

### 6.2. Métricas de Performance

```javascript
// performance/metrics.js
import { Trend } from 'k6/metrics'

const documentCreationTrend = new Trend('document_creation_duration')

export default function () {
  const startTime = new Date()
  
  // Perform document creation request
  
  const duration = new Date() - startTime
  documentCreationTrend.add(duration)
}
```

---

## 7. CI/CD e Automação

### 7.1. GitHub Actions

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run backend tests
      run: |
        pytest tests/
      env:
        DATABASE_URL: postgresql://test:test@localhost:5432/test_db
    
    - name: Set up Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Install frontend dependencies
      run: npm ci
    
    - name: Run frontend tests
      run: npm test
    
    - name: Run E2E tests
      run: |
        npm run build
        npm run start & npx wait-on http://localhost:3000
        cypress run
```

---

## 8. Boas Práticas

### 8.1. Organização de Testes

- Seguir padrão AAA (Arrange, Act, Assert)
- Um teste = uma assertiva
- Nomes descritivos para testes
- Agrupar testes relacionados
- Manter independência entre testes

### 8.2. Mocks e Fixtures

- Criar dados realistas
- Limpar dados após cada teste
- Isolar dependências externas
- Documentar comportamento esperado

### 8.3. Performance

- Otimizar setup/teardown
- Paralelizar testes quando possível
- Monitorar tempo de execução
- Cache de dependências no CI

---

## 9. Troubleshooting

### 9.1. Problemas Comuns

1. **Falhas Intermitentes**
   - Verificar timing/async
   - Checar limpeza de dados
   - Validar mocks

2. **Problemas de Performance**
   - Reduzir setup redundante
   - Otimizar queries
   - Ajustar timeouts

3. **Falhas no CI**
   - Verificar logs completos
   - Validar variáveis de ambiente
   - Confirmar versões de dependências

### 9.2. Debugging

```python
# pytest.ini
[pytest]
log_cli = 1
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

### 9.3. Logs e Relatórios

- Usar ferramentas de coverage
- Gerar relatórios HTML
- Integrar com dashboards
- Monitorar tendências

---

## Anexos

### A. Cheatsheet de Comandos

```bash
# Backend Tests
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest -k "test_login"          # Run specific test
pytest --cov                    # Coverage report

# Frontend Tests
npm test                        # Run Jest tests
npm run test:watch             # Watch mode
npm run test:coverage          # Coverage report

# E2E Tests
npm run cypress               # Open Cypress
npm run cypress:run          # Headless mode
npm run cypress:record       # Record results

# Performance Tests
k6 run performance/login.js  # Run k6 tests
```

### B. Estrutura de Diretórios

```
tests/
├── backend/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_documents.py
│   └── test_payments.py
├── frontend/
│   ├── __tests__/
│   │   ├── components/
│   │   └── hooks/
│   └── setup.ts
├── e2e/
│   ├── integration/
│   └── support/
└── performance/
    ├── scenarios/
    └── data/
```

### C. Métricas e KPIs

- Cobertura de código (meta: >80%)
- Tempo de execução (<10min no CI)
- Taxa de sucesso (>99%)
- Performance baseline
  - Tempo de resposta API (<200ms)
  - Throughput (>100 req/s)
  - Erro rate (<1%)

---

> Este documento serve como guia completo para implementação e manutenção dos testes de integração no projeto SaberAngola, garantindo qualidade e confiabilidade do sistema.