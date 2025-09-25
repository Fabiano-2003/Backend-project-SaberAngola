"""
Custom Admin Site for SaberAngola with enhanced dashboard statistics
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count, Sum
from django.http import HttpRequest
from django.template.response import TemplateResponse
from authentication.models import User
from documents.models import Document, Template
from payments.models import Subscription, Transaction


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
        }
        
        # Calculate total revenue
        total_revenue = Transaction.objects.filter(status='COMPLETED').aggregate(
            total=Sum('amount')
        )['total'] or 0
        stats['total_revenue'] = f"{total_revenue:.2f} AOA"
        
        # Add percentage calculations
        if stats['total_users'] > 0:
            stats['premium_percentage'] = round((stats['premium_users'] / stats['total_users']) * 100, 1)
        else:
            stats['premium_percentage'] = 0
            
        if stats['total_documents'] > 0:
            stats['completion_rate'] = round((stats['completed_documents'] / stats['total_documents']) * 100, 1)
        else:
            stats['completion_rate'] = 0

        # Merge with any extra context
        context = {
            'stats': stats,
            **(extra_context or {}),
        }
        
        return super().index(request, extra_context=context)


# Create instance of custom admin site
admin_site = SaberAngolaAdminSite(name='saberangola_admin')

# Import and register all admin classes
from authentication.admin import UserAdmin
from authentication.models import User
from documents.admin import TemplateAdmin, DocumentAdmin
from documents.models import Template, Document
from payments.admin import PlanAdmin, SubscriptionAdmin, TransactionAdmin
from payments.models import Plan, Subscription, Transaction
from users.admin import ProfileAdmin, ActivityAdmin
from users.models import Profile, Activity

# Register all models with their respective admin classes
admin_site.register(User, UserAdmin)
admin_site.register(Template, TemplateAdmin)
admin_site.register(Document, DocumentAdmin)
admin_site.register(Plan, PlanAdmin)
admin_site.register(Subscription, SubscriptionAdmin)
admin_site.register(Transaction, TransactionAdmin)
admin_site.register(Profile, ProfileAdmin)
admin_site.register(Activity, ActivityAdmin)