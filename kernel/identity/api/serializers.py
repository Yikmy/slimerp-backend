from rest_framework import serializers
from django.contrib.auth import get_user_model
from kernel.company.api.serializers import CompanySerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'last_login', 'created_at']
        read_only_fields = ['id', 'created_at', 'last_login']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class CompanyAccessSerializer(serializers.Serializer):
    id = serializers.UUIDField(source='company.id')
    name = serializers.CharField(source='company.name')
    is_default = serializers.BooleanField()

class MeResponseSerializer(serializers.Serializer):
    """
    Serializer for 'me' endpoint response structure.
    """
    user = UserSerializer()
    companies = CompanyAccessSerializer(many=True)
    roles = serializers.ListField(child=serializers.CharField(), allow_empty=True) # Placeholder
