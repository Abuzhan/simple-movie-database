import sqlalchemy as sa

from src.infrastructure.sql_alchemy_tables.declarative_base import declarative_base

MOVIE = sa.Table(
    'movie',
    declarative_base,
    sa.Column('imdb_id', sa.TEXT, nullable=False, unique=True),
    sa.Column('title', sa.TEXT, nullable=False),
    sa.Column('year', sa.INTEGER, nullable=False),
    sa.Column('genre', sa.TEXT, nullable=True),
    sa.Column('director', sa.TEXT, nullable=False),
    sa.Column('country', sa.TEXT, nullable=False),
    sa.Column('imdb_rating', sa.FLOAT, nullable=False),
    sa.Column('released_at', sa.DateTime(timezone=True), nullable=False),
)

MOVIE_INDEX_ELEMENTS = ['imdb_id']
MOVIE_COLUMNS_TO_UPDATE = [
    'title',
    'year',
    'genre',
    'director',
    'country',
    'imdb_rating',
    'released_at',
]

__all__ = ['MOVIE', 'MOVIE_INDEX_ELEMENTS', 'MOVIE_COLUMNS_TO_UPDATE']
