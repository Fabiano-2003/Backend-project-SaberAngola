# Referências e Recursos - SaberAngola

## Sumário

1. Documentação Oficial
2. Tutoriais e Guias
3. Bibliotecas e Frameworks
4. Ferramentas de Desenvolvimento
5. Segurança e Boas Práticas
6. Recursos de Aprendizado
7. Comunidade e Suporte
8. Exemplos e Repositórios
9. APIs e Integrações
10. Recursos de Deploy

---

## 1. Documentação Oficial

### 1.1. Backend (Django + DRF)

#### Django Framework
- [Django Documentation](https://docs.djangoproject.com/)
  - Models e ORM
  - Views e Templates
  - Forms e Validação
  - Admin Interface
  - Security
  - Testing
  - Deployment

#### Django REST Framework
- [DRF Documentation](https://www.django-rest-framework.org/)
  - Serializers
  - Views
  - Authentication
  - Permissions
  - Viewsets & Routers
  - Filtering
  - Pagination

#### SimpleJWT
- [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
  - Token Configuration
  - Views & URLs
  - Blacklisting
  - Custom Claims

### 1.2. Frontend (Next.js)

#### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
  - Pages & Routing
  - Data Fetching
  - API Routes
  - Deployment
  - Static Generation
  - Server-side Rendering

#### React
- [React Documentation](https://react.dev/)
  - Components
  - Hooks
  - Context
  - Performance
  - Testing
  - Accessibility

### 1.3. Infraestrutura

#### AWS Services
- [AWS Documentation](https://docs.aws.amazon.com/)
  - ECS
  - S3
  - RDS
  - ElastiCache
  - CloudFront
  - Route53

#### Docker
- [Docker Documentation](https://docs.docker.com/)
  - Containers
  - Images
  - Compose
  - Networks
  - Volumes

---

## 2. Tutoriais e Guias

### 2.1. Django + DRF

#### Iniciando com Django
1. [Tutorial Oficial Django](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
2. [Django Girls Tutorial](https://tutorial.djangogirls.org/)
3. [Real Python Django Tutorials](https://realpython.com/tutorials/django/)

#### API REST com DRF
1. [Tutorial Oficial DRF](https://www.django-rest-framework.org/tutorial/1-serialization/)
2. [Build an API with DRF](https://www.django-rest-framework.org/tutorial/quickstart/)
3. [Advanced DRF Features](https://www.django-rest-framework.org/api-guide/viewsets/)

### 2.2. Next.js

#### Fundamentos
1. [Learn Next.js](https://nextjs.org/learn)
2. [Pages and Routing](https://nextjs.org/docs/routing/introduction)
3. [Data Fetching](https://nextjs.org/docs/basic-features/data-fetching)

#### Avançado
1. [API Routes](https://nextjs.org/docs/api-routes/introduction)
2. [Authentication](https://nextjs.org/docs/authentication)
3. [Deployment](https://nextjs.org/docs/deployment)

### 2.3. DevOps

#### CI/CD
1. [GitHub Actions Guide](https://docs.github.com/en/actions)
2. [AWS Deployment Guide](https://aws.amazon.com/getting-started/hands-on/)
3. [Docker Compose Guide](https://docs.docker.com/compose/gettingstarted/)

---

## 3. Bibliotecas e Frameworks

### 3.1. Backend Python

#### Essenciais
```python
# requirements.txt
Django==5.0.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
django-filter==23.5.0
```

#### Documentos
```python
python-docx==0.8.11
reportlab==4.0.4
openpyxl==3.1.2
pypandoc==1.11
```

#### AWS
```python
boto3==1.28.0
django-storages==1.14.2
```

#### Tarefas Assíncronas
```python
celery==5.3.4
redis==5.0.1
```

#### Segurança
```python
django-ratelimit==4.1.0
bleach==6.0.0
```

### 3.2. Frontend JavaScript

#### Dependências Core
```json
{
  "dependencies": {
    "next": "13.4.19",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "1.4.0",
    "swr": "2.2.0"
  }
}
```

#### UI/UX
```json
{
  "dependencies": {
    "@tailwindcss/forms": "0.5.4",
    "@headlessui/react": "1.7.15",
    "@heroicons/react": "2.0.18"
  }
}
```

#### Forms e Validação
```json
{
  "dependencies": {
    "formik": "2.4.3",
    "yup": "1.2.0"
  }
}
```

---

## 4. Ferramentas de Desenvolvimento

### 4.1. IDEs e Editores

#### Visual Studio Code
- Extensions:
  - Python
  - Pylance
  - Django
  - ES7+ React/Redux/GraphQL
  - Prettier
  - ESLint
  - GitLens

#### PyCharm
- Features:
  - Django Support
  - Database Tools
  - REST Client
  - Docker Integration
  - Test Runner

### 4.2. Ferramentas CLI

#### Backend
```bash
# Django Management
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py test

# Virtual Environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Frontend
```bash
# Next.js Development
npm run dev
npm run build
npm run start
npm run lint

# Package Management
npm install
npm update
npm audit fix
```

### 4.3. Docker Tools

```bash
# Container Management
docker-compose up -d
docker-compose down
docker-compose logs -f

# Image Management
docker build -t saberangola-backend .
docker push registry.example.com/saberangola-backend
```

---

## 5. Segurança e Boas Práticas

### 5.1. Checklists de Segurança

#### Django Security
1. SECRET_KEY seguro
2. DEBUG=False em produção
3. ALLOWED_HOSTS configurado
4. SECURE_SSL_REDIRECT=True
5. SESSION_COOKIE_SECURE=True
6. CSRF_COOKIE_SECURE=True
7. X-Frame-Options header
8. XSS Protection
9. Content Security Policy

#### API Security
1. Rate Limiting
2. Token Authentication
3. CORS Configuration
4. Input Validation
5. Output Sanitization
6. Error Handling
7. Logging
8. SSL/TLS
9. API Versioning

### 5.2. Código Seguro

#### Python/Django
```python
# Exemplo de validação segura
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_user_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
```

#### JavaScript/React
```javascript
// Exemplo de sanitização XSS
import DOMPurify from 'dompurify';

const sanitizeContent = (content) => {
  return DOMPurify.sanitize(content);
};
```

---

## 6. Recursos de Aprendizado

### 6.1. Cursos Online

#### Django
1. [Django for Everybody (Coursera)](https://www.coursera.org/specializations/django)
2. [Django Web Framework (edX)](https://www.edx.org/learn/django)
3. [Complete Django Developer (Udemy)](https://www.udemy.com/course/complete-django-developer-course/)

#### Next.js
1. [Next.js & React (Udemy)](https://www.udemy.com/course/nextjs-react-the-complete-guide/)
2. [Fullstack Next.js (Frontend Masters)](https://frontendmasters.com/courses/fullstack-nextjs/)
3. [React & Next.js (Pluralsight)](https://www.pluralsight.com/courses/react-nextjs)

### 6.2. Livros Recomendados

#### Backend Development
1. "Two Scoops of Django"
2. "Django for APIs"
3. "Django for Professionals"
4. "Test-Driven Development with Python"

#### Frontend Development
1. "Next.js in Action"
2. "Full Stack React with Next.js"
3. "React Hooks in Action"
4. "Testing React Applications"

---

## 7. Comunidade e Suporte

### 7.1. Fóruns e Comunidades

#### Django/Python
- [Django Forum](https://forum.djangoproject.com/)
- [Django Developers Google Group](https://groups.google.com/forum/#!forum/django-developers)
- [Reddit r/django](https://reddit.com/r/django)
- Stack Overflow Tags:
  - [django]
  - [drf]
  - [python]

#### Next.js/React
- [Next.js Discord](https://discord.gg/nextjs)
- [React Discord](https://discord.gg/react)
- [Next.js GitHub Discussions](https://github.com/vercel/next.js/discussions)
- Stack Overflow Tags:
  - [next.js]
  - [reactjs]
  - [javascript]

### 7.2. Blogs e Newsletters

#### Development
1. [Real Python](https://realpython.com/search?q=django)
2. [TestDriven.io](https://testdriven.io/blog/)
3. [Django News](https://django-news.com)
4. [Next.js Blog](https://nextjs.org/blog)

#### Security
1. [OWASP Top 10](https://owasp.org/Top10/)
2. [Django Security Blog](https://www.djangoproject.com/weblog/categories/security/)
3. [Web Security Academy](https://portswigger.net/web-security)

---

## 8. Exemplos e Repositórios

### 8.1. Exemplos Django

#### Autenticação
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

#### Viewsets
```python
# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
```

### 8.2. Exemplos Next.js

#### API Routes
```typescript
// pages/api/auth/login.ts
import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' })
  }
  
  // Handler logic here
}
```

#### Data Fetching
```typescript
// pages/documents/[id].tsx
import { GetServerSideProps } from 'next'

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { id } = context.params
  const res = await fetch(`/api/documents/${id}`)
  const document = await res.json()
  
  return {
    props: { document }
  }
}
```

---

## 9. APIs e Integrações

### 9.1. APIs Externas

#### Documentação Swagger
```yaml
openapi: 3.0.0
info:
  title: SaberAngola API
  version: 1.0.0
paths:
  /api/documents:
    get:
      summary: Lista documentos
      responses:
        '200':
          description: Success
```

#### Postman Collections
```json
{
  "info": {
    "name": "SaberAngola API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Documents",
      "request": {
        "method": "GET",
        "url": "{{baseUrl}}/api/documents"
      }
    }
  ]
}
```

---

## 10. Recursos de Deploy

### 10.1. Infraestrutura como Código

#### Terraform
```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "documents" {
  bucket = "saberangola-documents"
}

resource "aws_ecs_cluster" "main" {
  name = "saberangola-cluster"
}
```

#### CloudFormation
```yaml
Resources:
  DocumentsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: saberangola-documents
```

### 10.2. Monitoramento

#### Prometheus
```yaml
scrape_configs:
  - job_name: 'django'
    static_configs:
      - targets: ['localhost:8000']
```

#### Grafana Dashboard
```json
{
  "dashboard": {
    "id": null,
    "title": "SaberAngola Metrics",
    "panels": []
  }
}
```

---

> Este documento serve como referência completa para recursos, ferramentas e documentação relacionados ao projeto SaberAngola. Mantenha-o atualizado conforme novas tecnologias e recursos são adicionados ao projeto.