"""
URL configuration for saberangola project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import dashboard_view, admin_stats_api
from .admin import admin_site

# Swagger API Documentation Schema
schema_view = get_schema_view(
   openapi.Info(
      title="SaberAngola API",
      default_version='v1',
      description="API para gestão de documentos e serviços SaberAngola",
      terms_of_service="https://www.saberangola.ao/terms/",
      contact=openapi.Contact(email="contato@saberangola.ao"),
      license=openapi.License(name="Proprietary License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin Stats API (must come before admin/ to avoid being captured)
    path('admin/stats/', admin_stats_api, name='admin_stats_api'),
    
    # Admin Interface (custom admin site with stats context)
    path('admin/', admin_site.urls),
    
    # Dashboard
    path('', dashboard_view, name='dashboard'),
    
    # API Documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/payments/', include('apps.payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
