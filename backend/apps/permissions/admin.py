from django.contrib import admin
from .models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'module', 'action', 'is_system_permission', 'is_active')
    list_filter = ('module', 'action', 'is_system_permission', 'is_active')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Permission Details', {
            'fields': ('id', 'code', 'name', 'description')
        }),
        ('Categorization', {
            'fields': ('module', 'action')
        }),
        ('Flags', {
            'fields': ('is_system_permission', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of system permissions
        if obj and obj.is_system_permission:
            return False
        return super().has_delete_permission(request, obj)
