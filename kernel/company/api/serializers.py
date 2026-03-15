from rest_framework import serializers
from kernel.company.models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'code', 'tax_id', 'currency', 'created_at']
        read_only_fields = ['id', 'created_at']

class CompanySwitchSerializer(serializers.Serializer):
    company_id = serializers.UUIDField(required=True)
