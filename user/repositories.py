from core.repositories import UserRepository
from user.models import User
from django.db.models import QuerySet


class UserRepository(UserRepository):
    def get_by_username(self, username: str):
        return self.get_or_none(username=username)

    def get_by_email(self, email: str):
        return self.get_or_none(email=email)

    def filter_by_role(self, role: str) -> QuerySet:
        return self.filter(role=role)

    def get_active_users(self) -> QuerySet:
        return self.filter(is_active=True)

    def get_all(self) -> QuerySet:
        return self.all()

    def create_user(self, **kwargs):
        return self.create(**kwargs)

    def update_user(self, user: User, **kwargs):
        return self.update(user, **kwargs)
