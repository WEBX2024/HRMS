from django.contrib import admin
from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'tenant', 'status', 'created_at', 'expires_at', 'created_by')
    list_filter = ('status', 'created_at', 'tenant')
    search_fields = ('email', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('id', 'token', 'created_at', 'sent_at', 'accepted_at', 'revoked_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'tenant', 'user', 'email', 'assigned_role')
        }),
        ('Status', {
            'fields': ('status', 'token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'sent_at', 'expires_at', 'accepted_at', 'revoked_at')
        }),
        ('Audit', {
            'fields': ('created_by', 'revoked_by', 'invitation_metadata')
        }),
    )
    
    def has_add_permission(self, request):
        # Invitations should be created through API, not admin
        return False
