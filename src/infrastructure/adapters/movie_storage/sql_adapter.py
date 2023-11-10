from typing import List

from sqlalchemy import select
from src.infrastructure.sql_alchemy_tables.movie import (
    MOVIE,
    MOVIE_COLUMNS_TO_UPDATE,
    MOVIE_INDEX_ELEMENTS,
)

from src.domain.movie_service import (
    MovieStoragePort,
    Movie,
)
from src.infrastructure.sql_client import UpsertCommand, SqlClient


class MovieStorageSqlAlchemyAdapter(MovieStoragePort):
    def __init__(self, sql_client: SqlClient):
        self.sql_client = sql_client
        self.table = MOVIE

    async def get_movie_by_title(self, title: str) -> Movie or None:
        query = select(self.table).where(self.table.c.title == title)
        row = await self.sql_client.fetch_one(query=query)
        return self.convert_movie_to_domain(row) if row else None

    async def get_all_movies(
        self, page: int = 1, number_of_records: int = 10
    ) -> List[Movie]:
        offset = (page - 1) * number_of_records
        query = (
            select(self.table)
            .order_by(self.table.c.title)
            .limit(number_of_records)
            .offset(offset)
        )
        rows = await self.sql_client.fetch_all(query=query)
        return [self.convert_movie_to_domain(row) for row in rows]

    async def upsert_movies(self, movies: List[Movie]):
        rows = [
            {
                'imdb_id': movie.imdb_id,
                'title': movie.title,
                'year': movie.year,
                'genre': movie.genre,
                'director': movie.director,
                'country': movie.country,
                'imdb_rating': movie.imdb_rating,
                'released_at': movie.released_at,
            }
            for movie in movies
        ]
        await self.sql_client.upsert(
            UpsertCommand(
                table=self.table,
                rows=rows,
                index_elements=MOVIE_INDEX_ELEMENTS,
                columns_to_update=MOVIE_COLUMNS_TO_UPDATE,
            )
        )

    async def delete_movie(self, imdb_id: str):
        query = self.table.delete().where(self.table.c.imdb_id == imdb_id)
        await self.sql_client.execute_statement(sql_statement=query)

    @staticmethod
    def convert_movie_to_domain(row) -> Movie:
        return Movie(
            imdb_id=row.imdb_id,
            title=row.title,
            year=row.year,
            genre=row.genre,
            director=row.director,
            country=row.country,
            imdb_rating=row.imdb_rating,
            released_at=row.released_at,
        )


__all__ = ['MovieStorageSqlAlchemyAdapter']
