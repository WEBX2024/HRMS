"""
Invitation model for employee onboarding
"""
import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from core.utils.constants import INVITATION_STATUS


class Invitation(models.Model):
    """
    Employee invitation system for secure onboarding.
    Employees cannot self-register; they must be invited by HR/Admin.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Tenant & User
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    
    # Invitation Details
    email = models.EmailField()  # Denormalized for validation
    token = models.CharField(max_length=255, unique=True, db_index=True)
    
    # Role Pre-assignment
    assigned_role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invitations'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=INVITATION_STATUS,
        default='CREATED',
        db_index=True
    )
    # CREATED, SENT, EXPIRED, ACCEPTED, REVOKED
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(db_index=True)  # 7 days from creation
    accepted_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    
    # Audit
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_invitations'
    )
    revoked_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='revoked_invitations'
    )
    
    # Metadata
    invitation_metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="IP address, user agent, etc."
    )
    
    class Meta:
        db_table = 'invitations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['tenant', 'status']),
            models.Index(fields=['email', 'status']),
            models.Index(fields=['expires_at']),
        ]
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'
    
    def __str__(self):
        return f"Invitation for {self.email} - {self.status}"
    
    def save(self, *args, **kwargs):
        # Set expiration to 7 days from now if not set
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if invitation has expired"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if invitation is valid for use"""
        return (
            self.status in ['CREATED', 'SENT'] and
            not self.is_expired()
        )
    
    def mark_as_sent(self):
        """Mark invitation as sent"""
        self.status = 'SENT'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at'])
    
    def mark_as_accepted(self):
        """Mark invitation as accepted"""
        self.status = 'ACCEPTED'
        self.accepted_at = timezone.now()
        self.save(update_fields=['status', 'accepted_at'])
    
    def revoke(self, revoked_by):
        """Revoke the invitation"""
        self.status = 'REVOKED'
        self.revoked_at = timezone.now()
        self.revoked_by = revoked_by
        self.save(update_fields=['status', 'revoked_at', 'revoked_by'])
