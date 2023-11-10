import logging

from sanic import Blueprint

from src.infrastructure.endpoints.utils import create_response

logger = logging.getLogger(__name__)

HEALTH_CHECK_ROUTES = Blueprint('health_check_api', url_prefix='/health-checks')


@HEALTH_CHECK_ROUTES.route('/ready', methods=['GET'])
async def health_check_readiness(_):
    logger.info('Checking for readiness')
    return create_response({'message': 'ready'})


@HEALTH_CHECK_ROUTES.route('/live', methods=['GET'])
async def health_check_liveness(_):
    logger.info('Checking for liveness')
    return create_response({'message': 'live'})


__all__ = ['HEALTH_CHECK_ROUTES']
