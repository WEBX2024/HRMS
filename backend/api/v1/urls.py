"""
API v1 URL Configuration
"""
from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('auth/', include('api.v1.auth.urls')),
    # Additional endpoints will be added here
]
