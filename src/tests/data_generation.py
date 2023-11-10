import random
from datetime import datetime, timezone

from src.domain.movie_service import Movie
from src.utils import generate_random_string


def generate_domain_movie(imdb_id: str = None) -> Movie:
    return Movie(
        imdb_id=imdb_id if imdb_id else generate_random_string(),
        title=generate_random_string(),
        year=random.randint(1900, 2023),
        genre=generate_random_string(),
        director=generate_random_string(),
        country=generate_random_string(),
        imdb_rating=random.uniform(0, 10),
        released_at=datetime.now(tz=timezone.utc),
    )


__all__ = ['generate_domain_movie']
