"""
Leave admin configuration.
"""
from django.contrib import admin
from .models import LeaveType, LeaveBalance, LeaveRequest


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'code', 'tenant', 'days_per_year',
        'is_paid', 'is_active'
    ]
    list_filter = ['tenant', 'is_paid', 'is_active']
    search_fields = ['name', 'code']


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'leave_type', 'year',
        'total_days', 'used_days', 'pending_days'
    ]
    list_filter = ['year', 'leave_type', 'tenant']
    search_fields = ['employee__employee_id', 'employee__user__email']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'leave_type', 'start_date', 'end_date',
        'days', 'status', 'approved_by'
    ]
    list_filter = ['status', 'leave_type', 'tenant', 'start_date']
    search_fields = ['employee__employee_id', 'employee__user__email', 'reason']
    readonly_fields = ['id', 'created_at', 'updated_at', 'approved_at']
