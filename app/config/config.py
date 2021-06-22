# config for user scopes
DEFAULT_USER_SCOPES = {
    "super_admin": [],
    "admin": [],
    "monitor": [],
    "visitor": []
}

# config for logger
LOGGER_PATH = 'logs/'
LOGGER_FILENAME = 'app.log'
LOGGER_MAX_SIZE = 1000000
LOGGER_MAX_FILES = 100


# config for database
DATABASE_CONFIG = {
    "DATABASE_ENGINE" : 'postgresql',
    "DATABASE_USERNAME" : 'test_fast_api',
    "DATABASE_PASSWORD" : 'test_fast_api',
    "DATABASE_HOST" : 'localhost',
    "DATABASE_PORT" : 5432,
    "DATABASE_NAME" : 'test_fast_api'
}


# config for cors middleware
ALLOWED_ORIGINS = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
