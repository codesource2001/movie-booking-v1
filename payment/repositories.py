from core.repositories import CrudRepository
from django.db.models import QuerySet
from payment.models import Payment
from booking.models import Booking
from typing import Optional


class PaymentRepository(CrudRepository[Payment]):
    def get_by_booking(self, booking: Booking) -> QuerySet:
        return self.filter(booking=booking)

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.get_or_none(id=payment_id)

    def get_by_user(self, user) -> QuerySet:
        return self.filter(booking__user=user).order_by('-payment_date')

    def get_by_status(self, status: str) -> QuerySet:
        return self.filter(status=status)

    def get_completed_payments(self, user) -> QuerySet:
        return self.filter(booking__user=user, status='completed')

    def with_relations(self) -> QuerySet:
        return self.select_related('booking', 'booking__user', 'booking__show', 'booking__show__movie')

    def process_refund(self, payment: Payment) -> Payment:
        return self.update(payment, status='refunded')
