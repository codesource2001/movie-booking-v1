from core.repositories import CrudRepository
from django.db.models import QuerySet
from notification.models import Notification
from user.models import User
from typing import Optional


class NotificationRepository(CrudRepository[Notification]):
    def get_by_user(self, user: User) -> QuerySet:
        return self.filter(user=user).order_by('-created_at')

    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        return self.get_or_none(id=notification_id)

    def get_unread_notifications(self, user: User) -> QuerySet:
        return self.filter(user=user, is_read=False).order_by('-created_at')

    def get_read_notifications(self, user: User) -> QuerySet:
        return self.filter(user=user, is_read=True).order_by('-created_at')

    def get_unread_count(self, user: User) -> int:
        return self.filter(user=user, is_read=False).count()

    def get_by_type(self, user: User, notification_type: str) -> QuerySet:
        return self.filter(user=user, notification_type=notification_type)

    def mark_as_read(self, notification: Notification) -> Notification:
        return self.update(notification, is_read=True)

    def mark_all_as_read(self, user: User) -> None:
        self.filter(user=user, is_read=False).update(is_read=True)

    def with_user(self) -> QuerySet:
        return self.select_related('user')
