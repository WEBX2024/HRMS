from django.contrib import admin
from .models import PasswordResetToken, LoginAudit


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'created_at', 'expires_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'is_expired', 'created_at', 'tenant')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'ip_address')
    readonly_fields = ('id', 'token', 'created_at', 'expires_at', 'used_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('id', 'user', 'tenant')
        }),
        ('Token Details', {
            'fields': ('token', 'is_used', 'is_expired')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'used_at')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent')
        }),
    )
    
    def has_add_permission(self, request):
        return False


@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'ip_address', 'attempted_at', 'tenant')
    list_filter = ('status', 'attempted_at', 'tenant')
    search_fields = ('email', 'ip_address', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'user', 'tenant', 'email', 'status', 'failure_reason', 
                      'ip_address', 'user_agent', 'device_info', 'attempted_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('id', 'user', 'tenant', 'email')
        }),
        ('Attempt Details', {
            'fields': ('status', 'failure_reason')
        }),
        ('Request Metadata', {
            'fields': ('ip_address', 'user_agent', 'device_info')
        }),
        ('Timestamp', {
            'fields': ('attempted_at',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
