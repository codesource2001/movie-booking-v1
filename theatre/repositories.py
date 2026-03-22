from core.repositories import CrudRepository
from django.db.models import QuerySet
from theatre.models import Theatre, Screen
from user.models import User
from typing import Optional


class TheatreRepository(CrudRepository[Theatre]):
    def get_active_theatres(self) -> QuerySet:
        return self.filter(is_active=True)

    def get_by_location(self, location: str) -> QuerySet:
        return self.filter(is_active=True, location__icontains=location)

    def get_by_owner(self, owner: User) -> QuerySet:
        return self.filter(owner=owner)

    def get_by_id(self, theatre_id: int) -> Optional[Theatre]:
        return self.get_or_none(id=theatre_id, is_active=True)

    def deactivate(self, theatre: Theatre) -> Theatre:
        return self.update(theatre, is_active=False)

    def activate(self, theatre: Theatre) -> Theatre:
        return self.update(theatre, is_active=True)

    def with_screens(self) -> QuerySet:
        return self.select_related('owner').prefetch_related('screens')


class ScreenRepository(CrudRepository[Screen]):
    def get_by_theatre(self, theatre: Theatre) -> QuerySet:
        return self.filter(theatre=theatre)

    def get_by_id(self, screen_id: int) -> Optional[Screen]:
        return self.get_or_none(id=screen_id)

    def get_available_screens(self, theatre_id: int) -> QuerySet:
        return self.filter(theatre_id=theatre_id)
