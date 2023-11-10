import logging

from sanic import Sanic
from sanic.exceptions import NotFound, MethodNotSupported
from sanic.request import Request

from src.infrastructure.endpoints import error_handlers

logger = logging.getLogger(__name__)


def register_request_handlers(app: Sanic):
    @app.middleware('request')
    async def _abort_if_not_http(request: Request):
        if request.protocol is None:
            logger.warning('Not an HTTP request, aborting')
            return error_handlers.handle_400()

    @app.exception(NotFound)
    async def _error_404(_request, e):
        logger.info(e, exc_info=True)
        return error_handlers.handle_404()

    @app.exception(MethodNotSupported)
    async def _error_405(_request, e):
        logger.info(e, exc_info=True)
        return error_handlers.handle_405()

    @app.exception(Exception)
    async def _error_500(_request, e):
        logger.error(e, exc_info=True)
        return error_handlers.handle_500(e)


__all__ = ['register_request_handlers']
