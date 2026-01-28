"""
Authentication serializers.
"""
from rest_framework import serializers
from apps.users.models import User
from apps.roles.models import Role, UserRole


class UserSerializer(serializers.ModelSerializer):
    """User serializer for responses"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'profile_picture', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class LoginSerializer(serializers.Serializer):
    """Login request serializer"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LoginResponseSerializer(serializers.Serializer):
    """Login response serializer"""
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
    tenant_id = serializers.UUIDField(allow_null=True)
    tenant_name = serializers.CharField(allow_null=True)
    roles = serializers.ListField(child=serializers.CharField())


class TokenRefreshSerializer(serializers.Serializer):
    """Token refresh request serializer"""
    refresh = serializers.CharField(required=True)


class TokenRefreshResponseSerializer(serializers.Serializer):
    """Token refresh response serializer"""
    access = serializers.CharField()
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    """Change password request serializer"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Extended user profile serializer"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    tenant_name = serializers.CharField(source='tenant.name', read_only=True, allow_null=True)
    roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'profile_picture', 'tenant_name', 'roles',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'last_login']
    
    def get_roles(self, obj):
        """Get user roles"""
        user_roles = UserRole.objects.filter(
            user=obj,
            is_deleted=False
        ).select_related('role')
        return [ur.role.name for ur in user_roles]
