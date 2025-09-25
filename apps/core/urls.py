from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

router = DefaultRouter()
router.register(r'settings', views.SettingViewSet, basename='setting')

urlpatterns = [
    path('', include(router.urls)),
]