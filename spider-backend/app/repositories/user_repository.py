# repositories/user_repository.py
from app import mongo
from app.models import User
from bson import ObjectId
from typing import Optional, List

class UserRepository:
    def __init__(self):
        self.collection = mongo.users
    
    def find_by_username(self, username: str) -> Optional[dict]:
        """根据用户名查找用户"""
        return self.collection.find_one({'username': username})
    
    def find_by_email(self, email: str) -> Optional[dict]:
        """根据邮箱查找用户"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id: str) -> Optional[dict]:
        """根据ID查找用户"""
        try:
            return self.collection.find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None
    
    def find_all(self) -> List[dict]:
        """获取所有用户"""
        return list(self.collection.find({}))
    
    def save(self, user: User) -> str:
        """保存用户"""
        user_data = user.to_dict()
        user_data['password_hash'] = user.password_hash
        user_data['created_at'] = user.created_at
        
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)