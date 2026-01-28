"""
Leave management models.
"""
import uuid
from django.db import models
from django.utils import timezone
from core.models.base import TenantBaseModel
from core.utils.constants import LeaveStatus, LeaveTypes


class LeaveType(TenantBaseModel):
    """Leave type configuration"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, choices=LeaveTypes.CHOICES)
    description = models.TextField(blank=True)
    
    # Allocation
    days_per_year = models.IntegerField(help_text="Annual leave allocation")
    max_carry_forward = models.IntegerField(
        default=0,
        help_text="Max days that can be carried to next year"
    )
    
    # Rules
    requires_approval = models.BooleanField(default=True)
    min_days_notice = models.IntegerField(
        default=1,
        help_text="Minimum days notice required"
    )
    max_consecutive_days = models.IntegerField(
        default=30,
        help_text="Maximum consecutive days allowed"
    )
    
    # Applicability
    is_paid = models.BooleanField(default=True)
    applicable_after_months = models.IntegerField(
        default=0,
        help_text="Applicable after X months of employment"
    )
    
    # Gender specific (for maternity/paternity)
    gender_specific = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('', 'All'),
            ('MALE', 'Male Only'),
            ('FEMALE', 'Female Only'),
        ]
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'leave_types'
        ordering = ['name']
        unique_together = [['tenant', 'code']]
    
    def __str__(self):
        return self.name


class LeaveBalance(TenantBaseModel):
    """Employee leave balance tracking"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='balances'
    )
    
    year = models.IntegerField(help_text="Financial year")
    
    # Balance tracking
    total_days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Total allocated days"
    )
    used_days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Days used"
    )
    pending_days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Days in pending requests"
    )
    
    class Meta:
        db_table = 'leave_balances'
        ordering = ['-year']
        unique_together = [['employee', 'leave_type', 'year', 'tenant']]
        indexes = [
            models.Index(fields=['employee', 'year']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type.name} - {self.year}"
    
    def get_available_days(self):
        """Calculate available leave days"""
        return self.total_days - self.used_days - self.pending_days
    
    def can_apply(self, days):
        """Check if employee can apply for given days"""
        return self.get_available_days() >= days


class LeaveRequest(TenantBaseModel):
    """Leave request/application"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.ForeignKey(
        LeaveType,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    
    # Dates
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    days = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Number of leave days"
    )
    
    # Details
    reason = models.TextField()
    contact_during_leave = models.CharField(max_length=200, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=LeaveStatus.CHOICES,
        default=LeaveStatus.PENDING,
        db_index=True
    )
    
    # Approval workflow
    approved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Cancellation
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'leave_requests'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['tenant', 'employee', 'status']),
            models.Index(fields=['tenant', 'start_date', 'end_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type.name} - {self.start_date}"
    
    def approve(self, approved_by):
        """Approve leave request"""
        self.status = LeaveStatus.APPROVED
        self.approved_by = approved_by
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])
    
    def reject(self, rejected_by, reason):
        """Reject leave request"""
        self.status = LeaveStatus.REJECTED
        self.approved_by = rejected_by
        self.approved_at = timezone.now()
        self.rejection_reason = reason
        self.save(update_fields=[
            'status', 'approved_by', 'approved_at',
            'rejection_reason', 'updated_at'
        ])
    
    def cancel(self, reason):
        """Cancel leave request"""
        self.status = LeaveStatus.CANCELLED
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save(update_fields=[
            'status', 'cancelled_at', 'cancellation_reason', 'updated_at'
        ])
