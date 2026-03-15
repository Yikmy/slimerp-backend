from django.urls import path
from kernel.company.api.views import CompanyListView, VerifyCompanyAccessView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('verify/', VerifyCompanyAccessView.as_view(), name='company-verify'),
]
