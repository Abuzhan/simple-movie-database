import logging
from datetime import datetime


from src.domain.movie_service import OMDBPort, Movie, OMDBMovieNotFound

logger = logging.getLogger(__name__)


class OMDBMockAdapter(OMDBPort):
    def __init__(self, throw_not_found_exception: bool = False):
        self.throw_not_found_exception = throw_not_found_exception

    async def fetch_movie_by_title(self, title: str) -> Movie:
        return Movie(
            imdb_id='tt0111161',
            title=title,
            year=1994,
            genre='Drama',
            director='Frank Darabont',
            country='USA',
            imdb_rating=9.3,
            released_at=datetime.strptime('14 Oct 1994', '%d %b %Y'),
        )

    async def fetch_movie_by_imdb_id(self, imdb_id: str) -> [Movie]:
        if self.throw_not_found_exception:
            raise OMDBMovieNotFound('Requested movie not found')

        return Movie(
            imdb_id=imdb_id,
            title='The Shawshank Redemption',
            year=1994,
            genre='Drama',
            director='Frank Darabont',
            country='USA',
            imdb_rating=9.3,
            released_at=datetime.strptime('14 Oct 1994', '%d %b %Y'),
        )


__all__ = ['OMDBMockAdapter']
