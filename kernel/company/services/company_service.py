from typing import List, Optional, Tuple
from django.db import transaction
from django.contrib.auth import get_user_model
from kernel.company.models import Company, UserCompanyAccess
from kernel.company.exceptions import CompanyNotFound, CompanyAccessDenied

User = get_user_model()

class CompanyService:
    @staticmethod
    def create_company(name: str, code: str, creator_user=None) -> Company:
        """
        Create a new company. If creator_user is provided, grant access automatically.
        """
        with transaction.atomic():
            company = Company.objects.create(name=name, code=code)
            if creator_user:
                UserCompanyAccess.objects.create(user=creator_user, company=company, is_default=True)
        return company

    @staticmethod
    def get_user_companies(user) -> List[Company]:
        """
        Get all companies accessible by the user.
        """
        return list(Company.objects.filter(user_accesses__user=user))

    @staticmethod
    def assert_company_access(user, company_id: str) -> Company:
        """
        Check if user has access to the company. Raises exception if not.
        Returns the company instance.
        """
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise CompanyNotFound(f"Company {company_id} does not exist")

        if not UserCompanyAccess.objects.filter(user=user, company=company).exists():
            raise CompanyAccessDenied(f"User {user} has no access to company {company.name}")
            
        return company

    @staticmethod
    def get_default_company(user) -> Optional[Company]:
        """
        Get user's default company.
        """
        access = UserCompanyAccess.objects.filter(user=user, is_default=True).first()
        if access:
            return access.company
        # If no default set, return the first one
        access = UserCompanyAccess.objects.filter(user=user).first()
        return access.company if access else None
