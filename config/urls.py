from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/companies/', include('kernel.company.api.urls')),
    path('api/v1/auth/', include('kernel.identity.api.urls')),
]
