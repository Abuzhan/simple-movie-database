import os

import service_secrets
from src.utils import generate_random_string

LOCAL_PORT = 1399


class Config:
    def __init__(self):
        self.PORT = os.environ.get('PORT', LOCAL_PORT)
        self.DB_CONNECTION_PARAMETERS = None
        self.DB_PORT = os.environ.get('DB_PORT', 5433)
        self.DB_NAME = 'simple_movie_database'
        self.DB_USER = 'postgres'
        self.OMDB_API_KEY = None
        self.OMDB_BASE_URL = 'http://www.omdbapi.com/'
        self.SECRET = generate_random_string()
        self.INITIALIZE_DATA = True


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'development'
        self.DB_PORT = 5432
        self.DB_CONNECTION_PARAMETERS = {
            'host': 'localhost',
            'user': self.DB_USER,
            'password': '',
            'port': self.DB_PORT,
            'dbname': self.DB_NAME,
        }
        self.OMDB_API_KEY = service_secrets.OMDB_API_KEY


class TestConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = True
        self.ENV = 'test'
        self.DB_PORT = 5432
        self.DB_NAME = 'simple_movie_database_test'
        self.DB_CONNECTION_PARAMETERS = {
            'host': 'localhost',
            'user': self.DB_USER,
            'password': '',
            'port': self.DB_PORT,
            'dbname': self.DB_NAME,
        }
        self.OMDB_API_KEY = generate_random_string()
        self.INITIALIZE_DATA = False


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.PORT = os.environ['PORT']
        self.ENV = 'production'
        self.OMDB_API_KEY = service_secrets.OMDB_API_KEY
        self.DB_CONNECTION_PARAMETERS = {
            'user': self.DB_USER,
            'password': service_secrets.DB_PASSWORD,
            'host': f'/cloudsql/vivid-partition-403614:europe-west1:main',
            'dbname': self.DB_NAME,
        }
