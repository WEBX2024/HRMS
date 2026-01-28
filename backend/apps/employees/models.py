"""
Employee models for HRMS.
"""
import uuid
from django.db import models
from core.models.base import TenantBaseModel
from core.utils.constants import EmployeeStatus, Gender


class Department(TenantBaseModel):
    """Department model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    # Department head
    head = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    
    # Parent department for hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments'
    )
    
    class Meta:
        db_table = 'departments'
        ordering = ['name']
        unique_together = [['tenant', 'code']]
        indexes = [
            models.Index(fields=['tenant', 'code']),
        ]
    
    def __str__(self):
        return self.name


class Designation(TenantBaseModel):
    """Designation/Job Title model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    level = models.IntegerField(default=1, help_text="Hierarchy level")
    
    class Meta:
        db_table = 'designations'
        ordering = ['-level', 'title']
        unique_together = [['tenant', 'code']]
    
    def __str__(self):
        return self.title


class Employee(TenantBaseModel):
    """
    Employee model - Core employee information.
    Links to User model for authentication.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Link to User
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    
    # Employee ID
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique employee identifier"
    )
    
    # Organization structure
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    
    # Reporting structure
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )
    
    # Employment details
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('FULL_TIME', 'Full Time'),
            ('PART_TIME', 'Part Time'),
            ('CONTRACT', 'Contract'),
            ('INTERN', 'Intern'),
        ],
        default='FULL_TIME'
    )
    
    # Personal information
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=Gender.CHOICES)
    blood_group = models.CharField(max_length=5, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[
            ('SINGLE', 'Single'),
            ('MARRIED', 'Married'),
            ('DIVORCED', 'Divorced'),
            ('WIDOWED', 'Widowed'),
        ],
        blank=True
    )
    
    # Contact information
    personal_email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=20)
    phone_secondary = models.CharField(max_length=20, blank=True)
    
    # Address
    current_address = models.TextField()
    permanent_address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_relationship = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Bank details
    bank_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_ifsc_code = models.CharField(max_length=20, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=EmployeeStatus.CHOICES,
        default=EmployeeStatus.ACTIVE
    )
    
    # Additional info (JSON for flexibility)
    additional_info = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['-date_of_joining']
        indexes = [
            models.Index(fields=['tenant', 'employee_id']),
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['department']),
            models.Index(fields=['manager']),
        ]
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
    
    def get_team_size(self):
        """Get number of direct reports"""
        return self.team_members.filter(is_deleted=False).count()
    
    def is_manager(self):
        """Check if employee is a manager"""
        return self.team_members.filter(is_deleted=False).exists()
