"""
Tenant models for multi-tenant HRMS SaaS platform.
"""
import uuid
from django.db import models
from core.models.base import BaseModel
from core.utils.constants import SubscriptionPlans


class Tenant(BaseModel):
    """
    Tenant/Company model.
    Each tenant represents a separate organization using the HRMS.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Company name")
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique company code (used for employee IDs)"
    )
    subdomain = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Subdomain for tenant (e.g., acme.hrms.com)"
    )
    
    # Contact Information
    email = models.EmailField(help_text="Primary contact email")
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Subscription & Limits
    subscription_plan = models.CharField(
        max_length=50,
        choices=SubscriptionPlans.CHOICES,
        default=SubscriptionPlans.FREE
    )
    max_employees = models.IntegerField(default=10)
    max_storage_mb = models.IntegerField(default=100)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_trial = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    
    # Settings (JSON field for flexible configuration)
    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text="Tenant-specific settings"
    )
    
    # Branding
    logo = models.CharField(max_length=500, blank=True)
    primary_color = models.CharField(max_length=7, default='#1976d2')
    
    class Meta:
        db_table = 'tenants'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['subdomain']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_employee_count(self):
        """Get current employee count"""
        return self.employee_set.filter(is_deleted=False).count()
    
    def can_add_employee(self):
        """Check if tenant can add more employees"""
        if self.max_employees == -1:  # Unlimited
            return True
        return self.get_employee_count() < self.max_employees
    
    def update_subscription(self, plan):
        """Update subscription plan and limits"""
        self.subscription_plan = plan
        limits = SubscriptionPlans.LIMITS.get(plan, {})
        self.max_employees = limits.get('max_employees', 10)
        self.max_storage_mb = limits.get('max_storage_mb', 100)
        self.save(update_fields=['subscription_plan', 'max_employees', 'max_storage_mb', 'updated_at'])
