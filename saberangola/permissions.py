from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user


class IsActiveSubscriber(BasePermission):
    """
    Custom permission to check if user has active subscription.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check if user has active subscription
        from payments.models import Subscription
        active_subscription = Subscription.objects.filter(
            user=request.user,
            status='ACTIVE'
        ).exists()
        
        return active_subscription or request.user.is_staff


class IsStaffOrReadOnly(BasePermission):
    """
    Custom permission to only allow staff users to write.
    """
    
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        return request.user.is_staff