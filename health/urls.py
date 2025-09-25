from django.urls import path
from .views import HealthCheckView

app_name = 'health'

urlpatterns = [
    path('', HealthCheckView.as_view(), name='health-check'),
]