from core.tests import BaseTestCase
from theatre.models import Theatre
from rest_framework import status


class TheatreAPITestCase(BaseTestCase):
    
    def test_list_theatres_unauthenticated(self):
        url = '/api/theatres/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_theatre_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = '/api/theatres/'
        data = {
            'name': 'New Theatre',
            'location': 'New Location',
            'address': 'New Address',
            'total_seats': 150
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Theatre')
    
    def test_create_theatre_as_customer_denied(self):
        self.authenticate_as_customer()
        url = '/api/theatres/'
        data = {
            'name': 'New Theatre',
            'location': 'New Location',
            'address': 'New Address',
            'total_seats': 150
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_theatre_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/theatres/'
        data = {
            'name': 'Admin Theatre',
            'location': 'Admin Location',
            'address': 'Admin Address',
            'total_seats': 200
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_theatre_detail(self):
        url = f'/api/theatres/{self.theatre.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Theatre')
    
    def test_update_theatre_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = f'/api/theatres/{self.theatre.id}/'
        data = {'name': 'Updated Theatre'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_theatre_as_other_denied(self):
        self.authenticate_as_customer()
        url = f'/api/theatres/{self.theatre.id}/'
        data = {'name': 'Updated Theatre'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_theatre_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = f'/api/theatres/{self.theatre.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_get_screens_for_theatre(self):
        url = f'/api/theatres/{self.theatre.id}/screens/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_screen_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = f'/api/theatres/{self.theatre.id}/add_screen/'
        data = {
            'name': 'Screen 2',
            'screen_type': '3d',
            'total_seats': 50
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_filter_theatres_by_location(self):
        url = '/api/theatres/?location=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
