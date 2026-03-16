from django.urls import path
from kernel.system_config.api.views import ConfigAPIView, ModuleSwitchAPIView

app_name = 'system_config'

urlpatterns = [
    path('', ConfigAPIView.as_view(), name='config'),
    path('module-switch/', ModuleSwitchAPIView.as_view(), name='module-switch'),
]
