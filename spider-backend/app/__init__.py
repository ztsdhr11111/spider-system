from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from config import Config
import os

mongo = None
jwt = JWTManager()

def create_app(config_class=Config):
    global mongo
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化 MongoDB 连接
    if Config.MONGO_URI:
        client = MongoClient(Config.MONGO_URI)
        mongo = client[Config.MONGO_DATABASE]
    else:
        # 默认本地连接
        client = MongoClient('localhost', 27017)
        mongo = client['spider_backend']
    
    jwt.init_app(app)
    
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app