from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from authentication.models import User
from documents.models import Document, Template
from payments.models import Subscription, Transaction


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


@staff_member_required
def admin_stats_api(request):
    """
    API endpoint for admin dashboard statistics
    """
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    # Calculate statistics
    stats = {
        'total_users': User.objects.count(),
        'premium_users': User.objects.filter(is_premium=True).count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_documents': Document.objects.count(),
        'pending_documents': Document.objects.filter(status='pending').count(),
        'completed_documents': Document.objects.filter(status='completed').count(),
        'failed_documents': Document.objects.filter(status='failed').count(),
        'total_templates': Template.objects.count(),
        'active_templates': Template.objects.filter(is_active=True).count(),
        'total_transactions': Transaction.objects.count(),
        'completed_transactions': Transaction.objects.filter(status='COMPLETED').count(),
        'failed_transactions': Transaction.objects.filter(status='FAILED').count(),
        'active_subscriptions': Subscription.objects.filter(status='ACTIVE').count(),
        'total_revenue': Transaction.objects.filter(status='COMPLETED').aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }
    
    # Add percentage calculations
    if stats['total_users'] > 0:
        stats['premium_percentage'] = round((stats['premium_users'] / stats['total_users']) * 100, 1)
    else:
        stats['premium_percentage'] = 0
        
    if stats['total_documents'] > 0:
        stats['completion_rate'] = round((stats['completed_documents'] / stats['total_documents']) * 100, 1)
    else:
        stats['completion_rate'] = 0
    
    return JsonResponse(stats)