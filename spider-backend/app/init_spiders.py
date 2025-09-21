# app/init_spiders.py
import os
from app.repositories.spider_repository import SpiderRepository
from app.models.spider import Spider
from config import Config

def init_default_spiders():
    """初始化默认爬虫"""
    spider_repo = SpiderRepository()
    
    # 检查是否已存在zhaobiao爬虫
    existing_spiders = spider_repo.find_all_spiders()
    zhaobiao_exists = any(spider.name == '招标网站爬虫' for spider in existing_spiders)
    
    if not zhaobiao_exists:
        # 创建zhaobiao爬虫
        zhaobiao_path = os.path.join(Config.SPIDER_SCRIPTS_BASE_DIR, 'zhaobiao')
        if os.path.exists(zhaobiao_path):
            spider = Spider(
                name='招标网站爬虫',
                description='抓取招标网站数据',
                script_path=zhaobiao_path,
                main_module='main.py'
            )
            spider_repo.save_spider(spider)
            print("Default spider 'zhaobiao' initialized")