from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from apps.users.models import User
from apps.documents.models import Document
from apps.payments.models import Payment


def dashboard_view(request):
    """
    Dashboard view with system statistics and management links
    """
    # Get system statistics
    context = {
        'user_count': User.objects.count(),
        'document_count': Document.objects.count(),
        'payment_count': Payment.objects.filter(status='completed').count(),
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
        'verified_users': User.objects.filter(is_verified=True).count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'total_documents': Document.objects.count(),
        'draft_documents': Document.objects.filter(status='draft').count(),
        'published_documents': Document.objects.filter(status='published').count(),
        'archived_documents': Document.objects.filter(status='archived').count(),
        'total_payments': Payment.objects.count(),
        'completed_payments': Payment.objects.filter(status='completed').count(),
        'failed_payments': Payment.objects.filter(status='failed').count(),
        'total_revenue': Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0,
    }
    
    # Add percentage calculations
    if stats['total_users'] > 0:
        stats['verified_percentage'] = round((stats['verified_users'] / stats['total_users']) * 100, 1)
    else:
        stats['verified_percentage'] = 0
        
    if stats['total_documents'] > 0:
        stats['publish_rate'] = round((stats['published_documents'] / stats['total_documents']) * 100, 1)
    else:
        stats['publish_rate'] = 0
    
    return JsonResponse(stats)