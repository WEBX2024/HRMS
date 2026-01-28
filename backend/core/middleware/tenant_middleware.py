"""
Tenant Middleware for Multi-Tenant HRMS SaaS Platform.
Extracts tenant context from JWT token and attaches to request.
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from core.utils.constants import ErrorMessages

logger = logging.getLogger(__name__)


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware to extract and attach tenant context to request.
    Tenant is resolved from JWT token payload.
    """
    
    def process_request(self, request):
        """
        Extract tenant from JWT token and attach to request.
        Super admins bypass tenant restriction.
        """
        request.tenant = None
        request.is_super_admin = False
        
        # Skip tenant check for public endpoints
        public_paths = [
            '/api/v1/auth/login',
            '/api/v1/auth/register',
            '/api/schema/',
            '/api/docs/',
            '/admin/',
        ]
        
        if any(request.path.startswith(path) for path in public_paths):
            return None
        
        # Try to authenticate using JWT
        jwt_auth = JWTAuthentication()
        
        try:
            # Get user and token from request
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if not auth_header.startswith('Bearer '):
                return None
            
            # Authenticate and get validated token
            validated_token = jwt_auth.get_validated_token(
                auth_header.split(' ')[1]
            )
            
            # Get user from token
            user = jwt_auth.get_user(validated_token)
            
            # Check if super admin
            if user.is_superuser:
                request.is_super_admin = True
                logger.info(f"Super admin access: {user.email}")
                return None
            
            # Extract tenant_id from token
            tenant_id = validated_token.get('tenant_id')
            
            if not tenant_id:
                logger.warning(f"No tenant_id in token for user: {user.email}")
                return None
            
            # Import here to avoid circular dependency
            from apps.tenants.models import Tenant
            
            try:
                tenant = Tenant.objects.get(id=tenant_id, is_active=True)
                request.tenant = tenant
                logger.debug(f"Tenant context set: {tenant.name} for user: {user.email}")
            except Tenant.DoesNotExist:
                logger.error(f"Tenant not found: {tenant_id}")
                raise AuthenticationFailed(ErrorMessages.TENANT_NOT_FOUND)
                
        except AuthenticationFailed:
            # Let DRF handle authentication errors
            pass
        except Exception as e:
            logger.exception(f"Error in tenant middleware: {e}")
        
        return None
    
    def process_response(self, request, response):
        """Clean up tenant context"""
        if hasattr(request, 'tenant'):
            delattr(request, 'tenant')
        if hasattr(request, 'is_super_admin'):
            delattr(request, 'is_super_admin')
        return response
