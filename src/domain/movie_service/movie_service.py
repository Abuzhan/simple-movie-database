import logging
from typing import List

from src.domain.movie_service.models import Movie
from src.domain.movie_service.ports import OMDBPort, MovieStoragePort
from src.domain.movie_service.exceptions import OMDBMovieNotFound, MovieNotFound
from src.domain.movie_service.constants import TOP_100_MOVIE_IDS

logger = logging.getLogger(__name__)


class MovieService:
    def __init__(self, omdb_port: OMDBPort, movie_storage_port: MovieStoragePort):
        self.omdb_port = omdb_port
        self.movie_storage_port = movie_storage_port

    async def initialize_data(self):
        if await self._is_storage_empty():
            logger.info('Initializing data for the service')
            movie_ids = TOP_100_MOVIE_IDS
            fetched_movies = []
            for movie_id in movie_ids:
                try:
                    result = await self.omdb_port.fetch_movie_by_imdb_id(movie_id)
                    fetched_movies.append(result)
                except OMDBMovieNotFound as e:
                    logger.error(f'Failed to fetch movie with id {movie_id} due to {e}')
                    continue
            await self.movie_storage_port.upsert_movies(fetched_movies)
            logger.info('Data initialized')

    async def get_all_movies(
        self, page: int or None, number_of_records: int or None
    ) -> List[Movie]:
        page = page or 1
        number_of_records = number_of_records or 10
        return await self.movie_storage_port.get_all_movies(page, number_of_records)

    async def get_movie_by_title(self, title: str) -> Movie or None:
        result = await self.movie_storage_port.get_movie_by_title(title)

        if result is None:
            raise MovieNotFound(f'Movie with title {title} not found')

        return result

    async def create_new_movie(self, title: str):
        movie = await self.omdb_port.fetch_movie_by_title(title)
        await self.movie_storage_port.upsert_movies([movie])
        return movie

    async def delete_movie(self, imdb_id: str):
        return await self.movie_storage_port.delete_movie(imdb_id)

    async def _is_storage_empty(self):
        stored_movies = await self.movie_storage_port.get_all_movies()
        return len(stored_movies) == 0


__all__ = ['MovieService']
