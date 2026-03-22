from booking.repositories import BookingRepository
from booking.models import Booking
from show.repositories import ShowRepository
from show.models import Show
from user.models import User
from django.db import transaction
from django.db.models import QuerySet
from typing import Optional


class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository(Booking)
        self.show_repo = ShowRepository(Show)

    def get_user_bookings(self, user: User, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.booking_repo.get_all_for_admin()
        return self.booking_repo.get_by_user(user)

    def get_booking_by_id(self, booking_id: int, user: User = None, is_admin: bool = False) -> Optional[Booking]:
        booking = self.booking_repo.get_by_id(booking_id)
        if booking and (is_admin or (user and booking.user == user)):
            return booking
        return None

    def get_bookings_by_status(self, user: User, status: str) -> QuerySet:
        return self.booking_repo.get_by_status(user, status)

    @transaction.atomic
    def create_booking(self, user: User, show_id: int, seats: list) -> tuple[Booking, Optional[str]]:
        show = self.show_repo.get_by_id(show_id)
        
        if not show:
            return None, "Show not found"
        
        if show.status not in ['scheduled', 'running']:
            return None, "Show is not available"
        
        if len(seats) > show.available_seats:
            return None, f"Not enough available seats. Only {show.available_seats} seats available"
        
        total_price = show.price * len(seats)
        
        booking = self.booking_repo.create(
            user=user,
            show=show,
            seats=seats,
            total_price=total_price,
            status='pending'
        )
        
        self.show_repo.update_available_seats(show, len(seats))
        
        return booking, None

    @transaction.atomic
    def cancel_booking(self, booking: Booking, user: User, is_admin: bool = False) -> tuple[Booking, Optional[str]]:
        if not is_admin and booking.user != user:
            return None, "Not authorized to cancel this booking"
        
        if booking.status not in ['pending', 'confirmed']:
            return None, "This booking cannot be cancelled"
        
        show = booking.show
        self.show_repo.restore_available_seats(show, len(booking.seats))
        
        return self.booking_repo.cancel_booking(booking), None

    def confirm_booking(self, booking: Booking) -> Booking:
        return self.booking_repo.confirm_booking(booking)

    def get_booking_history(self, user: User, status: str = None) -> QuerySet:
        if status:
            return self.booking_repo.get_by_status(user, status)
        return self.booking_repo.get_by_user(user)

    def get_bookings_with_relations(self, user: User = None) -> QuerySet:
        queryset = self.booking_repo.with_relations()
        if user:
            queryset = queryset.filter(user=user)
        return queryset
