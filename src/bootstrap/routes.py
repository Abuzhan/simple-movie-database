from sanic import Sanic

from src.infrastructure.endpoints import (
    HEALTH_CHECK_ROUTES,
    MOVIES_ROUTES,
    LOGIN_ROUTES,
)


def register_routes(app: Sanic):
    app.blueprint(HEALTH_CHECK_ROUTES)
    app.blueprint(LOGIN_ROUTES)
    app.blueprint(MOVIES_ROUTES)


__all__ = ['register_routes']
