# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # MongoDB 配置
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017'
    MONGO_DATABASE = os.environ.get('MONGO_DATABASE') or 'spider_system'
    
    # 爬虫相关配置
    SPIDER_SCRIPTS_BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spider-scripts')
    SPIDER_RUNNER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'spider-runner')