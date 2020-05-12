import os

from my_app.config import Config

environment = os.getenv('ENV', 'dev')
settings = Config()
