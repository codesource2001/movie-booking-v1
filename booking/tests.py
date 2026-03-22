from core.tests import BaseTestCase
from show.models import Show
from datetime import timedelta
from django.utils import timezone
from rest_framework import status


class BookingAPITestCase(BaseTestCase):
    
    def test_list_bookings_as_customer(self):
        self.authenticate_as_customer()
        url = '/api/bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_bookings_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_booking_as_customer(self):
        self.authenticate_as_customer()
        
        new_show = Show.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=timezone.now() + timedelta(days=3),
            end_time=timezone.now() + timedelta(days=3, hours=2),
            price=15.00,
            available_seats=100
        )
        
        url = '/api/bookings/'
        data = {
            'show_id': new_show.id,
            'seats': ['B1', 'B2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['seats']), 2)
    
    def test_create_booking_insufficient_seats(self):
        self.authenticate_as_customer()
        
        new_show = Show.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=timezone.now() + timedelta(days=3),
            end_time=timezone.now() + timedelta(days=3, hours=2),
            price=15.00,
            available_seats=1
        )
        
        url = '/api/bookings/'
        data = {
            'show_id': new_show.id,
            'seats': ['B1', 'B2']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_booking_detail(self):
        self.authenticate_as_customer()
        url = f'/api/bookings/{self.booking.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_other_user_booking_denied(self):
        self.authenticate_as(self.theatre_owner)
        url = f'/api/bookings/{self.booking.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_cancel_booking_as_owner(self):
        self.authenticate_as_customer()
        url = f'/api/bookings/{self.booking.id}/cancel/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'cancelled')
    
    def test_cancel_booking_as_admin(self):
        self.authenticate_as_admin()
        url = f'/api/bookings/{self.booking.id}/cancel/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_cancel_other_user_booking_denied(self):
        self.authenticate_as(self.theatre_owner)
        url = f'/api/bookings/{self.booking.id}/cancel/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_my_bookings(self):
        self.authenticate_as_customer()
        url = '/api/bookings/my-bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_booking_history(self):
        self.authenticate_as_customer()
        url = '/api/bookings/history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_booking_history_by_status(self):
        self.authenticate_as_customer()
        url = '/api/bookings/history/?status=pending'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_cannot_list_bookings(self):
        url = '/api/bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
