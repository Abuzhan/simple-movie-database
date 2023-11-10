import logging

from sanic import Sanic

from src.infrastructure.sql_client import SqlClient

logger = logging.getLogger(__name__)


def initialize_db(app: Sanic) -> SqlClient:
    sql_client = SqlClient(app.config['DB_CONNECTION_PARAMETERS'])

    @app.listener('before_server_start')
    async def _initialize_engine(_app: Sanic, _loop):
        await sql_client.start()

    @app.listener('after_server_stop')
    async def _close_db_engine(_app: Sanic, _loop):
        await sql_client.stop()

    return sql_client


__all__ = ['initialize_db']
