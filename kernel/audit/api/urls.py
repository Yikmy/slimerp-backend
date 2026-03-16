from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuditLogViewSet, LoginLogViewSet

router = DefaultRouter()
router.register(r'logs', AuditLogViewSet, basename='audit-log')
router.register(r'login-logs', LoginLogViewSet, basename='login-log')

urlpatterns = [
    path('', include(router.urls)),
]
