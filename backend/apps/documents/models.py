"""
Document management models.
"""
import uuid
from django.db import models
from core.models.base import TenantBaseModel
from core.utils.constants import DocumentTypes


class Document(TenantBaseModel):
    """Employee document storage"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    employee = models.ForeignKey(
        'employees.Employee',
        on_delete=models.CASCADE,
        related_name='documents'
    )
    
    # Document details
    document_type = models.CharField(
        max_length=100,
        choices=DocumentTypes.CHOICES
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # File information
    file_path = models.CharField(
        max_length=500,
        help_text="Path to stored file"
    )
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    file_type = models.CharField(max_length=50, help_text="MIME type")
    
    # Metadata
    document_number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # Upload info
    uploaded_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents'
    )
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_documents'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant', 'employee']),
            models.Index(fields=['document_type']),
            models.Index(fields=['is_verified']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.title}"
    
    def is_expired(self):
        """Check if document is expired"""
        if not self.expiry_date:
            return False
        from django.utils import timezone
        return self.expiry_date < timezone.now().date()


class DocumentCategory(TenantBaseModel):
    """Custom document categories for tenant"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_mandatory = models.BooleanField(
        default=False,
        help_text="Required for all employees"
    )
    
    class Meta:
        db_table = 'document_categories'
        ordering = ['name']
        verbose_name_plural = 'Document Categories'
    
    def __str__(self):
        return self.name
