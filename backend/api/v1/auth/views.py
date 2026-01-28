"""
Authentication views.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from core.utils.exception_handler import success_response
from core.utils.constants import ErrorMessages, SuccessMessages
from apps.users.models import User
from apps.roles.models import UserRole
from .serializers import (
    LoginSerializer,
    LoginResponseSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
import logging

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """
    User login endpoint.
    Returns JWT access and refresh tokens with user info.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return success_response(
                data=None,
                message=ErrorMessages.INVALID_CREDENTIALS,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return success_response(
                data=None,
                message=ErrorMessages.INVALID_CREDENTIALS,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return success_response(
                data=None,
                message="Account is inactive",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        # Add custom claims
        if user.tenant:
            access['tenant_id'] = str(user.tenant.id)
            refresh['tenant_id'] = str(user.tenant.id)
        
        # Get user roles
        user_roles = UserRole.objects.filter(
            user=user,
            is_deleted=False
        ).select_related('role')
        roles = [ur.role.code for ur in user_roles]
        
        if roles:
            access['roles'] = roles
            refresh['roles'] = roles
        
        # Prepare response
        response_data = {
            'access': str(access),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
            'tenant_id': str(user.tenant.id) if user.tenant else None,
            'tenant_name': user.tenant.name if user.tenant else None,
            'roles': roles
        }
        
        # Update last login
        user.save(update_fields=['last_login'])
        
        logger.info(f"User logged in: {user.email}")
        
        return success_response(
            data=response_data,
            message=SuccessMessages.LOGIN_SUCCESS,
            status_code=status.HTTP_200_OK
        )


class LogoutView(APIView):
    """
    User logout endpoint.
    Blacklists the refresh token.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logger.info(f"User logged out: {request.user.email}")
            
            return success_response(
                data=None,
                message=SuccessMessages.LOGOUT_SUCCESS,
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return success_response(
                data=None,
                message="Logout successful",
                status_code=status.HTTP_200_OK
            )


class UserProfileView(APIView):
    """
    Get current user profile.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return success_response(
            data=serializer.data,
            message="Profile retrieved successfully",
            status_code=status.HTTP_200_OK
        )
    
    def put(self, request):
        """Update user profile"""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(
            data=serializer.data,
            message="Profile updated successfully",
            status_code=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Verify old password
        if not user.check_password(serializer.validated_data['old_password']):
            return success_response(
                data=None,
                message="Current password is incorrect",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        logger.info(f"Password changed for user: {user.email}")
        
        return success_response(
            data=None,
            message="Password changed successfully",
            status_code=status.HTTP_200_OK
        )
