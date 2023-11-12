from typing import List, Dict

from src.domain.movie_service import (
    MovieStoragePort,
    Movie,
)


class MovieStorageMockAdapter(MovieStoragePort):
    def __init__(self, movies: Dict[str, Movie] = None):
        self.movies = movies if movies else {}

    async def get_movie_by_title(self, title: str) -> Movie or None:
        for movie in self.movies.values():
            if movie.title == title:
                return movie
        return None

    async def get_all_movies(
        self, page: int = 1, number_of_records: int = 10
    ) -> List[Movie]:
        if number_of_records >= len(self.movies):
            return list(self.movies.values())
        if page > 1 and number_of_records * page >= len(self.movies):
            return list(self.movies.values())[number_of_records * (page - 1) :]
        return list(
            self.movies.values()[
                number_of_records * (page - 1) : number_of_records * page
            ]
        )

    async def upsert_movies(self, movies: List[Movie]):
        for movie in movies:
            self.movies[movie.imdb_id] = movie

    async def delete_movie(self, imdb_id: str):
        if imdb_id in self.movies:
            del self.movies[imdb_id]


__all__ = ['MovieStorageMockAdapter']
