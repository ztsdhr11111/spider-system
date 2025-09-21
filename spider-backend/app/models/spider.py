# app/models/spider.py
from datetime import datetime

class Spider:
    def __init__(self, name, description, script_path, main_module='main.py', _id=None, created_at=None):
        self._id = _id
        self.name = name
        self.description = description
        self.script_path = script_path
        self.main_module = main_module
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.enabled = True
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'description': self.description,
            'script_path': self.script_path,
            'main_module': self.main_module,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'enabled': self.enabled
        }
    
    @staticmethod
    def from_dict(data):
        spider = Spider(
            name=data['name'],
            description=data['description'],
            script_path=data['script_path'],
            main_module=data.get('main_module', 'main.py'),
            _id=data.get('_id'),
            created_at=data.get('created_at')
        )
        if isinstance(spider.created_at, str):
            spider.created_at = datetime.fromisoformat(spider.created_at.replace('Z', '+00:00'))
        if 'updated_at' in data:
            spider.updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
        spider.enabled = data.get('enabled', True)
        return spider

class SpiderRun:
    def __init__(self, spider_id, status='pending', start_time=None, end_time=None, result_data=None, log_output=None, error_message=None, _id=None):
        self._id = _id
        self.spider_id = spider_id
        self.status = status
        self.start_time = start_time or datetime.utcnow()
        self.end_time = end_time
        self.result_data = result_data or {}
        self.log_output = log_output or ''
        self.error_message = error_message
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'spider_id': str(self.spider_id),
            'status': self.status,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'result_data': self.result_data,
            'log_output': self.log_output,
            'error_message': self.error_message
        }
    
    @staticmethod
    def from_dict(data):
        run = SpiderRun(
            spider_id=data['spider_id'],
            status=data.get('status', 'pending'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            result_data=data.get('result_data', {}),
            log_output=data.get('log_output', ''),
            error_message=data.get('error_message'),
            _id=data.get('_id')
        )
        if isinstance(run.start_time, str):
            run.start_time = datetime.fromisoformat(run.start_time.replace('Z', '+00:00'))
        if isinstance(run.end_time, str):
            run.end_time = datetime.fromisoformat(run.end_time.replace('Z', '+00:00'))
        return run