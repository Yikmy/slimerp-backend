from rest_framework import serializers

from kernel.rbac.models import Permission, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'is_system']


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    company_id = serializers.UUIDField()
    role_name = serializers.CharField(max_length=100)


class GrantPermissionSerializer(serializers.Serializer):
    company_id = serializers.UUIDField()
    role_name = serializers.CharField(max_length=100)
    permission_code = serializers.CharField(max_length=120)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'description']
