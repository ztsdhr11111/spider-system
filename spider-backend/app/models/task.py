# app/models/task.py
from datetime import datetime

class Task:
    def __init__(self, name, spider_id, schedule_type, cron_expression=None, parameters=None, 
                 enabled=True, description=None, _id=None, created_at=None, updated_at=None,
                 scheduled_time=None, start_time=None, end_time=None, status='pending'):
        self._id = _id
        self.name = name
        self.spider_id = spider_id
        self.schedule_type = schedule_type
        self.cron_expression = cron_expression
        self.parameters = parameters
        self.enabled = enabled
        self.description = description
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.scheduled_time = scheduled_time
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'spider_id': self.spider_id,
            'schedule_type': self.schedule_type,
            'cron_expression': self.cron_expression,
            'parameters': self.parameters,
            'enabled': self.enabled,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        task = Task(
            name=data['name'],
            spider_id=data['spider_id'],
            schedule_type=data['schedule_type'],
            cron_expression=data.get('cron_expression'),
            parameters=data.get('parameters'),
            enabled=data.get('enabled', True),
            description=data.get('description'),
            _id=data.get('_id'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            scheduled_time=data.get('scheduled_time'),
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 'pending')
        )
        
        # 转换字符串为datetime对象
        if isinstance(task.created_at, str):
            task.created_at = datetime.fromisoformat(task.created_at.replace('Z', '+00:00'))
        if isinstance(task.updated_at, str):
            task.updated_at = datetime.fromisoformat(task.updated_at.replace('Z', '+00:00'))
        if isinstance(task.scheduled_time, str):
            task.scheduled_time = datetime.fromisoformat(task.scheduled_time.replace('Z', '+00:00'))
        if isinstance(task.start_time, str):
            task.start_time = datetime.fromisoformat(task.start_time.replace('Z', '+00:00'))
        if isinstance(task.end_time, str):
            task.end_time = datetime.fromisoformat(task.end_time.replace('Z', '+00:00'))
            
        return task