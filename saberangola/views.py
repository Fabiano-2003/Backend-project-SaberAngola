from django.shortcuts import render
from django.conf import settings
from authentication.models import User
from documents.models import Document, Template
from payments.models import Subscription


def dashboard_view(request):
    """
    Dashboard view with system statistics and management links
    """
    # Get system statistics
    context = {
        'user_count': User.objects.count(),
        'document_count': Document.objects.count(),
        'template_count': Template.objects.filter(is_active=True).count(),
        'subscription_count': Subscription.objects.filter(status='ACTIVE').count(),
        'environment': 'Desenvolvimento' if settings.DEBUG else 'Produção',
    }
    
    return render(request, 'dashboard.html', context)