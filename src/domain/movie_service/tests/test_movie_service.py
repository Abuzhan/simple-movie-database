import pytest

from src.domain.movie_service import MovieNotFound, OMDBMovieNotFound
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


@pytest.mark.asyncio
async def test_get_all_movies_returns_all_movies():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001'
    )
    service.movie_storage_port.movies['tt0000002'] = generate_domain_movie(
        imdb_id='tt0000002'
    )

    # when
    result = await service.get_all_movies(page=1, number_of_records=10)

    # then
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_all_movies_returns_empty_list_if_no_movies():
    # given
    service = initialize_movie_service_for_test()

    # when
    result = await service.get_all_movies(page=1, number_of_records=10)

    # then
    assert len(result) == 0


@pytest.mark.asyncio
async def test_get_movie_by_title_returns_movie():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001', title='Test Movie'
    )

    # when
    result = await service.get_movie_by_title('Test Movie')

    # then
    assert result.imdb_id == 'tt0000001'


@pytest.mark.asyncio
async def test_get_movie_by_title_raises_exception_if_movie_not_found():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001', title='Test Movie'
    )

    # when
    with pytest.raises(MovieNotFound):
        await service.get_movie_by_title('Test Movie 2')


@pytest.mark.asyncio
async def test_create_new_movie_creates_new_movie():
    # given
    service = initialize_movie_service_for_test()

    # when
    await service.create_new_movie(title='Test Movie')

    # then
    assert len(service.movie_storage_port.movies) == 1
    assert list(service.movie_storage_port.movies.values())[0].title == 'Test Movie'


@pytest.mark.asyncio
async def test_create_new_movie_raises_exception_if_movie_not_found_in_omdb():
    # given
    service = initialize_movie_service_for_test()
    service.omdb_port.throw_not_found_exception = True

    # when
    with pytest.raises(OMDBMovieNotFound):
        await service.create_new_movie(title='Test Movie')


@pytest.mark.asyncio
async def test_create_new_movie_succeeds_even_if_movie_already_stored():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001', title='Test Movie'
    )
    service.omdb_port.imdb_id_to_use = 'tt0000001'

    # when
    await service.create_new_movie(title='Test Movie')

    # then
    assert len(service.movie_storage_port.movies) == 1
    assert list(service.movie_storage_port.movies.values())[0].title == 'Test Movie'


@pytest.mark.asyncio
async def test_delete_movie_deletes_movie():
    # given
    service = initialize_movie_service_for_test()
    service.movie_storage_port.movies['tt0000001'] = generate_domain_movie(
        imdb_id='tt0000001', title='Test Movie'
    )

    # when
    await service.delete_movie('tt0000001')

    # then
    assert len(service.movie_storage_port.movies) == 0


@pytest.mark.asyncio
async def test_delete_movie_skips_if_movie_not_found():
    # given
    service = initialize_movie_service_for_test()

    # when
    await service.delete_movie('tt0000001')

    # then
    assert len(service.movie_storage_port.movies) == 0
