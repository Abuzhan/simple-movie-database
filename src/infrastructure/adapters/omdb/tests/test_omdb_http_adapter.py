from datetime import datetime

import pytest

from src.domain.movie_service import OMDBMovieNotFound
from src.infrastructure.adapters.omdb.http_adapter import OMDBHttpAdapter


@pytest.mark.asyncio
async def test_fetch_movie_by_imdb_id_returns_correct_data_format_when_succeeds(mock_aioresponse):
    # given
    base_url = 'http://www.test.com'
    api_key = 'random_api_key'
    imdb_id = 'tt3896198'
    response = get_fetch_movie_by_imdb_id_success_response(imdb_id=imdb_id)
    mock_aioresponse.get(
        url=f'{base_url}/?apikey={api_key}&i={imdb_id}&type=movie',
        payload=response,
        status=200
    )
    http_adapter = OMDBHttpAdapter(api_key=api_key, base_url=base_url)

    # when
    result = await http_adapter.fetch_movie_by_imdb_id(imdb_id=imdb_id)

    # then
    assert result.imdb_id == imdb_id
    assert result.title == response['Title']
    assert result.year == int(response['Year'])
    assert result.released_at == datetime.strptime(response['Released'], '%d %b %Y')
    assert result.genre == response['Genre']
    assert result.director == response['Director']
    assert result.country == response['Country']
    assert result.imdb_rating == float(response['imdbRating'])


@pytest.mark.asyncio
async def test_fetch_movie_by_imdb_id_raises_correct_exception_when_movie_not_found(mock_aioresponse):
    # given
    base_url = 'http://www.test.com'
    api_key = 'random_api_key'
    imdb_id = 'tt3896198'
    response = get_fetch_movie_by_imdb_id_not_found_response()
    mock_aioresponse.get(
        url=f'{base_url}/?apikey={api_key}&i={imdb_id}&type=movie',
        payload=response,
        status=200
    )
    http_adapter = OMDBHttpAdapter(api_key=api_key, base_url=base_url)

    # when
    with pytest.raises(OMDBMovieNotFound) as excinfo:
        await http_adapter.fetch_movie_by_imdb_id(imdb_id=imdb_id)

    # then
    assert str(excinfo.value) == 'Requested movie not found'


def get_fetch_movie_by_imdb_id_success_response(imdb_id: str = None, title: str = None) -> dict:
    return {
        "Title": title if title else "The Guardians of the Galaxy",
        "Year": "2017",
        "Released": "05 May 2017",
        "Genre": "Action, Adventure, Comedy",
        "Director": "James Gunn",
        "Country": "United States",
        "imdbRating": "7.6",
        "imdbID": imdb_id if imdb_id else "tt3896198",
        "Type": "movie",
        "Response": "True"
    }


def get_fetch_movie_by_imdb_id_not_found_response() -> dict:
    return {
        "Error": "Incorrect IMDb ID.",
        "Response": "False"
    }
