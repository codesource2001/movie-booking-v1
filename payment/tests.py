from core.tests import BaseTestCase
from booking.models import Booking
from show.models import Show
from datetime import timedelta
from django.utils import timezone
from rest_framework import status


class PaymentAPITestCase(BaseTestCase):
    
    def test_list_payments_as_customer(self):
        self.authenticate_as_customer()
        url = '/api/payments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_payments_as_admin(self):
        self.authenticate_as_admin()
        url = '/api/payments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_payment_as_customer(self):
        self.authenticate_as_customer()
        
        new_booking = Booking.objects.create(
            user=self.customer,
            show=self.show,
            seats=['C1', 'C2'],
            total_price=30.00,
            status='pending'
        )
        
        url = '/api/payments/'
        data = {
            'booking_id': new_booking.id,
            'method': 'debit_card'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'completed')
    
    def test_create_payment_for_other_booking_denied(self):
        self.authenticate_as_customer()
        
        new_booking = Booking.objects.create(
            user=self.theatre_owner,
            show=self.show,
            seats=['D1'],
            total_price=10.00,
            status='pending'
        )
        
        url = '/api/payments/'
        data = {
            'booking_id': new_booking.id,
            'method': 'credit_card'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_payment_detail(self):
        self.authenticate_as_customer()
        url = f'/api/payments/{self.payment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_payment_for_other_booking_denied(self):
        self.authenticate_as(self.theatre_owner)
        url = f'/api/payments/{self.payment.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_refund_as_admin(self):
        self.authenticate_as_admin()
        
        payment = Payment.objects.create(
            booking=self.booking,
            amount=20.00,
            method='credit_card',
            status='completed',
            transaction_id='TXN-REFUND123'
        )
        
        url = f'/api/payments/{payment.id}/refund/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'refunded')
    
    def test_refund_as_customer_denied(self):
        self.authenticate_as_customer()
        url = f'/api/payments/{self.payment.id}/refund/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_my_payments(self):
        self.authenticate_as_customer()
        url = '/api/payments/my-payments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_payments_by_booking(self):
        self.authenticate_as_customer()
        url = f'/api/payments/booking/{self.booking.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_cannot_list_payments(self):
        url = '/api/payments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
