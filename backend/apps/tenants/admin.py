"""
Tenant admin configuration.
"""
from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'subscription_plan', 'is_active',
        'max_employees', 'created_at'
    ]
    list_filter = ['subscription_plan', 'is_active', 'is_trial', 'country']
    search_fields = ['name', 'code', 'email', 'subdomain']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'subdomain', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Address', {
            'fields': (
                'address_line1', 'address_line2', 'city',
                'state', 'country', 'postal_code'
            )
        }),
        ('Subscription', {
            'fields': (
                'subscription_plan', 'max_employees', 'max_storage_mb',
                'is_trial', 'trial_ends_at'
            )
        }),
        ('Branding', {
            'fields': ('logo', 'primary_color')
        }),
        ('Settings', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
