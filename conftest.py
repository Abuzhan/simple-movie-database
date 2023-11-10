import asyncio
import os
import socket
from contextlib import closing

import pytest
import pytest_asyncio
from sanic_testing.reusable import ReusableClient
from aioresponses import aioresponses

from config import TestConfig
from src.infrastructure.sql_alchemy_tables import declarative_base
from src.infrastructure.sql_client import SqlClient


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def port():
    # pylint: disable=no-member
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as stream:
        stream.bind(('', 0))
        return stream.getsockname()[1]


@pytest.fixture(scope='session', autouse=True)
def logging():
    from src.logging import initialize_logging

    initialize_logging()


@pytest.fixture(scope='session')
def app(port, db_tables):
    os.environ['PORT'] = str(port)
    from src.bootstrap import create_app

    os.environ['ENVIRONMENT'] = 'test'
    app = create_app()
    return app


@pytest.fixture(scope='session')
def client(app, port, event_loop):
    client = ReusableClient(app, port=port, loop=event_loop)
    with client:
        yield client


@pytest.fixture(scope='function')
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture(scope='session')
def db_tables():
    from sqlalchemy import create_engine as sync_create_engine

    engine = sync_create_engine(_get_connection_string())
    declarative_base.drop_all(engine)
    declarative_base.create_all(engine)
    yield declarative_base
    declarative_base.drop_all(engine)


def _get_connection_string() -> str:
    connection_string = (
        'postgresql+psycopg2://{user}:{password}@localhost:{port}/{dbname}'
    )
    db_parameters = TestConfig().DB_CONNECTION_PARAMETERS
    return connection_string.format(**db_parameters)


@pytest_asyncio.fixture(scope='function')
async def sql_client(db_tables):
    config = TestConfig()
    _sql_client = SqlClient(config.DB_CONNECTION_PARAMETERS)
    await _sql_client.start()
    yield _sql_client

    # clear tables
    async with _sql_client.db_engine.acquire() as connection:
        transaction = await connection.begin()
        for table in reversed(db_tables.sorted_tables):
            await connection.execute(table.delete())
        await transaction.commit()
    await _sql_client.stop()
