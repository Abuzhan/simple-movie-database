from src.domain.movie_service.movie_service import MovieService
from src.infrastructure.adapters.movie_storage import MovieStorageMockAdapter
from src.infrastructure.adapters.omdb.mock_adapter import OMDBMockAdapter


def initialize_movie_service_for_test() -> MovieService:
    return MovieService(
        movie_storage_port=MovieStorageMockAdapter(),
        omdb_port=OMDBMockAdapter(),
    )


__all__ = ['initialize_movie_service_for_test']
