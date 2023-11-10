import abc
from typing import List

from src.domain.movie_service.models import Movie


class MovieStoragePort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_movie_by_title(self, title: str) -> Movie or None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_movies(
        self, page: int = 1, number_of_records: int = 10
    ) -> List[Movie]:
        raise NotImplementedError

    @abc.abstractmethod
    async def upsert_movies(self, movies: List[Movie]):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_movie(self, imdb_id: str):
        raise NotImplementedError


__all__ = ['MovieStoragePort']
