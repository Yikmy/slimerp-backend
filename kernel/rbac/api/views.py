from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from kernel.company.models import Company
from kernel.core.api.responses import error_response, success_response
from kernel.rbac.api.serializers import (
    AssignRoleSerializer,
    GrantPermissionSerializer,
    PermissionSerializer,
    RoleSerializer,
)
from kernel.rbac.exceptions import PermissionDenied
from kernel.rbac.models import Permission, Role
from kernel.rbac.services import GrantService, PermissionService, RoleService

User = get_user_model()


class RbacAdminRequiredMixin:
    admin_permission_code = 'rbac.role.manage'

    def _assert_admin(self, request):
        company_id = request.data.get('company_id') or request.query_params.get('company_id')
        if not company_id:
            raise PermissionDenied('company_id is required for RBAC admin operations')

        company = Company.objects.filter(id=company_id).first()
        if company is None:
            raise PermissionDenied('invalid company scope')

        check = PermissionService.has_perm(
            user=request.user,
            company=company,
            code=self.admin_permission_code,
        )
        if not check.allowed:
            raise PermissionDenied(f'RBAC admin permission required: {check.reason}')


class RoleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return success_response(data=serializer.data)


class AssignRoleView(RbacAdminRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AssignRoleSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message='Invalid data', data=serializer.errors)

        self._assert_admin(request)
        target_user = User.objects.filter(id=serializer.validated_data['user_id']).first()
        if target_user is None:
            return error_response(message='User not found', code='USER_NOT_FOUND', status=404)

        user_role = RoleService.assign_role(
            user=target_user,
            company_id=str(serializer.validated_data['company_id']),
            role_name=serializer.validated_data['role_name'],
            actor=request.user,
        )
        return success_response(
            data={
                'user_id': str(user_role.user_id),
                'company_id': str(user_role.company_id),
                'role_id': str(user_role.role_id),
            }
        )


class GrantPermissionView(RbacAdminRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GrantPermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(message='Invalid data', data=serializer.errors)

        self._assert_admin(request)
        role_permission = GrantService.grant(
            role_name=serializer.validated_data['role_name'],
            permission_code=serializer.validated_data['permission_code'],
            actor=request.user,
        )
        return success_response(
            data={
                'role_id': str(role_permission.role_id),
                'permission_id': str(role_permission.permission_id),
            }
        )


class MePermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company_id = request.query_params.get('company_id')
        if not company_id:
            return error_response(message='company_id is required')

        permission_qs = Permission.objects.filter(
            role_permissions__role__user_roles__user=request.user,
            role_permissions__role__user_roles__company_id=company_id,
        ).distinct()
        serializer = PermissionSerializer(permission_qs, many=True)
        return success_response(data=serializer.data)
