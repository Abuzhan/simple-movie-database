import logging

from sanic import Blueprint, Request

from src.domain.movie_service import MovieNotFound
from src.infrastructure.endpoints.decorators import protected
from src.infrastructure.endpoints.movies.utils import convert_movie_to_dict
from src.infrastructure.endpoints.utils import create_response

logger = logging.getLogger(__name__)

MOVIES_ROUTES = Blueprint('movies_api', url_prefix='/v1')


@MOVIES_ROUTES.route('/movies.list', methods=['GET'])
async def list_all_movies(request: Request):
    logger.info('Listing all movies')
    page = request.args.get('page', 1)
    number_of_records = request.args.get('number_of_records', 10)
    if not _is_valid_int(page) or not _is_valid_int(number_of_records):
        return create_response(
            error_code='INVALID_REQUEST_BODY',
            message='Invalid request body',
            status_code=400,
        )
    movie_service = request.app.ctx.movie_service
    movies = await movie_service.get_all_movies(page, number_of_records)
    return create_response([convert_movie_to_dict(movie) for movie in movies])


@MOVIES_ROUTES.route('/movies.get/<title:str>', methods=['GET'])
async def get_movie(request: Request, title: str):
    logger.info('Getting movie %s', title)
    movie_service = request.app.ctx.movie_service

    try:
        movie = await movie_service.get_movie_by_title(title)
    except MovieNotFound as e:
        return create_response(
            error_code=e.error_code,
            message=f'Movie {title} not found',
            status_code=404,
        )

    return create_response(convert_movie_to_dict(movie))


@MOVIES_ROUTES.route('/movies.create', methods=['POST'])
async def create_movie(request: Request):
    logger.info('Creating movie')
    movie_service = request.app.ctx.movie_service
    title = request.json.get('title')

    if not title:
        return create_response(
            error_code='INVALID_REQUEST_BODY',
            message='Missing title in request body',
            status_code=400,
        )

    movie = await movie_service.create_new_movie(str(title))
    return create_response(convert_movie_to_dict(movie))


@MOVIES_ROUTES.route('/movies.delete/<imdb_id:str>', methods=['DELETE'])
@protected
async def delete_movie(request: Request, imdb_id: str):
    logger.info('Deleting movie %s', imdb_id)
    movie_service = request.app.ctx.movie_service
    await movie_service.delete_movie(imdb_id)
    return create_response()


def _is_valid_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


__all__ = ['MOVIES_ROUTES']
