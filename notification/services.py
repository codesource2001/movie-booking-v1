from notification.repositories import NotificationRepository
from notification.models import Notification
from user.models import User
from django.db.models import QuerySet
from typing import Optional, List


class NotificationService:
    def __init__(self):
        self.repository = NotificationRepository(Notification)

    def get_user_notifications(self, user: User, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.repository.all()
        return self.repository.get_by_user(user)

    def get_notification_by_id(self, notification_id: int, user: User = None, is_admin: bool = False) -> Optional[Notification]:
        notification = self.repository.get_by_id(notification_id)
        if notification and (is_admin or (user and notification.user == user)):
            return notification
        return None

    def get_unread_notifications(self, user: User) -> QuerySet:
        return self.repository.get_unread_notifications(user)

    def get_unread_count(self, user: User, is_admin: bool = False) -> int:
        if is_admin:
            return self.repository.filter(is_read=False).count()
        return self.repository.get_unread_count(user)

    def create_notification(self, user: User, title: str, message: str, notification_type: str, related_id: int = None) -> Notification:
        return self.repository.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            related_id=related_id
        )

    def create_bulk_notifications(self, notifications_data: List[dict]) -> List[Notification]:
        notifications = [
            Notification(**data) for data in notifications_data
        ]
        return self.repository.bulk_create(notifications)

    def mark_as_read(self, notification: Notification, user: User, is_admin: bool = False) -> tuple[Notification, Optional[str]]:
        if not is_admin and notification.user != user:
            return None, "Not authorized"
        return self.repository.mark_as_read(notification), None

    def mark_all_as_read(self, user: User) -> None:
        self.repository.mark_all_as_read(user)

    def send_booking_confirmation(self, booking) -> Notification:
        return self.create_notification(
            user=booking.user,
            title="Booking Confirmed",
            message=f"Your booking for {booking.show.movie.title} has been confirmed. Seats: {', '.join(booking.seats)}",
            notification_type='booking',
            related_id=booking.id
        )

    def send_payment_confirmation(self, payment) -> Notification:
        return self.create_notification(
            user=payment.booking.user,
            title="Payment Successful",
            message=f"Payment of ${payment.amount} for {payment.booking.show.movie.title} was successful. Transaction ID: {payment.transaction_id}",
            notification_type='payment',
            related_id=payment.id
        )

    def send_booking_cancelled(self, booking) -> Notification:
        return self.create_notification(
            user=booking.user,
            title="Booking Cancelled",
            message=f"Your booking for {booking.show.movie.title} has been cancelled.",
            notification_type='booking',
            related_id=booking.id
        )
