import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from kernel.identity.services.login_service import LoginService
from kernel.identity.services.password_service import PasswordService
from kernel.identity.exceptions import InvalidCredentials, PasswordMismatch
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

User = get_user_model()

@pytest.mark.django_db
class TestIdentityService:
    def test_login_success(self):
        user = User.objects.create_user(username='testlogin', password='password')
        factory = RequestFactory()
        request = factory.post('/api/v1/auth/login/')
        middleware = SessionMiddleware(lambda r: None)
        middleware.process_request(request)
        request.session.save()
        
        logged_in_user = LoginService.login(request, 'testlogin', 'password')
        assert logged_in_user == user
        assert '_auth_user_id' in request.session

    def test_login_failure(self):
        factory = RequestFactory()
        request = factory.post('/api/v1/auth/login/')
        # Session needed for login failure too if it tries to access session?
        # authenticate() doesn't need session, but login() does.
        # InvalidCredentials raised before login(), so maybe fine.
        
        with pytest.raises(InvalidCredentials):
            LoginService.login(request, 'wrong', 'creds')

    def test_change_password(self):
        user = User.objects.create_user(username='changepw', password='oldpassword')
        PasswordService.change_password(user, 'oldpassword', 'newpassword')
        
        assert user.check_password('newpassword')
        
        with pytest.raises(PasswordMismatch):
            PasswordService.change_password(user, 'wrongold', 'newerpassword')

@pytest.mark.django_db
class TestIdentityAPI:
    def test_login_api(self, client):
        user = User.objects.create_user(username='api_user', password='password')
        resp = client.post('/api/v1/auth/login/', {'username': 'api_user', 'password': 'password'})
        assert resp.status_code == 200
        assert resp.data['success'] is True
        
    def test_me_api(self, client):
        user = User.objects.create_user(username='me_user', password='password')
        client.force_login(user)
        
        resp = client.get('/api/v1/auth/me/')
        assert resp.status_code == 200
        assert resp.data['data']['user']['username'] == 'me_user'
        # Current company might be null if not set
        assert 'current_company' in resp.data['data']
