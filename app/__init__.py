#-*- coding: utf-8 -*-
# ./app/__init__.py
import os 
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

from flask_cors import CORS

from app.routes.chat_routes import chat_routes
from .config.Config import api, db, jwt
from .config.DBConfig import MySQLConfig
from .controller.controller import register_namespaces
import warnings

import redis

app = Flask(__name__)

CORS(app, supports_credentials=True,  resources={r"/*": {
    "origins": "http://localhost:3000",
    "expose_headers": ["access_token", "refresh_token"],
    "allow_headers": ["Content-Type", "Authorization", "accept"]
}})

app.config['JSON_AS_ASCII'] = False

app.config.from_object(MySQLConfig)

'''JWT 설정'''
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 30 * 24 *  60 * 60
# app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 
''''''
# JST SECRET KEY
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET_KEY')

# SECRET_KEY 설정
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

'''Redis - Session 설정'''
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)
api.init_app(app)
db.init_app(app)
jwt.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*", message_queue= f'redis://{REDIS_HOST}:{REDIS_PORT}', 
                    logger=True)
register_namespaces(api)
chat_routes(socketio, redis_client)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    socketio.run(app= app)

