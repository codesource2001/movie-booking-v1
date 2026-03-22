from core.tests import BaseTestCase
from show.models import Show
from datetime import timedelta
from django.utils import timezone
from rest_framework import status


class ShowAPITestCase(BaseTestCase):
    
    def test_list_shows_unauthenticated(self):
        url = '/api/shows/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_shows_authenticated(self):
        self.authenticate_as_customer()
        url = '/api/shows/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_show_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = '/api/shows/'
        data = {
            'movie': self.movie.id,
            'screen': self.screen.id,
            'start_time': (timezone.now() + timedelta(days=2)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=2, hours=2)).isoformat(),
            'price': '15.00',
            'available_seats': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_show_as_customer_denied(self):
        self.authenticate_as_customer()
        url = '/api/shows/'
        data = {
            'movie': self.movie.id,
            'screen': self.screen.id,
            'start_time': (timezone.now() + timedelta(days=2)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=2, hours=2)).isoformat(),
            'price': '15.00',
            'available_seats': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_show_detail(self):
        url = f'/api/shows/{self.show.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_show_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = f'/api/shows/{self.show.id}/'
        data = {'price': '20.00'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_show_as_owner(self):
        self.authenticate_as_theatre_owner()
        url = f'/api/shows/{self.show.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_get_available_seats(self):
        url = f'/api/shows/{self.show.id}/available_seats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('available_seats', response.data)
    
    def test_filter_shows_by_movie(self):
        url = f'/api/shows/by-movie/{self.movie.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_shows_by_theatre(self):
        url = f'/api/shows/by-theatre/{self.theatre.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_shows_by_screen(self):
        url = f'/api/shows/?screen={self.screen.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
