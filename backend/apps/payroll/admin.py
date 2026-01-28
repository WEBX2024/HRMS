"""
Payroll admin configuration.
"""
from django.contrib import admin
from .models import SalaryStructure, EmployeeSalary, PayrollRecord


@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'tenant', 'is_active', 'created_at']
    list_filter = ['tenant', 'is_active']
    search_fields = ['name']


@admin.register(EmployeeSalary)
class EmployeeSalaryAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'gross_salary', 'net_salary',
        'effective_from', 'is_current'
    ]
    list_filter = ['tenant', 'is_current', 'effective_from']
    search_fields = ['employee__employee_id', 'employee__user__email']


@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'month', 'year', 'gross_salary',
        'net_salary', 'is_processed'
    ]
    list_filter = ['tenant', 'year', 'month', 'is_processed']
    search_fields = ['employee__employee_id']
