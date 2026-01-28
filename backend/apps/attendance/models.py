"""
Attendance models for time tracking.
"""
import uuid
from django.db import models
from django.utils import timezone
from core.models.base import TenantBaseModel
from core.utils.constants import AttendanceStatus


class AttendancePolicy(TenantBaseModel):
    """Attendance policy configuration for tenant"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Working hours
    work_hours_per_day = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=8.00
    )
    work_days_per_week = models.IntegerField(default=5)
    
    # Timing rules
    standard_check_in_time = models.TimeField(help_text="e.g., 09:00")
    standard_check_out_time = models.TimeField(help_text="e.g., 18:00")
    grace_period_minutes = models.IntegerField(
        default=15,
        help_text="Grace period for late arrival"
    )
    
    # Half day rules
    half_day_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=4.00
    )
    
    # Weekend configuration
    weekend_days = models.JSONField(
        default=list,
        help_text="List of weekend day numbers (0=Monday, 6=Sunday)"
    )
    
    # Overtime
    allow_overtime = models.BooleanField(default=False)
    overtime_multiplier = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.5
    )
    
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'attendance_policies'
        ordering = ['-is_default', 'name']
    
    def __str__(self):
        return self.name


class Attendance(TenantBaseModel):
    """Daily attendance record"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    
    date = models.DateField(db_index=True)
    
    # Check-in/out times
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    
    # Calculated fields
    work_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.CHOICES,
        default=AttendanceStatus.ABSENT
    )
    
    # Location (optional - for future geo-tracking)
    check_in_location = models.JSONField(null=True, blank=True)
    check_out_location = models.JSONField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Approval (for manual entries)
    is_manual_entry = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_attendance'
    )
    
    class Meta:
        db_table = 'attendance'
        ordering = ['-date']
        unique_together = [['employee', 'date', 'tenant']]
        indexes = [
            models.Index(fields=['tenant', 'employee', 'date']),
            models.Index(fields=['tenant', 'date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
    
    def calculate_work_hours(self):
        """Calculate work hours from check-in and check-out"""
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            hours = delta.total_seconds() / 3600
            self.work_hours = round(hours, 2)
            return self.work_hours
        return 0.00
    
    def is_late(self, policy):
        """Check if employee was late"""
        if not self.check_in or not policy:
            return False
        
        check_in_time = self.check_in.time()
        grace_time = (
            timezone.datetime.combine(timezone.now().date(), policy.standard_check_in_time) +
            timezone.timedelta(minutes=policy.grace_period_minutes)
        ).time()
        
        return check_in_time > grace_time


class Holiday(TenantBaseModel):
    """Company holidays"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateField(db_index=True)
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(
        default=True,
        help_text="If False, employees can choose to work"
    )
    
    class Meta:
        db_table = 'holidays'
        ordering = ['date']
        unique_together = [['tenant', 'date']]
    
    def __str__(self):
        return f"{self.name} - {self.date}"
