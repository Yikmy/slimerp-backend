from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/companies/', include('kernel.company.api.urls')),
    path('api/v1/auth/', include('kernel.identity.api.urls')),
    path('api/v1/rbac/', include('kernel.rbac.api.urls')),
    path('api/v1/audit/', include('kernel.audit.api.urls')),
    path('api/v1/config/', include('kernel.system_config.api.urls')),
]
