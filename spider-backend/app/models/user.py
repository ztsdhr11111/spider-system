from datetime import datetime
# 强制使用 pbkdf2 方法
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password=None, created_at=None, _id=None):
        self._id = _id
        self.username = username
        self.email = email
        self.password_hash = self.set_password(password) if password else None
        self.created_at = created_at or datetime.utcnow()
    
    def set_password(self, password):
        if password:
            # 强制使用 pbkdf2 方法，避免使用 scrypt
            return generate_password_hash(password, method='pbkdf2:sha256', salt_length=12)
        return None
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            '_id': str(self._id) if self._id else None,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        user = User(
            username=data['username'],
            email=data['email'],
            _id=data.get('_id'),
            created_at=data.get('created_at')
        )
        if isinstance(user.created_at, str):
            user.created_at = datetime.fromisoformat(user.created_at.replace('Z', '+00:00'))
        return user