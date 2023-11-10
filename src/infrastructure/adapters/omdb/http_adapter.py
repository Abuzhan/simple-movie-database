import logging
from datetime import datetime

import aiohttp

from src.domain.movie_service import (
    OMDBPort,
    Movie,
    FailedToFetchOMDBMovie,
    OMDBMovieNotFound,
)

logger = logging.getLogger(__name__)


class OMDBHttpAdapter(OMDBPort):
    def __init__(self, api_key: str, base_url: str):
        self.base_url = base_url
        self.api_key = api_key

    async def fetch_movie_by_title(self, title: str) -> Movie:
        params = {'s': title, 'type': 'movie', 'apikey': self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
                if response.status != 200:
                    raise FailedToFetchOMDBMovie('Error fetching movie')
                if (
                    data.get('Response') == 'False'
                    and data.get('Error') == 'Movie not found!'
                ):
                    raise OMDBMovieNotFound('Requested movie not found')
                if data.get('Response') == 'False':
                    raise FailedToFetchOMDBMovie('Error fetching movie')

                fetched_movies = data.get('Search')
                # picking first in the list, assuming it's the most relevant
                target_movie = fetched_movies[0]
                return self._convert_omdb_movie_to_domain_movie(target_movie)

    async def fetch_movie_by_imdb_id(self, imdb_id: str) -> [Movie]:
        params = {'i': imdb_id, 'type': 'movie', 'apikey': self.api_key}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
                if response.status != 200:
                    raise FailedToFetchOMDBMovie('Error fetching movie')
                if (
                    data.get('Response') == 'False'
                    and data.get('Error') == 'Incorrect IMDb ID.'
                ):
                    raise OMDBMovieNotFound('Requested movie not found')
                if data.get('Response') == 'False':
                    raise FailedToFetchOMDBMovie('Error fetching movie')

                return self._convert_omdb_movie_to_domain_movie(data)

    @staticmethod
    def _convert_omdb_movie_to_domain_movie(omdb_movie: dict) -> Movie:
        return Movie(
            imdb_id=omdb_movie.get('imdbID'),
            title=omdb_movie.get('Title'),
            year=int(omdb_movie.get('Year')),
            genre=omdb_movie.get('Genre'),
            director=omdb_movie.get('Director'),
            country=omdb_movie.get('Country'),
            imdb_rating=float(omdb_movie.get('imdbRating')),
            released_at=datetime.strptime(omdb_movie.get('Released'), '%d %b %Y'),
        )


__all__ = ['OMDBHttpAdapter']
