# Spider System Backend

基于 Flask 的后端服务，用于爬虫系统的用户管理和数据处理。

## 项目结构

```
app/
├── models/          # 数据模型
├── repositories/    # 数据访问层
├── services/        # 业务逻辑层
├── routes/          # API路由层
├── utils/           # 工具类
├── __init__.py      # Flask应用工厂
config.py            # 配置文件
run.py               # 应用入口
```

## 技术栈

- Flask: Web框架
- MongoDB: 数据库
- Flask-JWT-Extended: JWT认证
- Python 3.8+

## 安装与运行

### 环境要求

- Python 3.8+
- MongoDB 4.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件或设置以下环境变量：

```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=spider_system
```

### 运行应用

```bash
python run.py
```

## API接口

### 健康检查

```
GET /api/health
```

### 用户注册

```
POST /api/register
Content-Type: application/json

{
  "username": "example_user",
  "email": "user@example.com",
  "password": "secure_password"
}
```

### 用户登录

```
POST /api/login
Content-Type: application/json

{
  "username": "example_user",
  "password": "secure_password"
}
```

### 获取用户列表

```
GET /api/users
Authorization: Bearer <access_token>
```

### 获取指定用户

```
GET /api/users/<user_id>
Authorization: Bearer <access_token>
```

## 架构设计

本项目采用分层架构设计：

1. **Routes层**: 处理HTTP请求和响应
2. **Services层**: 实现业务逻辑
3. **Repositories层**: 处理数据访问
4. **Models层**: 定义数据模型

## 认证机制

使用JWT进行用户认证，登录成功后会返回access_token，后续请求需要在Header中携带：

```
Authorization: Bearer <access_token>
```

## 错误处理

API会返回标准的JSON格式错误信息：

```json
{
  "message": "错误描述"
}
```