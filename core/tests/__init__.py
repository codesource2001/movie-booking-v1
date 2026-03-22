from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from movie.models import Movie
from theatre.models import Theatre, Screen
from show.models import Show
from booking.models import Booking
from payment.models import Payment
from notification.models import Notification
from datetime import datetime, timedelta
from django.utils import timezone


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='admin'
        )
        
        self.theatre_owner = User.objects.create_user(
            username='theatre_owner',
            email='owner@test.com',
            password='owner123',
            role='theatre_owner'
        )
        
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer123',
            role='customer'
        )
        
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            duration=120,
            release_date='2025-01-01',
            genre='action'
        )
        
        self.theatre = Theatre.objects.create(
            name='Test Theatre',
            location='Test Location',
            address='Test Address',
            total_seats=100,
            owner=self.theatre_owner
        )
        
        self.screen = Screen.objects.create(
            theatre=self.theatre,
            name='Screen 1',
            screen_type='standard',
            total_seats=100
        )
        
        self.show = Show.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            price=10.00,
            available_seats=100
        )
        
        self.booking = Booking.objects.create(
            user=self.customer,
            show=self.show,
            seats=['A1', 'A2'],
            total_price=20.00,
            status='pending'
        )
        
        self.payment = Payment.objects.create(
            booking=self.booking,
            amount=20.00,
            method='credit_card',
            status='completed',
            transaction_id='TXN-TEST123'
        )
        
        self.notification = Notification.objects.create(
            user=self.customer,
            title='Test Notification',
            message='Test Message',
            notification_type='system'
        )
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def authenticate_as_admin(self):
        token = self.get_tokens_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def authenticate_as_theatre_owner(self):
        token = self.get_tokens_for_user(self.theatre_owner)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def authenticate_as_customer(self):
        token = self.get_tokens_for_user(self.customer)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    def authenticate_as(self, user):
        token = self.get_tokens_for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
