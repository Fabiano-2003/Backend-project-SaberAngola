"""
Custom Admin Site for SaberAngola with enhanced dashboard statistics
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.http import HttpRequest
from django.template.response import TemplateResponse
from apps.users.models import User
from apps.documents.models import Document
from apps.payments.models import Payment


class SaberAngolaAdminSite(AdminSite):
    """
    Custom AdminSite that provides dashboard statistics context
    """
    site_header = 'SaberAngola Admin'
    site_title = 'SaberAngola Admin'
    index_title = 'Dashboard Administrativo'

    def index(self, request, extra_context=None):
        """
        Display the main admin index page with statistics.
        """
        # Calculate statistics for the dashboard
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
        }
        
        # Calculate total revenue
        total_revenue = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        stats['total_revenue'] = f"{total_revenue:.2f} AOA"
        
        # Add percentage calculations
        if stats['total_users'] > 0:
            stats['verified_percentage'] = round((stats['verified_users'] / stats['total_users']) * 100, 1)
        else:
            stats['verified_percentage'] = 0
            
        if stats['total_documents'] > 0:
            stats['publish_rate'] = round((stats['published_documents'] / stats['total_documents']) * 100, 1)
        else:
            stats['publish_rate'] = 0

        # Merge with any extra context
        context = {
            'stats': stats,
            **(extra_context or {}),
        }
        
        return super().index(request, extra_context=context)


# Create instance of custom admin site
admin_site = SaberAngolaAdminSite(name='saberangola_admin')