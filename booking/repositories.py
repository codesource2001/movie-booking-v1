from core.repositories import CrudRepository
from django.db.models import QuerySet
from booking.models import Booking
from user.models import User
from typing import Optional


class BookingRepository(CrudRepository[Booking]):
    def get_by_user(self, user: User) -> QuerySet:
        return self.filter(user=user).order_by('-booking_date')

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        return self.get_or_none(id=booking_id)

    def get_pending_bookings(self, user: User) -> QuerySet:
        return self.filter(user=user, status='pending')

    def get_confirmed_bookings(self, user: User) -> QuerySet:
        return self.filter(user=user, status='confirmed')

    def get_cancelled_bookings(self, user: User) -> QuerySet:
        return self.filter(user=user, status='cancelled')

    def get_by_status(self, user: User, status: str) -> QuerySet:
        return self.filter(user=user, status=status)

    def get_all_for_admin(self) -> QuerySet:
        return self.order_by('-booking_date')

    def with_relations(self) -> QuerySet:
        return self.select_related('user', 'show', 'show__movie', 'show__screen', 'show__screen__theatre')

    def cancel_booking(self, booking: Booking) -> Booking:
        return self.update(booking, status='cancelled')

    def confirm_booking(self, booking: Booking) -> Booking:
        return self.update(booking, status='confirmed')
