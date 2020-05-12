import os


class Config(object):
    """
    Base config class
    """
    ENV = os.getenv('ENV', 'dev')
    TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Kolkata')

    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST,
        port=POSTGRES_PORT, db=POSTGRES_DB
    )

    REDIS_DB_FOR_APPLICATION = int(os.getenv('REDIS_DB_FOR_APPLICATION', 0))
    REDIS_HOSTNAME = os.getenv('REDIS_HOSTNAME')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
