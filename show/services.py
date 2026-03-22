from show.repositories import ShowRepository
from show.models import Show
from django.db.models import QuerySet
from django.utils import timezone
from typing import Optional


class ShowService:
    def __init__(self):
        self.repository = ShowRepository(Show)

    def get_all_shows(self, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.repository.all()
        return self.repository.get_scheduled_shows()

    def get_show_by_id(self, show_id: int) -> Optional[Show]:
        return self.repository.get_by_id(show_id)

    def get_shows_by_movie(self, movie_id: int) -> QuerySet:
        return self.repository.get_by_movie(movie_id)

    def get_shows_by_screen(self, screen_id: int) -> QuerySet:
        return self.repository.get_by_screen(screen_id)

    def get_shows_by_theatre(self, theatre_id: int) -> QuerySet:
        return self.repository.get_by_theatre(theatre_id)

    def get_shows_by_date(self, date_str: str) -> QuerySet:
        from django.utils.dateparse import parse_date
        parsed_date = parse_date(date_str)
        if parsed_date:
            from django.db.models import Q
            return self.repository.filter(
                Q(start_time__date=parsed_date) | 
                Q(start_time__date__gte=parsed_date)
            )
        return self.repository.none()

    def create_show(self, data: dict) -> Show:
        return self.repository.create(**data)

    def update_show(self, show: Show, data: dict) -> Show:
        return self.repository.update(show, **data)

    def delete_show(self, show: Show) -> None:
        self.repository.update(show, status='cancelled')

    def get_available_seats(self, show: Show) -> dict:
        return {
            'show_id': show.id,
            'available_seats': show.available_seats,
            'total_seats': show.screen.total_seats
        }

    def get_shows_with_relations(self) -> QuerySet:
        return self.repository.with_relations()
