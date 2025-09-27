# spider-scripts/base_spider.py
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class BaseSpider(ABC):
    """
    爬虫基类，所有爬虫脚本都应该继承此类
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.start_time = None
        self.end_time = None
    
    @abstractmethod
    def run(self):
        """
        抽象方法，子类必须实现具体的爬虫逻辑
        返回格式应为:
        {
            "status": "success|failed",
            "items_count": int,
            "data": list,  # 可选，爬取的数据
            "message": str  # 可选，额外信息
        }
        """
        pass
    
    def execute(self):
        """
        执行爬虫的主方法，处理异常和时间记录
        """
        self.start_time = datetime.now()
        try:
            self.logger.info(f"开始执行爬虫: {self.__class__.__name__}")
            
            # 调用子类实现的run方法
            result = self.run()
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            # 确保返回结果格式正确
            if not isinstance(result, dict):
                result = {"data": result}
            
            # 补充标准字段
            result.setdefault("status", "success")
            result.setdefault("items_count", 0)
            result.setdefault("duration", duration)
            result.setdefault("start_time", self.start_time.isoformat())
            result.setdefault("end_time", self.end_time.isoformat())
            
            self.logger.info(f"爬虫执行完成: {self.__class__.__name__}, 耗时: {duration}秒")
            return result
            
        except Exception as e:
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds() if self.start_time else 0
            
            error_result = {
                "status": "failed",
                "items_count": 0,
                "error": str(e),
                "duration": duration,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None
            }
            
            self.logger.error(f"爬虫执行失败: {self.__class__.__name__}, 错误: {str(e)}")
            return error_result
    
    def log_info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def log_error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def log_warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)

# 兼容旧版本的run函数接口
def run_spider(spider_class):
    """
    运行继承自BaseSpider的爬虫类
    """
    spider = spider_class()
    return spider.execute()