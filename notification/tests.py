from core.tests import BaseTestCase
from notification.models import Notification
from rest_framework import status


class NotificationAPITestCase(BaseTestCase):
    
    def test_list_notifications_as_customer(self):
        self.authenticate_as_customer()
        url = '/api/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_notifications_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_notification_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/notifications/'
        data = {
            'user': self.customer.id,
            'title': 'New Notification',
            'message': 'New Message',
            'notification_type': 'system'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_notification_as_customer_denied(self):
        self.authenticate_as_customer()
        url = '/api/notifications/'
        data = {
            'user': self.customer.id,
            'title': 'New Notification',
            'message': 'New Message',
            'notification_type': 'system'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_notification_detail(self):
        self.authenticate_as_customer()
        url = f'/api/notifications/{self.notification.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_other_user_notification_denied(self):
        self.authenticate_as(self.theatre_owner)
        url = f'/api/notifications/{self.notification.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_mark_notification_as_read(self):
        self.authenticate_as_customer()
        url = f'/api/notifications/{self.notification.id}/mark-read/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])
    
    def test_mark_all_notifications_as_read(self):
        self.authenticate_as_customer()
        
        Notification.objects.create(
            user=self.customer,
            title='Unread 1',
            message='Message 1',
            notification_type='system'
        )
        Notification.objects.create(
            user=self.customer,
            title='Unread 2',
            message='Message 2',
            notification_type='system'
        )
        
        url = '/api/notifications/mark-all-read/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_unread_count(self):
        self.authenticate_as_customer()
        url = '/api/notifications/unread-count/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('unread_count', response.data)
    
    def test_get_unread_count_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/notifications/unread-count/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_my_notifications(self):
        self.authenticate_as_customer()
        url = '/api/notifications/my-notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_cannot_list_notifications(self):
        url = '/api/notifications/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
