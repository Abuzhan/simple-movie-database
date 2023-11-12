from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Movie:
    imdb_id: str
    title: str
    year: int
    genre: str or None
    director: str or None
    country: str or None
    imdb_rating: float or None
    released_at: datetime


__all__ = ["Movie"]
