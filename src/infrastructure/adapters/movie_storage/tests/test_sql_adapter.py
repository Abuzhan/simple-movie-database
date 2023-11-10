import pytest

from src.infrastructure.adapters.movie_storage.sql_adapter import (
    MovieStorageSqlAlchemyAdapter,
)
from src.tests.data_generation import generate_domain_movie
from src.utils import generate_random_string


@pytest.mark.asyncio
async def test_upsert_movies_succeeds_at_storing_new_records(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movies = [generate_domain_movie() for _ in range(10)]

    # when
    await adapter.upsert_movies(movies)

    # then
    for movie in movies:
        assert await adapter.get_movie_by_title(movie.title) == movie


@pytest.mark.asyncio
async def test_upsert_movies_succeeds_at_updating_existing_records(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movies = [generate_domain_movie() for _ in range(10)]
    await adapter.upsert_movies(movies)
    updated_movies = [generate_domain_movie(imdb_id=movie.imdb_id) for movie in movies]

    # when
    await adapter.upsert_movies(updated_movies)

    # then
    for movie in updated_movies:
        assert await adapter.get_movie_by_title(movie.title) == movie


@pytest.mark.asyncio
async def test_get_movie_by_title_returns_none_when_movie_does_not_exist(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    title = generate_random_string()

    # when
    movie = await adapter.get_movie_by_title(title)

    # then
    assert movie is None


@pytest.mark.asyncio
async def test_get_all_movies_returns_empty_list_when_no_movies_exist(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    page = 1
    number_of_records = 10

    # when
    movies = await adapter.get_all_movies(page, number_of_records)

    # then
    assert movies == []


@pytest.mark.asyncio
async def test_delete_movie_succeeds_at_deleting_existing_movie(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movie = generate_domain_movie()
    await adapter.upsert_movies([movie])

    # when
    await adapter.delete_movie(movie.imdb_id)

    # then
    assert await adapter.get_movie_by_title(movie.title) is None


@pytest.mark.asyncio
async def test_get_all_movies_returns_movies_in_correct_order(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movies = [generate_domain_movie() for _ in range(10)]
    await adapter.upsert_movies(movies)
    movies.sort(key=lambda movie: movie.title)

    # when
    retrieved_movies = await adapter.get_all_movies(1, 10)

    # then
    assert retrieved_movies == movies


@pytest.mark.asyncio
async def test_get_movie_by_title_returns_movie_when_movie_exists(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movie = generate_domain_movie()
    await adapter.upsert_movies([movie])

    # when
    retrieved_movie = await adapter.get_movie_by_title(movie.title)

    # then
    assert retrieved_movie == movie


@pytest.mark.asyncio
async def test_get_all_movies_returns_movies_with_pagination(
    sql_client,
):
    # given
    adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    movies = [generate_domain_movie() for _ in range(10)]
    await adapter.upsert_movies(movies)
    movies.sort(key=lambda movie: movie.title)

    # when
    retrieved_movies = await adapter.get_all_movies(1, 5)

    # then
    assert retrieved_movies == movies[:5]

    # when
    retrieved_movies = await adapter.get_all_movies(2, 5)

    # then
    assert retrieved_movies == movies[5:10]

    # when
    retrieved_movies = await adapter.get_all_movies(3, 5)

    # then
    assert retrieved_movies == []
