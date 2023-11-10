import os

LOCAL_PORT = 1399


class Config:
    def __init__(self):
        self.PORT = os.environ.get('PORT', LOCAL_PORT)
        self.DB_CONNECTION_PARAMETERS = None
        self.DB_PORT = os.environ.get('DB_PORT', 5433)
        self.DB_NAME = 'simple_movie_database'
        self.DB_USER = 'postgres'


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


class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.PORT = os.environ['PORT']
        self.ENV = 'production'
