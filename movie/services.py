from movie.repositories import MovieRepository
from movie.models import Movie
from django.db.models import QuerySet
from typing import Optional, List


class MovieService:
    def __init__(self):
        self.repository = MovieRepository(Movie)

    def get_all_movies(self, is_admin: bool = False) -> QuerySet:
        if is_admin:
            return self.repository.all()
        return self.repository.get_active_movies()

    def get_movie_by_id(self, movie_id: int, is_admin: bool = False) -> Optional[Movie]:
        if is_admin:
            return self.repository.get_or_none(id=movie_id)
        return self.repository.get_by_id(movie_id)

    def get_movies_by_genre(self, genre: str) -> QuerySet:
        return self.repository.get_by_genre(genre)

    def search_movies(self, query: str) -> QuerySet:
        return self.repository.search_movies(query)

    def get_upcoming_movies(self) -> QuerySet:
        return self.repository.get_upcoming_movies()

    def get_now_showing(self) -> QuerySet:
        return self.repository.get_now_showing()

    def create_movie(self, data: dict) -> Movie:
        return self.repository.create(**data)

    def update_movie(self, movie: Movie, data: dict) -> Movie:
        return self.repository.update(movie, **data)

    def delete_movie(self, movie: Movie) -> None:
        self.repository.deactivate(movie)

    def activate_movie(self, movie: Movie) -> Movie:
        return self.repository.activate(movie)
