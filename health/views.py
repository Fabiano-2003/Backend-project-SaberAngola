from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import connection
from django.utils import timezone


class HealthCheckView(APIView):
    permission_classes = []
    
    def get(self, request):
        checks = {
            'database': self._check_database(),
            'timestamp': timezone.now().isoformat(),
            'version': getattr(settings, 'APP_VERSION', '1.0.0'),
        }
        
        status_code = status.HTTP_200_OK if checks['database'] else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return Response({
            'status': 'healthy' if status_code == 200 else 'unhealthy',
            'checks': checks
        }, status=status_code)
    
    def _check_database(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return True
        except Exception:
            return False
