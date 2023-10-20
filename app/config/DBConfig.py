import os 
from redis import Redis

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PORT = os.environ.get('DB_PORT')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

## REDIS 설정
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

class MySQLConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config(object):
    # Parse redis environment variables.
    SESSION_TYPE = "redis"
    redis_client = Redis(
        host=REDIS_HOST, port=REDIS_PORT
    )
    SESSION_REDIS = redis_client
