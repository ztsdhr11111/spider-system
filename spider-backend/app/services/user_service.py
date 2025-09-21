# services/user_service.py
from app.repositories.user_repository import UserRepository
from app.models import User
from typing import Optional, List

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
    
    def register_user(self, username: str, email: str, password: str) -> dict:
        """用户注册业务逻辑"""
        # 检查用户名是否已存在
        if self.user_repository.find_by_username(username):
            raise ValueError('Username already exists')
        
        # 检查邮箱是否已存在
        if self.user_repository.find_by_email(email):
            raise ValueError('Email already exists')
        
        # 创建新用户
        user = User(username=username, email=email, password=password)
        user_id = self.user_repository.save(user)
        
        # 返回用户信息
        user_data = user.to_dict()
        user_data['_id'] = user_id
        user_data['password_hash'] = user.password_hash
        user_data['created_at'] = user.created_at
        
        return user_data
    
    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """用户认证业务逻辑"""
        user_data = self.user_repository.find_by_username(username)
        
        if user_data:
            temp_user = User.from_dict(user_data)
            temp_user.password_hash = user_data['password_hash']
            
            if temp_user.check_password(password):
                user_dict = temp_user.to_dict()
                user_dict['_id'] = str(user_data['_id'])
                return user_dict
        
        return None
    
    def get_all_users(self) -> List[dict]:
        """获取所有用户业务逻辑"""
        users_data = self.user_repository.find_all()
        users_list = []
        
        for user_data in users_data:
            user = User.from_dict(user_data)
            user.password_hash = user_data['password_hash']
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_data['_id'])
            users_list.append(user_dict)
        
        return users_list
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """根据ID获取用户业务逻辑"""
        user_data = self.user_repository.find_by_id(user_id)
        
        if user_data:
            user = User.from_dict(user_data)
            user.password_hash = user_data['password_hash']
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_data['_id'])
            return user_dict
        
        return None