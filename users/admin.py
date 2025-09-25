from django.contrib import admin
from .models import Profile, Activity


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_of_birth', 'created_at')
    list_filter = ('created_at', 'date_of_birth')
    search_fields = ('user__email', 'user__name', 'phone', 'bio')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações de Perfil', {
            'fields': ('profile_picture', 'bio', 'phone', 'address', 'date_of_birth')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__email', 'user__name', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Ação', {
            'fields': ('user', 'action', 'timestamp')
        }),
        ('Detalhes', {
            'fields': ('details',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
    
    def has_add_permission(self, request):
        return False  # Activities should be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Activities should be read-only
