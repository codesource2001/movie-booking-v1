from core.repositories import CrudRepository
from django.db.models import QuerySet
from django.utils import timezone
from show.models import Show
from typing import Optional


class ShowRepository(CrudRepository[Show]):
    def get_scheduled_shows(self) -> QuerySet:
        now = timezone.now()
        return self.filter(start_time__gte=now, status__in=['scheduled', 'running'])

    def get_by_movie(self, movie_id: int) -> QuerySet:
        now = timezone.now()
        return self.filter(movie_id=movie_id, start_time__gte=now, status='scheduled')

    def get_by_screen(self, screen_id: int) -> QuerySet:
        now = timezone.now()
        return self.filter(screen_id=screen_id, start_time__gte=now, status='scheduled')

    def get_by_theatre(self, theatre_id: int) -> QuerySet:
        now = timezone.now()
        return self.filter(
            screen__theatre_id=theatre_id, 
            start_time__gte=now, 
            status='scheduled'
        )

    def get_by_id(self, show_id: int) -> Optional[Show]:
        return self.get_or_none(id=show_id)

    def update_available_seats(self, show: Show, seats_count: int) -> Show:
        show.available_seats -= seats_count
        show.save()
        return show

    def restore_available_seats(self, show: Show, seats_count: int) -> Show:
        show.available_seats += seats_count
        show.save()
        return show

    def with_relations(self) -> QuerySet:
        return self.select_related('movie', 'screen', 'screen__theatre')
