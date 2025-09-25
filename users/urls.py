from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('change-password/', views.change_password, name='change-password'),
]