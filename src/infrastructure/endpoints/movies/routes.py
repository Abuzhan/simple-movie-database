import logging

from sanic import Blueprint, Request

from src.infrastructure.endpoints.decorators import protected
from src.infrastructure.endpoints.movies.utils import convert_movie_to_dict
from src.infrastructure.endpoints.utils import create_response

logger = logging.getLogger(__name__)

MOVIES_ROUTES = Blueprint('movies_api', url_prefix='/v1')


@MOVIES_ROUTES.route('/movies.list', methods=['GET'])
@protected
async def list_all_movies(request: Request):
    logger.info('Listing all movies')
    page = int(request.args.get('page'))
    number_of_records = int(request.args.get('number_of_records'))
    movie_service = request.app.ctx.movie_service
    movies = await movie_service.get_all_movies(page, number_of_records)
    return create_response([convert_movie_to_dict(movie) for movie in movies])


__all__ = ['MOVIES_ROUTES']
