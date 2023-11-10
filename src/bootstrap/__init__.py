import logging
import os

from sanic import Sanic

from config import (
    ProductionConfig,
    DevelopmentConfig,
    Config,
    TestConfig,
)
from src.bootstrap.db import initialize_db
from src.logging import initialize_logging
from src.bootstrap.movie_service import initialize_movie_service
from src.bootstrap.request_handlers import register_request_handlers
from src.bootstrap.routes import register_routes

logger = logging.getLogger(__name__)


def create_app():
    logger.info('Initializing application')
    config = get_config()
    initialize_logging()

    app = Sanic('application')
    app.update_config(config)

    register_request_handlers(app)
    register_routes(app)

    app.register_listener(
        lambda app, loop: logger.info('Starting service'), 'before_server_start'
    )
    app.register_listener(
        lambda app, loop: logger.info('Service started'), 'after_server_start'
    )
    app.register_listener(
        lambda app, loop: logger.info('Stopping service'), 'before_server_stop'
    )
    app.register_listener(
        lambda app, loop: logger.info('Service stopped'), 'after_server_stop'
    )

    sql_client = initialize_db(app)
    initialize_movie_service(app, sql_client)

    logger.info('Application initialized')
    return app


def get_config() -> Config:
    environment = os.getenv('ENVIRONMENT', 'local')
    if environment == 'production':
        return ProductionConfig()
    if environment == 'test':
        return TestConfig()
    return DevelopmentConfig()


__all__ = ['create_app', 'get_config']
