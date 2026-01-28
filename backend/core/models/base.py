"""
Base model classes for all HRMS models.
Provides common fields and functionality.
"""
import uuid
from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models.
    Includes UUID primary key, timestamps, audit fields, and soft delete.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        db_index=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def soft_delete(self):
        """Soft delete the record"""
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])
    
    def restore(self):
        """Restore a soft-deleted record"""
        self.is_deleted = False
        self.save(update_fields=['is_deleted', 'updated_at'])


class TenantBaseModel(BaseModel):
    """
    Abstract base model for tenant-scoped models.
    All business data should inherit from this.
    """
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        db_index=True
    )
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['tenant', '-created_at']),
            models.Index(fields=['tenant', 'is_deleted']),
        ]
