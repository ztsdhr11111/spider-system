# app/repositories/spider_repository.py
from app import mongo
from app.models.spider import Spider, SpiderRun
from bson import ObjectId
from typing import Optional, List

class SpiderRepository:
    def __init__(self):
        self.spiders_collection = mongo.spiders
        self.spider_runs_collection = mongo.spider_runs
    
    def find_all_spiders(self) -> List[Spider]:
        """获取所有爬虫"""
        spiders_data = list(self.spiders_collection.find({}))
        return [Spider.from_dict(spider_data) for spider_data in spiders_data]
    
    def find_spider_by_id(self, spider_id: str) -> Optional[Spider]:
        """根据ID查找爬虫"""
        try:
            spider_data = self.spiders_collection.find_one({'_id': ObjectId(spider_id)})
            return Spider.from_dict(spider_data) if spider_data else None
        except Exception:
            return None
    
    def save_spider(self, spider: Spider) -> str:
        """保存爬虫"""
        spider_data = spider.to_dict()
        if spider_data['_id']:
            # 更新操作
            spider_id = spider_data['_id']
            del spider_data['_id']
            self.spiders_collection.update_one(
                {'_id': ObjectId(spider_id)}, 
                {'$set': spider_data}
            )
        else:
            # 插入操作
            result = self.spiders_collection.insert_one(spider_data)
            spider_id = str(result.inserted_id)
        return spider_id
    
    def delete_spider(self, spider_id: str) -> bool:
        """删除爬虫"""
        result = self.spiders_collection.delete_one({'_id': ObjectId(spider_id)})
        return result.deleted_count > 0
    
    def save_spider_run(self, run: SpiderRun) -> str:
        """保存运行记录"""
        run_data = run.to_dict()
        if run_data['_id']:
            # 更新操作
            run_id = run_data['_id']
            del run_data['_id']
            self.spider_runs_collection.update_one(
                {'_id': ObjectId(run_id)}, 
                {'$set': run_data}
            )
        else:
            # 插入操作
            result = self.spider_runs_collection.insert_one(run_data)
            run_id = str(result.inserted_id)
        return run_id
    
    def find_spider_runs(self, spider_id: str = None, limit: int = 50) -> List[SpiderRun]:
        """获取运行记录"""
        query = {}
        if spider_id:
            query['spider_id'] = spider_id
        
        runs_data = list(self.spider_runs_collection.find(query).sort('start_time', -1).limit(limit))
        return [SpiderRun.from_dict(run_data) for run_data in runs_data]