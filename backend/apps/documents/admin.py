"""
Documents admin configuration.
"""
from django.contrib import admin
from .models import Document, DocumentCategory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'title', 'document_type', 'file_name',
        'is_verified', 'created_at'
    ]
    list_filter = ['document_type', 'is_verified', 'tenant']
    search_fields = [
        'employee__employee_id', 'title', 'file_name', 'document_number'
    ]
    readonly_fields = ['id', 'created_at', 'updated_at', 'verified_at']


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tenant', 'is_mandatory', 'created_at']
    list_filter = ['tenant', 'is_mandatory']
    search_fields = ['name']
