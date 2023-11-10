from sanic import Sanic

from src.domain.movie_service.movie_service import MovieService
from src.infrastructure.adapters import MovieStorageSqlAlchemyAdapter, OMDBHttpAdapter
from src.infrastructure.sql_client import SqlClient


def initialize_movie_service(app: Sanic, sql_client: SqlClient) -> MovieService:
    storage_adapter = MovieStorageSqlAlchemyAdapter(sql_client)
    omdb_adapter = OMDBHttpAdapter(
        base_url=app.config['OMDB_BASE_URL'], api_key=app.config['OMDB_API_KEY']
    )

    app.ctx.movie_service = MovieService(
        movie_storage_port=storage_adapter,
        omdb_port=omdb_adapter,
    )

    @app.listener('after_server_start')
    async def _initialize_data(_app: Sanic, _loop):
        await app.ctx.movie_service.initialize_data()

    return app.ctx.movie_service


__all__ = ["initialize_movie_service"]
