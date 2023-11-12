class FailedToFetchOMDBMovie(Exception):
    error_code = 'FAILED_TO_FETCH_OMDB_MOVIE'


class OMDBMovieNotFound(Exception):
    error_code = 'OMDB_MOVIE_NOT_FOUND'


class MovieNotFound(Exception):
    error_code = 'MOVIE_NOT_FOUND'


__all__ = ['FailedToFetchOMDBMovie', 'OMDBMovieNotFound', 'MovieNotFound']
