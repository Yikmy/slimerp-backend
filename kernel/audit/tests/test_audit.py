from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from kernel.audit.models import AuditLog, LoginLog
from kernel.audit.services import AuditService
from kernel.company.models import Company

User = get_user_model()

class AuditServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.company = Company.objects.create(name='Test Company', code='TEST')

    def test_log_action(self):
        AuditService.log_action(
            actor=self.user,
            action=AuditLog.ACTION_CREATE,
            target_model='User',
            target_object_id=str(self.user.id),
            result=AuditLog.RESULT_SUCCESS,
            details={'foo': 'bar'},
            company=self.company
        )
        self.assertEqual(AuditLog.objects.count(), 1)
        log = AuditLog.objects.first()
        self.assertEqual(log.created_by, self.user)
        self.assertEqual(log.action, AuditLog.ACTION_CREATE)
        self.assertEqual(log.company, self.company)
        self.assertEqual(log.details, {'foo': 'bar'})

    def test_log_login(self):
        AuditService.log_login(
            user=self.user,
            username='testuser',
            status=LoginLog.STATUS_SUCCESS,
            ip_address='127.0.0.1',
            company=self.company
        )
        self.assertEqual(LoginLog.objects.count(), 1)
        log = LoginLog.objects.first()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.username, 'testuser')
        self.assertEqual(log.status, LoginLog.STATUS_SUCCESS)

class AuditAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(name='Test Company', code='TEST')
        
        # Create some logs
        self.log1 = AuditLog.objects.create(
            created_by=self.user,
            action=AuditLog.ACTION_CREATE,
            target_model='User',
            target_object_id='123',
            company=self.company,
            details={'test': 'data'}
        )
        self.log2 = LoginLog.objects.create(
            user=self.user,
            username='testuser',
            status=LoginLog.STATUS_SUCCESS,
            company=self.company,
            ip_address='127.0.0.1'
        )

    def test_list_audit_logs(self):
        url = '/api/v1/audit/logs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if pagination is used
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertTrue(len(data) >= 1)
        # Verify fields
        self.assertEqual(data[0]['action'], self.log1.action)

    def test_list_login_logs(self):
        url = '/api/v1/audit/login-logs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('results', response.data) if isinstance(response.data, dict) else response.data
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]['username'], self.log2.username)
