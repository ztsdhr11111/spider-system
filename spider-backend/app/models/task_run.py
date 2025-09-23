# app/models/task_run.py
from datetime import datetime

class TaskRun:
    def __init__(self, task_id, spider_id, status, parameters=None, start_time=None, 
                 end_time=None, log_output=None, error_message=None, _id=None):
        self._id = _id
        self.task_id = task_id
        self.spider_id = spider_id
        self.status = status
        self.parameters = parameters
        self.start_time = start_time or datetime.utcnow()
        self.end_time = end_time
        self.log_output = log_output or ''
        self.error_message = error_message
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'task_id': self.task_id,
            'spider_id': self.spider_id,
            'status': self.status,
            'parameters': self.parameters,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'log_output': self.log_output,
            'error_message': self.error_message
        }
    
    @staticmethod
    def from_dict(data):
        run = TaskRun(
            task_id=data['task_id'],
            spider_id=data['spider_id'],
            status=data['status'],
            parameters=data.get('parameters'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            log_output=data.get('log_output', ''),
            error_message=data.get('error_message'),
            _id=data.get('_id')
        )
        
        # 转换字符串为datetime对象
        if isinstance(run.start_time, str):
            run.start_time = datetime.fromisoformat(run.start_time.replace('Z', '+00:00'))
        if isinstance(run.end_time, str):
            run.end_time = datetime.fromisoformat(run.end_time.replace('Z', '+00:00'))
            
        return run