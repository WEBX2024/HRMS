"""
Role models for RBAC system.
"""
import uuid
from django.db import models
from core.models.base import TenantBaseModel
from core.utils.constants import UserRoles


class Role(TenantBaseModel):
    """
    Role model for defining user roles within a tenant.
    Roles are tenant-specific and can have custom permissions.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="Display name of the role")
    code = models.CharField(
        max_length=50,
        choices=UserRoles.CHOICES,
        help_text="System code for the role"
    )
    description = models.TextField(blank=True)
    
    # Permissions (JSON field for flexible permission structure)
    permissions = models.JSONField(
        default=list,
        blank=True,
        help_text="List of permission codes"
    )
    
    # Priority (higher number = more authority)
    priority = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'roles'
        ordering = ['-priority', 'name']
        unique_together = [['tenant', 'code']]
        indexes = [
            models.Index(fields=['tenant', 'code']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class UserRole(TenantBaseModel):
    """
    User-Role association.
    Links users to their roles within a tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_assignments'
    )
    
    # Optional: Role can be assigned for specific department/team
    department = models.ForeignKey(
        'employees.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="If set, role applies only to this department"
    )
    
    # Validity period
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_roles'
        ordering = ['-created_at']
        unique_together = [['user', 'role', 'tenant']]
        indexes = [
            models.Index(fields=['user', 'tenant']),
            models.Index(fields=['role', 'tenant']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name}"
    
    def is_valid(self):
        """Check if role assignment is currently valid"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.valid_from and today < self.valid_from:
            return False
        if self.valid_until and today > self.valid_until:
            return False
        
        return True
