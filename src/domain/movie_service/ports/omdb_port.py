import abc


from src.domain.movie_service.models import Movie


class OMDBPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def fetch_movie_by_title(self, title: str) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_movie_by_imdb_id(self, imdb_id: str) -> [Movie]:
        raise NotImplementedError


__all__ = ['OMDBPort']
