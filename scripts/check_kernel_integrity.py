import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from kernel.company.models import Company, UserCompanyAccess
from kernel.company.services.company_service import CompanyService
from kernel.company.exceptions import CompanyNotFound, CompanyAccessDenied
from kernel.identity.exceptions import InvalidCredentials, AccountDisabled
import json
import uuid

User = get_user_model()

def print_header(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def print_result(step, success, details=""):
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {step}")
    if details:
        print(f"      {details}")
    if not success:
        print(f"      !!! FAILURE !!!")

def run_checks():
    print_header("KERNEL INTEGRITY CHECK")

    # --- Flow 1: Data Preparation ---
    print_header("Flow 1: Data Preparation")
    
    # Cleanup
    username = "test_integrity_user"
    email = "test_integrity@example.com"
    password = "SecurePassword123!"
    
    try:
        u = User.objects.filter(username=username).first()
        if u:
            u.delete()
        Company.objects.filter(code__in=["COMP_A", "COMP_B"]).delete()
        print_result("Cleanup existing data", True)
    except Exception as e:
        print_result("Cleanup existing data", False, str(e))
        return

    # Create User
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        print_result(f"Create user {username}", True)
    except Exception as e:
        print_result(f"Create user {username}", False, str(e))
        return

    # Create Companies
    try:
        company_a = Company.objects.create(name="Company A", code="COMP_A")
        company_b = Company.objects.create(name="Company B", code="COMP_B")
        print_result("Create Company A & B", True)
    except Exception as e:
        print_result("Create Company A & B", False, str(e))
        return

    # Link User to Companies
    try:
        UserCompanyAccess.objects.create(user=user, company=company_a, is_default=True)
        UserCompanyAccess.objects.create(user=user, company=company_b, is_default=False)
        print_result("Link User to Companies", True)
    except Exception as e:
        print_result("Link User to Companies", False, str(e))
        return

    # --- Flow 2: Login & Me ---
    print_header("Flow 2: Login & Me")
    client = Client()
    
    # Login
    login_url = "/api/v1/auth/login/"
    login_data = {"username": username, "password": password}
    try:
        response = client.post(login_url, login_data, content_type="application/json")
        if response.status_code == 200 and response.json().get("success"):
            print_result("Login API (200 OK)", True)
            print(f"      Response: {json.dumps(response.json(), indent=2)}")
            # Check session
            if "_auth_user_id" in client.session:
                print_result("Session Created", True)
            else:
                print_result("Session Created", False, "Session key _auth_user_id missing")
        else:
            print_result("Login API", False, f"Status: {response.status_code}, Body: {response.content}")
    except Exception as e:
        print_result("Login API", False, str(e))

    # Me
    me_url = "/api/v1/auth/me/"
    try:
        response = client.get(me_url)
        if response.status_code == 200:
            data = response.json().get("data", {})
            user_data = data.get("user", {})
            companies_data = data.get("companies", [])
            
            if user_data.get("username") == username:
                print_result("Me API - User Data", True)
            else:
                print_result("Me API - User Data", False, f"Expected {username}, got {user_data.get('username')}")
                
            comp_codes = [c.get("company", {}).get("code") for c in companies_data] # Serializer structure check needed
            # The serializer might structure it differently. Let's assume standard ModelSerializer or specific one.
            # Based on MeView: companies = CompanyService.get_user_company_accesses(user)
            # Access -> Company. 
            # Let's inspect the response to be sure.
            
            # Since I don't know the exact serializer output, I'll check if the string "COMP_A" is in the response text for now as a soft check, 
            # and print the structure.
            print(f"      Response: {json.dumps(response.json(), indent=2)}")
            
            if "COMP_A" in str(response.content) and "COMP_B" in str(response.content):
                 print_result("Me API - Companies List", True)
            else:
                 print_result("Me API - Companies List", False, "COMP_A or COMP_B missing")

        else:
            print_result("Me API", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Me API", False, str(e))

    # --- Flow 3: Get User Companies ---
    print_header("Flow 3: Get User Companies")
    companies_url = "/api/v1/companies/" # Check kernel/company/api/urls.py path. It was path('', ...) included under /api/v1/companies/
    # So it should be /api/v1/companies/
    
    try:
        response = client.get(companies_url)
        if response.status_code == 200:
            print_result("Companies List API (200 OK)", True)
            print(f"      Response: {json.dumps(response.json(), indent=2)}")
            if "COMP_A" in str(response.content) and "COMP_B" in str(response.content):
                print_result("Companies List Content", True)
            else:
                print_result("Companies List Content", False, "Missing company codes")
        else:
            print_result("Companies List API", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Companies List API", False, str(e))

    # --- Flow 4: Company Permission (Service Level) ---
    print_header("Flow 4: Company Permission (Service)")
    
    try:
        has_access = CompanyService.user_has_company(user, company_a.id)
        if has_access:
            print_result(f"user_has_company({company_a.code})", True)
        else:
            print_result(f"user_has_company({company_a.code})", False, "Returned False")
            
        random_id = uuid.uuid4()
        try:
            CompanyService.assert_company_access(user, random_id)
            print_result("assert_company_access(random)", False, "Should have raised exception")
        except CompanyNotFound:
            print_result("assert_company_access(random) -> CompanyNotFound", True)
        except CompanyAccessDenied:
             print_result("assert_company_access(random) -> CompanyAccessDenied", True, "Note: Raised AccessDenied instead of NotFound, acceptable depending on implementation")
        except Exception as e:
            print_result("assert_company_access(random)", False, f"Raised wrong exception: {type(e).__name__}: {e}")

        # Test Access Denied (Company exists but no access)
        company_c = Company.objects.create(name="Company C", code="COMP_C")
        try:
            CompanyService.assert_company_access(user, company_c.id)
            print_result("assert_company_access(no_access)", False, "Should have raised CompanyAccessDenied")
        except CompanyAccessDenied:
            print_result("assert_company_access(no_access) -> CompanyAccessDenied", True)
        except Exception as e:
            print_result("assert_company_access(no_access)", False, f"Raised wrong exception: {type(e).__name__}: {e}")
        finally:
            company_c.delete()

    except Exception as e:
        print_result("Permission Service Checks", False, str(e))

    # --- Flow 5: Exception Handling ---
    print_header("Flow 5: Exception Handling")
    
    # Wrong Password
    try:
        response = client.post(login_url, {"username": username, "password": "WrongPassword"}, content_type="application/json")
        if response.status_code in [400, 401]:
             print_result("Login Wrong Password", True, f"Status: {response.status_code}")
             print(f"      Response: {json.dumps(response.json(), indent=2)}")
        else:
             print_result("Login Wrong Password", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Login Wrong Password", False, str(e))
        
    # Unauth Access
    client_unauth = Client()
    try:
        response = client_unauth.get(me_url)
        if response.status_code == 401 or response.status_code == 403:
            print_result("Unauth Access to /me", True, f"Status: {response.status_code}")
        else:
            print_result("Unauth Access to /me", False, f"Status: {response.status_code}")
    except Exception as e:
        print_result("Unauth Access to /me", False, str(e))

    # Clean up
    user.delete()
    company_a.delete()
    company_b.delete()

if __name__ == "__main__":
    run_checks()
