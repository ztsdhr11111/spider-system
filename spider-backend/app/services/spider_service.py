# app/services/spider_service.py
import os
import sys
from datetime import datetime
import json
from app.repositories.spider_repository import SpiderRepository
from app.models.spider import Spider, SpiderRun
from app.utils.exceptions import BusinessError

class SpiderService:
    def __init__(self):
        self.spider_repository = SpiderRepository()
    
    def get_all_spiders(self):
        """获取所有爬虫"""
        spiders = self.spider_repository.find_all_spiders()
        return [spider.to_dict() for spider in spiders]
    
    def get_spider_by_id(self, spider_id):
        """根据ID获取爬虫"""
        spider = self.spider_repository.find_spider_by_id(spider_id)
        return spider.to_dict() if spider else None
    
    def _get_project_root(self):
        """获取项目根目录"""
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    def _resolve_script_path(self, script_path):
        """解析脚本路径为绝对路径"""
        if os.path.isabs(script_path):
            return script_path
        else:
            project_root = self._get_project_root()
            return os.path.join(project_root, script_path)

    def create_spider(self, spider_data):
        """创建爬虫"""
        # 验证脚本路径是否存在
        script_path = spider_data.get('script_path')
        full_script_path = self._resolve_script_path(script_path)
        
        # 检查路径是否存在
        if not os.path.exists(full_script_path):
            raise BusinessError(f'Script path does not exist: {script_path}')
        
        # 验证主模块是否存在
        main_module = spider_data.get('main_module', 'main.py')
        main_path = os.path.join(full_script_path, main_module)
        if not os.path.exists(main_path):
            raise BusinessError(f'Main module {main_module} does not exist')
        
        spider = Spider(
            name=spider_data['name'],
            description=spider_data['description'],
            script_path=script_path,  # 保存原始路径（可能是相对路径）
            main_module=main_module
        )
        
        spider_id = self.spider_repository.save_spider(spider)
        spider._id = spider_id
        return spider.to_dict()
    
    def update_spider(self, spider_id, spider_data):
        """更新爬虫"""
        spider = self.spider_repository.find_spider_by_id(spider_id)
        if not spider:
            raise BusinessError('Spider not found')
        
        # 更新字段
        if 'name' in spider_data:
            spider.name = spider_data['name']
        if 'description' in spider_data:
            spider.description = spider_data['description']
        if 'enabled' in spider_data:
            spider.enabled = spider_data['enabled']
        
        spider.updated_at = datetime.utcnow()
        self.spider_repository.save_spider(spider)
        return spider.to_dict()
    
    def delete_spider(self, spider_id):
        """删除爬虫"""
        return self.spider_repository.delete_spider(spider_id)
    
    def run_spider(self, spider_id):
        """运行爬虫"""
        spider = self.spider_repository.find_spider_by_id(spider_id)
        if not spider:
            raise BusinessError('Spider not found')
        
        if not spider.enabled:
            raise BusinessError('Spider is disabled')
        
        # 创建运行记录
        run = SpiderRun(spider_id=spider_id, status='running')
        run_id = self.spider_repository.save_spider_run(run)
        
        try:
            # 解析脚本路径
            script_path = spider.script_path
            full_script_path = self._resolve_script_path(script_path)
            
            # 确保路径存在
            if not os.path.exists(full_script_path):
                raise BusinessError(f'Script path does not exist: {script_path}')
            
            main_module = spider.main_module
            
            # 确保主模块存在
            main_path = os.path.join(full_script_path, main_module)
            if not os.path.exists(main_path):
                raise BusinessError(f'Main module {main_module} does not exist')
            
            # 动态导入runner模块并调用
            runner_path = os.path.join(self._get_project_root(), 'spider-runner')
            if runner_path not in sys.path:
                sys.path.insert(0, runner_path)
            
            import importlib.util
            runner_module_path = os.path.join(runner_path, 'runner.py')
            spec = importlib.util.spec_from_file_location("runner", runner_module_path)
            runner_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(runner_module)
            
            # 直接调用runner函数获取结果
            execution_result = runner_module.run_spider(full_script_path, main_module)
            print('execution_result:', execution_result)
            
            # 提取结果信息
            if execution_result.get("status") == "completed":
                spider_result = execution_result.get("result", {})
                status = spider_result.get("status", "unknown")
                message = spider_result.get("message", "")
                error = None
                log_output = json.dumps(spider_result, ensure_ascii=False, indent=2)
            else:
                status = execution_result.get("status", "unknown")
                message = execution_result.get("message", "")
                error = execution_result.get("error", None)
                log_output = execution_result.get("traceback", "")
            
            # 更新运行记录
            run.end_time = datetime.utcnow()
            run.status = status
            run.log_output = log_output
            run.error_message = error
            
            self.spider_repository.save_spider_run(run)
            
            return {
                'run_id': run_id,
                'status': status,
                'output': message,
                'error': error
            }
            
        except Exception as e:
            run.end_time = datetime.utcnow()
            run.status = 'failed'
            run.error_message = str(e)
            self.spider_repository.save_spider_run(run)
            raise BusinessError(f'Failed to run spider: {str(e)}')
    
    def get_spider_runs(self, spider_id=None):
        """获取爬虫运行记录"""
        runs = self.spider_repository.find_spider_runs(spider_id)
        return [run.to_dict() for run in runs]