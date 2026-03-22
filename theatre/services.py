from theatre.repositories import TheatreRepository, ScreenRepository
from theatre.models import Theatre, Screen
from user.models import User
from django.db.models import QuerySet
from typing import Optional


class TheatreService:
    def __init__(self):
        self.theatre_repo = TheatreRepository(Theatre)
        self.screen_repo = ScreenRepository(Screen)

    def get_all_theatres(self, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.theatre_repo.all()
        return self.theatre_repo.get_active_theatres()

    def get_theatre_by_id(self, theatre_id: int, is_admin: bool = False) -> Optional[Theatre]:
        if is_admin:
            return self.theatre_repo.get_or_none(id=theatre_id)
        return self.theatre_repo.get_by_id(theatre_id)

    def get_theatres_by_location(self, location: str) -> QuerySet:
        return self.theatre_repo.get_by_location(location)

    def get_theatres_by_owner(self, owner: User) -> QuerySet:
        return self.theatre_repo.get_by_owner(owner)

    def create_theatre(self, data: dict, owner: User = None) -> Theatre:
        if owner:
            data['owner'] = owner
        return self.theatre_repo.create(**data)

    def update_theatre(self, theatre: Theatre, data: dict) -> Theatre:
        return self.theatre_repo.update(theatre, **data)

    def delete_theatre(self, theatre: Theatre) -> None:
        self.theatre_repo.deactivate(theatre)

    def get_screens_for_theatre(self, theatre: Theatre) -> QuerySet:
        return self.screen_repo.get_by_theatre(theatre)

    def create_screen(self, theatre: Theatre, data: dict) -> Screen:
        data['theatre'] = theatre
        return self.screen_repo.create(**data)

    def update_screen(self, screen: Screen, data: dict) -> Screen:
        return self.screen_repo.update(screen, **data)

    def delete_screen(self, screen: Screen) -> None:
        self.screen_repo.delete(screen)

    def get_theatre_with_screens(self, theatre_id: int) -> Optional[Theatre]:
        return self.theatre_repo.filter(id=theatre_id).prefetch_related('screens').first()
