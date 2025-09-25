from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.DocumentListCreateView.as_view(), name='document-list-create'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('templates/', views.TemplateListView.as_view(), name='template-list'),
    path('generate/', views.generate_document, name='generate-document'),
]