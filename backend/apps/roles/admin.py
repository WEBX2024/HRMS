"""
Roles admin configuration.
"""
from django.contrib import admin
from .models import Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'tenant', 'priority', 'created_at']
    list_filter = ['code', 'tenant', 'priority']
    search_fields = ['name', 'code', 'tenant__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'name', 'code', 'description', 'priority')
        }),
        ('Permissions', {
            'fields': ('permissions',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'tenant', 'department', 'valid_from', 'valid_until', 'created_at']
    list_filter = ['role', 'tenant', 'department']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'role__name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Assignment', {
            'fields': ('tenant', 'user', 'role', 'department')
        }),
        ('Validity', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        }),
    )
