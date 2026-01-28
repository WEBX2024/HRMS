"""
Employees admin configuration.
"""
from django.contrib import admin
from .models import Department, Designation, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'tenant', 'head', 'parent', 'created_at']
    list_filter = ['tenant', 'parent']
    search_fields = ['name', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['title', 'code', 'tenant', 'level', 'created_at']
    list_filter = ['tenant', 'level']
    search_fields = ['title', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee_id', 'user', 'department', 'designation',
        'status', 'date_of_joining'
    ]
    list_filter = ['status', 'employment_type', 'department', 'tenant']
    search_fields = [
        'employee_id', 'user__email', 'user__first_name', 'user__last_name'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tenant', 'user', 'employee_id', 'status')
        }),
        ('Organization', {
            'fields': ('department', 'designation', 'manager', 'employment_type')
        }),
        ('Employment Dates', {
            'fields': ('date_of_joining', 'date_of_leaving')
        }),
        ('Personal Information', {
            'fields': (
                'date_of_birth', 'gender', 'blood_group', 'marital_status'
            )
        }),
        ('Contact Information', {
            'fields': (
                'personal_email', 'phone_primary', 'phone_secondary'
            )
        }),
        ('Address', {
            'fields': (
                'current_address', 'permanent_address',
                'city', 'state', 'country', 'postal_code'
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 'emergency_contact_relationship',
                'emergency_contact_phone'
            )
        }),
        ('Bank Details', {
            'fields': (
                'bank_name', 'bank_account_number',
                'bank_ifsc_code', 'pan_number'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('additional_info',),
            'classes': ('collapse',)
        }),
    )
