"""
Attendance admin configuration.
"""
from django.contrib import admin
from .models import AttendancePolicy, Attendance, Holiday


@admin.register(AttendancePolicy)
class AttendancePolicyAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'tenant', 'work_hours_per_day',
        'grace_period_minutes', 'is_default'
    ]
    list_filter = ['tenant', 'is_default']
    search_fields = ['name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'date', 'check_in', 'check_out',
        'work_hours', 'status'
    ]
    list_filter = ['status', 'date', 'tenant']
    search_fields = ['employee__employee_id', 'employee__user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'tenant', 'is_mandatory']
    list_filter = ['tenant', 'is_mandatory', 'date']
    search_fields = ['name']
