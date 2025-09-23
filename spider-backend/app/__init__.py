# app/__init__.py
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
        mongo = client['spider_system']
    
    # 创建必要的集合
    if 'spiders' not in mongo.list_collection_names():
        mongo.create_collection('spiders')
    if 'spider_runs' not in mongo.list_collection_names():
        mongo.create_collection('spider_runs')
    # 添加任务相关的集合
    if 'tasks' not in mongo.list_collection_names():
        mongo.create_collection('tasks')
    if 'task_runs' not in mongo.list_collection_names():
        mongo.create_collection('task_runs')

    jwt.init_app(app)
    
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.routes.spider_routes import bp as spiders_bp
    app.register_blueprint(spiders_bp, url_prefix='/api')

    from app.routes.task_routes import task_bp as tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    # 添加调试信息，确认蓝图已注册
    print("Registered blueprints:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.endpoint}: {rule.rule}")
    
    return app