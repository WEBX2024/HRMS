"""
Authentication-related models: PasswordResetToken and LoginAudit
"""
import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from core.utils.constants import LOGIN_STATUS


class PasswordResetToken(models.Model):
    """
    Password reset token management for secure password recovery.
    Tokens are single-use and expire after 1 hour.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User & Tenant
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    
    # Token
    token = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Status
    is_used = models.BooleanField(default=False, db_index=True)
    is_expired = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True)  # 1 hour from creation
    used_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_used']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
    
    def __str__(self):
        return f"Password Reset for {self.user.email} - {'Used' if self.is_used else 'Active'}"
    
    def save(self, *args, **kwargs):
        # Set expiration to 1 hour from now if not set
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=1)
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if token is valid for use"""
        return (
            not self.is_used and
            not self.is_expired and
            timezone.now() <= self.expires_at
        )
    
    def mark_as_used(self):
        """Mark token as used"""
        self.is_used = True
        self.used_at = timezone.now()
        self.save(update_fields=['is_used', 'used_at'])


class LoginAudit(models.Model):
    """
    Login attempt tracking for security monitoring and compliance.
    Tracks both successful and failed login attempts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # User & Tenant (nullable if user not found)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='login_audits'
    )
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='login_audits'
    )
    email = models.EmailField(db_index=True)  # Store even if user not found
    
    # Attempt Details
    status = models.CharField(
        max_length=50,
        choices=LOGIN_STATUS,
        db_index=True
    )
    # SUCCESS, FAILED_INVALID_CREDENTIALS, FAILED_INACTIVE, FAILED_SUSPENDED, etc.
    
    failure_reason = models.CharField(max_length=255, blank=True)
    
    # Request Metadata
    ip_address = models.GenericIPAddressField(db_index=True)
    user_agent = models.TextField(blank=True)
    device_info = models.JSONField(default=dict, blank=True)
    
    # Timestamp
    attempted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'login_audits'
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['user', 'attempted_at']),
            models.Index(fields=['email', 'status']),
            models.Index(fields=['ip_address', 'attempted_at']),
            models.Index(fields=['status', 'attempted_at']),
        ]
        verbose_name = 'Login Audit'
        verbose_name_plural = 'Login Audits'
    
    def __str__(self):
        return f"{self.email} - {self.status} at {self.attempted_at}"
    
    @classmethod
    def log_attempt(cls, email, status, ip_address, user_agent='', user=None, tenant=None, failure_reason='', device_info=None):
        """
        Convenience method to log a login attempt
        """
        return cls.objects.create(
            email=email,
            status=status,
            ip_address=ip_address,
            user_agent=user_agent,
            user=user,
            tenant=tenant,
            failure_reason=failure_reason,
            device_info=device_info or {}
        )
