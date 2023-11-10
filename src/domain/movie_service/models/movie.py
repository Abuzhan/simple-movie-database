from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Movie:
    imdb_id: str
    title: str
    year: int
    genre: str
    director: str
    country: str
    imdb_rating: float
    released_at: datetime


__all__ = ["Movie"]
