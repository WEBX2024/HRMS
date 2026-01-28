"""
Permission model for granular access control
"""
import uuid
from django.db import models


class Permission(models.Model):
    """
    System-wide permission definitions for RBAC.
    Permissions are assigned to roles, not directly to users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Permission Details
    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Format: 'module.action' e.g., 'employee.create', 'payroll.approve'"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Categorization
    module = models.CharField(
        max_length=50,
        db_index=True,
        help_text="employee, attendance, leave, payroll, etc."
    )
    action = models.CharField(
        max_length=50,
        help_text="view, create, update, delete, approve, etc."
    )
    
    # Flags
    is_system_permission = models.BooleanField(
        default=True,
        help_text="System permissions cannot be deleted"
    )
    is_active = models.BooleanField(default=True)
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'permissions'
        ordering = ['module', 'action']
        indexes = [
            models.Index(fields=['module', 'action']),
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate code from module and action if not set
        if not self.code and self.module and self.action:
            self.code = f"{self.module}.{self.action}"
        super().save(*args, **kwargs)
