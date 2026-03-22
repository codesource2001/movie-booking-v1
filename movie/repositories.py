from core.repositories import CrudRepository
from django.db.models import QuerySet
from django.db import models
from movie.models import Movie
from typing import Optional


class MovieRepository(CrudRepository[Movie]):
    def get_active_movies(self) -> QuerySet:
        return self.filter(is_active=True)

    def get_by_genre(self, genre: str) -> QuerySet:
        return self.filter(genre=genre, is_active=True)

    def search_movies(self, query: str) -> QuerySet:
        return self.filter(is_active=True).filter(
            models.Q(title__icontains=query) | 
            models.Q(description__icontains=query)
        )

    def get_upcoming_movies(self) -> QuerySet:
        from django.utils import timezone
        return self.filter(is_active=True, release_date__gte=timezone.now().date())

    def get_now_showing(self) -> QuerySet:
        from django.utils import timezone
        return self.filter(is_active=True, release_date__lte=timezone.now().date())

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return self.get_or_none(id=movie_id, is_active=True)

    def deactivate(self, movie: Movie) -> Movie:
        return self.update(movie, is_active=False)

    def activate(self, movie: Movie) -> Movie:
        return self.update(movie, is_active=True)
