from flask import Blueprint, request, jsonify, current_app
from app import mongo, jwt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

bp = Blueprint('api', __name__)

# 辅助函数：获取 users 集合
def get_users_collection():
    return mongo.users

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Backend is running with MongoDB'})

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 检查用户名和邮箱是否已存在
    users_collection = get_users_collection()
    if users_collection.find_one({'username': data['username']}):
        return jsonify({'message': 'Username already exists'}), 400
    
    if users_collection.find_one({'email': data['email']}):
        return jsonify({'message': 'Email already exists'}), 400
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # 保存到 MongoDB
    user_data = user.to_dict()
    user_data['password_hash'] = user.password_hash
    user_data['created_at'] = user.created_at
    
    result = users_collection.insert_one(user_data)
    user_data['_id'] = str(result.inserted_id)
    
    return jsonify({'message': 'User created successfully', 'user': user_data}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # 查找用户
    users_collection = get_users_collection()
    user_data = users_collection.find_one({'username': data['username']})
    
    if user_data:
        # 创建临时 User 对象用于密码验证
        temp_user = User.from_dict(user_data)
        temp_user.password_hash = user_data['password_hash']
        
        if temp_user.check_password(data['password']):
            access_token = create_access_token(identity=str(user_data['_id']))
            user_dict = temp_user.to_dict()
            user_dict['_id'] = str(user_data['_id'])  # 确保 ID 是字符串
            return jsonify({
                'access_token': access_token,
                'user': user_dict
            }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users_collection = get_users_collection()
    users_cursor = users_collection.find({})
    
    users_list = []
    for user_data in users_cursor:
        user = User.from_dict(user_data)
        user.password_hash = user_data['password_hash']  # 保留密码哈希但不返回给客户端
        user_dict = user.to_dict()
        user_dict['_id'] = str(user_data['_id'])
        users_list.append(user_dict)
    
    return jsonify(users_list), 200

@bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    users_collection = get_users_collection()
    try:
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            user = User.from_dict(user_data)
            user.password_hash = user_data['password_hash']
            user_dict = user.to_dict()
            user_dict['_id'] = str(user_data['_id'])
            return jsonify(user_dict), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception:
        return jsonify({'message': 'Invalid user ID'}), 400