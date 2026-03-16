from rest_framework import viewsets, mixins, permissions
from kernel.audit.models import AuditLog, LoginLog
from kernel.audit.api.serializers import AuditLogSerializer, LoginLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows audit logs to be viewed.
    """
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['action', 'target_model', 'result', 'created_by']
    search_fields = ['details', 'target_object_id', 'ip_address']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # In a real multi-tenant system, we should filter by the user's company
        # user = self.request.user
        # if not user.is_superuser:
        #     return self.queryset.filter(company=user.company)
        return super().get_queryset()

class LoginLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows login logs to be viewed.
    """
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'username', 'ip_address']
    search_fields = ['username', 'ip_address', 'failure_reason']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # In a real multi-tenant system, we should filter by the user's company
        return super().get_queryset()
