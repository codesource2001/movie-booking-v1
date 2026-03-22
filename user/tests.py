from core.tests import BaseTestCase
from user.models import User


class UserAuthenticationTestCase(BaseTestCase):
    
    def test_user_registration(self):
        url = '/api/auth/register/'
        data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_registration_password_mismatch(self):
        url = '/api/auth/register/'
        data = {
            'username': 'newuser2',
            'email': 'newuser2@test.com',
            'password': 'newpass123',
            'password_confirm': 'differentpass',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login_success(self):
        url = '/api/auth/login/'
        data = {
            'username': 'customer',
            'password': 'customer123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login_invalid_credentials(self):
        url = '/api/auth/login/'
        data = {
            'username': 'customer',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_profile(self):
        self.authenticate_as_customer()
        url = '/api/auth/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'customer')
    
    def test_update_user_profile(self):
        self.authenticate_as_customer()
        url = '/api/auth/profile/'
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
    
    def test_change_password(self):
        self.authenticate_as_customer()
        url = '/api/auth/change-password/'
        data = {
            'old_password': 'customer123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        user = User.objects.get(username='customer')
        self.assertTrue(user.check_password('newpass123'))
    
    def test_change_password_mismatch(self):
        self.authenticate_as_customer()
        url = '/api/auth/change-password/'
        data = {
            'old_password': 'customer123',
            'new_password': 'newpass123',
            'new_password_confirm': 'differentpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        self.authenticate_as_customer()
        url = '/api/auth/logout/'
        response = self.client.post(url, {'refresh': 'dummy'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_access_denied(self):
        url = '/api/auth/profile/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
