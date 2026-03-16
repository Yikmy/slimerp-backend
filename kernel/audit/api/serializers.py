from rest_framework import serializers
from kernel.audit.models import AuditLog, LoginLog

class AuditLogSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = [f.name for f in AuditLog._meta.get_fields()]

class LoginLogSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = LoginLog
        fields = '__all__'
        read_only_fields = [f.name for f in LoginLog._meta.get_fields()]
