from src.domain.movie_service import Movie


def convert_movie_to_dict(movie: Movie) -> dict:
    return {
        'imdb_id': movie.imdb_id,
        'title': movie.title,
        'year': movie.year,
        'genre': movie.genre,
        'director': movie.director,
        'country': movie.country,
        'imdb_rating': movie.imdb_rating,
        'released_at': movie.released_at.isoformat(),
    }


__all__ = ['convert_movie_to_dict']
