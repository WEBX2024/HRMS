"""
Payroll models (MVP structure only).
Full payroll processing to be implemented in Phase 2.
"""
import uuid
from django.db import models
from core.models.base import TenantBaseModel


class SalaryStructure(TenantBaseModel):
    """Salary structure template"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Components stored as JSON
    # Example: {"basic": 50000, "hra": 20000, "da": 10000, "allowances": 5000}
    components = models.JSONField(
        default=dict,
        help_text="Salary components and amounts"
    )
    
    # Deductions
    # Example: {"pf": 0.12, "tax": 0.10}
    deductions = models.JSONField(
        default=dict,
        help_text="Deduction types and percentages/amounts"
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'salary_structures'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def calculate_gross_salary(self):
        """Calculate gross salary from components"""
        return sum(self.components.values())


class EmployeeSalary(TenantBaseModel):
    """Employee salary assignment"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='salary_records'
    )
    
    salary_structure = models.ForeignKey(
        SalaryStructure,
        on_delete=models.PROTECT,
        related_name='employee_assignments'
    )
    
    # Salary details
    gross_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Gross monthly salary"
    )
    net_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Net monthly salary after deductions"
    )
    
    # Custom components (overrides from structure)
    custom_components = models.JSONField(
        default=dict,
        blank=True,
        help_text="Employee-specific component overrides"
    )
    
    # Validity
    effective_from = models.DateField(db_index=True)
    effective_until = models.DateField(null=True, blank=True)
    
    is_current = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'employee_salaries'
        ordering = ['-effective_from']
        indexes = [
            models.Index(fields=['employee', 'is_current']),
            models.Index(fields=['effective_from']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.gross_salary}"


class PayrollRecord(TenantBaseModel):
    """
    Payroll record for a specific month (Placeholder for MVP).
    Full implementation in Phase 2.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )
    
    # Period
    month = models.IntegerField()
    year = models.IntegerField()
    
    # Amounts
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Breakdown
    components_breakdown = models.JSONField(default=dict)
    deductions_breakdown = models.JSONField(default=dict)
    
    # Status
    is_processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payroll_records'
        ordering = ['-year', '-month']
        unique_together = [['employee', 'month', 'year', 'tenant']]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}/{self.year}"
