from django.urls import path
from kernel.company.api.views import CompanyListView, CurrentCompanyView, SwitchCompanyView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('current/', CurrentCompanyView.as_view(), name='company-current'),
    path('switch/', SwitchCompanyView.as_view(), name='company-switch'),
]
