from django.urls import path

from kernel.rbac.api.views import AssignRoleView, GrantPermissionView, MePermissionsView, RoleListView

urlpatterns = [
    path('roles/', RoleListView.as_view(), name='rbac-roles'),
    path('assign-role/', AssignRoleView.as_view(), name='rbac-assign-role'),
    path('grant/', GrantPermissionView.as_view(), name='rbac-grant'),
    path('me-permissions/', MePermissionsView.as_view(), name='rbac-me-permissions'),
]
