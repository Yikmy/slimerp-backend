from rest_framework import views, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kernel.system_config.services import config_service
from kernel.system_config.models import ConfigScope
from kernel.company.models import Company

class ConfigSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
    value = serializers.JSONField(required=True)
    scope = serializers.ChoiceField(choices=ConfigScope.choices, default=ConfigScope.GLOBAL)
    company_id = serializers.IntegerField(required=False, allow_null=True)
    module = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)

class ConfigQuerySerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
    scope = serializers.ChoiceField(choices=ConfigScope.choices, default=ConfigScope.GLOBAL)
    company_id = serializers.IntegerField(required=False, allow_null=True)
    module = serializers.CharField(required=False, allow_null=True)


class ConfigAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ConfigQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        company = None
        if data.get('company_id'):
            company = Company.objects.filter(id=data['company_id']).first()
            if not company:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            value = config_service.get(
                key=data['key'],
                scope=data['scope'],
                company=company,
                module=data.get('module')
            )
            return Response({"key": data['key'], "value": value})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        # Note: in real app, only system admin can set configs
        serializer = ConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        company = None
        if data.get('company_id'):
            company = Company.objects.filter(id=data['company_id']).first()
            if not company:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        config_service.set(
            key=data['key'],
            value=data['value'],
            scope=data['scope'],
            company=company,
            module=data.get('module'),
            description=data.get('description', '')
        )
        return Response({"message": "Configuration updated successfully"})


class ModuleSwitchAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        module_name = request.query_params.get('module')
        if not module_name:
            return Response({"error": "module parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        company_id = request.query_params.get('company_id')
        company = None
        if company_id:
            company = Company.objects.filter(id=company_id).first()
            
        is_enabled = config_service.is_module_enabled(module_name, company=company)
        return Response({
            "module": module_name,
            "is_enabled": is_enabled,
            "company_id": company_id
        })
