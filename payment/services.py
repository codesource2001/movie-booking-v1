from payment.repositories import PaymentRepository
from payment.models import Payment
from booking.repositories import BookingRepository
from booking.models import Booking
from user.models import User
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional
import uuid


class PaymentService:
    def __init__(self):
        self.payment_repo = PaymentRepository(Payment)
        self.booking_repo = BookingRepository(Booking)

    def get_user_payments(self, user: User, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.payment_repo.all()
        return self.payment_repo.get_by_user(user)

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.payment_repo.get_by_id(payment_id)

    def get_payments_by_booking(self, booking: Booking) -> QuerySet:
        return self.payment_repo.get_by_booking(booking)

    @transaction.atomic
    def process_payment(self, user: User, booking_id: int, method: str, payment_details: dict = None) -> tuple[Payment, Optional[str]]:
        booking = self.booking_repo.get_by_id(booking_id)
        
        if not booking:
            return None, "Booking not found"
        
        if booking.user != user and not user.is_admin:
            return None, "Not authorized to make payment for this booking"
        
        if booking.status != 'pending':
            return None, "This booking cannot be paid"
        
        transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        payment = self.payment_repo.create(
            booking=booking,
            amount=booking.total_price,
            method=method,
            payment_details=payment_details or {},
            transaction_id=transaction_id,
            status='completed'
        )
        
        self.booking_repo.confirm_booking(booking)
        
        return payment, None

    @transaction.atomic
    def process_refund(self, payment_id: int, is_admin: bool = False) -> tuple[Payment, Optional[str]]:
        if not is_admin:
            return None, "Only admins can process refunds"
        
        payment = self.payment_repo.get_by_id(payment_id)
        
        if not payment:
            return None, "Payment not found"
        
        if payment.status != 'completed':
            return None, "Only completed payments can be refunded"
        
        payment = self.payment_repo.process_refund(payment)
        self.booking_repo.cancel_booking(payment.booking)
        
        return payment, None

    def get_payment_history(self, user: User) -> QuerySet:
        return self.payment_repo.get_by_user(user)

    def get_payments_with_relations(self) -> QuerySet:
        return self.payment_repo.with_relations()
