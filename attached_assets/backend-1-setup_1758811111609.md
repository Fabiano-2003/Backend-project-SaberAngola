# Backend Setup Inicial

## Configuração Base do Projeto Django

1. Settings Base
```python
# saberangola/settings/base.py
from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'storages',
    
    # Local apps
    'apps.users',
    'apps.documents',
    'apps.payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'saberangola.urls'

WSGI_APPLICATION = 'saberangola.wsgi.application'

AUTH_USER_MODEL = 'users.User'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

2. URLs Base
```python
# saberangola/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/payments/', include('apps.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

3. WSGI Configuration
```python
# saberangola/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saberangola.settings.production')

application = get_wsgi_application()
```

4. Requirements Base
```txt
# requirements/base.txt
Django==5.0.0
djangorestframework==3.14.0
django-cors-headers==4.3.0
django-filter==23.4
django-storages==1.14.2
djangorestframework-simplejwt==5.3.0
Pillow==10.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
redis==5.0.1
celery==5.3.6
boto3==1.33.6
```

5. Docker Compose
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
    env_file:
      - .env
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
    command: celery -A saberangola worker -l INFO
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - web
      - redis

volumes:
  postgres_data:
```