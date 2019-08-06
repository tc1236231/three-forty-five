import os

from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': os.getenv('REDIS_HOST', ''),
    'CACHE_REDIS_PORT': os.getenv('REDIS_PORT', ''),
    'CACHE_REDIS_PASSWORD': os.getenv('REDIS_PASSWORD', '')
                      })
