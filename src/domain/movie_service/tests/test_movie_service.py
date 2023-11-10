import pytest

from src.domain.movie_service.tests.utils import initialize_movie_service_for_test
from src.tests.data_generation import generate_domain_movie


@pytest.mark.asyncio
async def test_initialize_data_fetches_movies_and_stores_them():
    # given
    service = initialize_movie_service_for_test()

    # when
    await service.initialize_data()

    # then
    stored_movies = service.movie_storage_port.movies
    assert len(stored_movies) == 100


@pytest.mark.asyncio
async def test_initialize_data_skips_if_data_exists():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001'
    )

    # when
    await service.initialize_data()

    # then
    stored_movies = service.movie_storage_port.movies
    assert len(stored_movies) == 1


@pytest.mark.asyncio
async def test_initialize_data_ignores_not_found_movies():
    # given
    service = initialize_movie_service_for_test()
    service.omdb_port.throw_not_found_exception = True

    # when
    await service.initialize_data()

    # then
    stored_movies = service.movie_storage_port.movies
    assert len(stored_movies) == 0
