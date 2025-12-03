# 工商联用户管理 - 后端API实现指南

## 一、数据库表设计

### 1. 创建用户表
```sql
CREATE TABLE chamber_users (
  id VARCHAR(36) PRIMARY KEY COMMENT '用户ID',
  username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
  email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
  password VARCHAR(255) NOT NULL COMMENT '密码(bcrypt加密)',
  real_name VARCHAR(50) COMMENT '真实姓名',
  phone VARCHAR(20) COMMENT '手机号',
  level ENUM('county', 'province', 'national') NOT NULL COMMENT '层级：县市/省级/全联',
  region VARCHAR(100) COMMENT '地区',
  role ENUM('admin', 'reviewer', 'operator') DEFAULT 'operator' COMMENT '角色',
  review_level ENUM('beginner', 'intermediate', 'advanced') COMMENT '审核权限等级',
  department VARCHAR(100) COMMENT '部门',
  position VARCHAR(100) COMMENT '职位',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  status ENUM('active', 'inactive', 'pending') DEFAULT 'pending' COMMENT '状态',
  remark TEXT COMMENT '备注',
  created_by VARCHAR(36) COMMENT '创建人ID',
  
  INDEX idx_level_region (level, region),
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### 2. 创建操作日志表
```sql
CREATE TABLE chamber_user_logs (
  id VARCHAR(36) PRIMARY KEY,
  operator_id VARCHAR(36) COMMENT '操作人ID',
  target_user_id VARCHAR(36) COMMENT '目标用户ID',
  action VARCHAR(50) COMMENT '操作类型: create/update/delete/status_change',
  old_value JSON COMMENT '旧值',
  new_value JSON COMMENT '新值',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_operator_id (operator_id),
  INDEX idx_target_user_id (target_user_id),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 二、权限检查工具类

### Python/Flask 示例
```python
from functools import wraps
from flask import request, jsonify, session
from datetime import datetime

class PermissionChecker:
    """权限检查工具"""
    
    @staticmethod
    def get_current_user():
        """获取当前登录用户"""
        user_id = session.get('user_id')
        if not user_id:
            return None
        # 从数据库获取用户信息
        return db.query(ChamberUser).filter_by(id=user_id).first()
    
    @staticmethod
    def can_view_user(current_user, target_user):
        """检查是否可以查看用户"""
        # 全联管理员可以看所有用户
        if current_user.level == 'national':
            return True
        
        # 省级管理员可以看本省的用户
        if current_user.level == 'province':
            return target_user.level in ['county', 'province'] and \
                   target_user.region == current_user.region
        
        # 县市级管理员只能看本县市的用户
        if current_user.level == 'county':
            return target_user.level == 'county' and \
                   target_user.region == current_user.region
        
        return False
    
    @staticmethod
    def can_edit_user(current_user, target_user):
        """检查是否可以编辑用户"""
        # 全联管理员可以编辑所有用户
        if current_user.level == 'national':
            return True
        
        # 省级管理员可以编辑本省的用户（不能编辑管理员）
        if current_user.level == 'province':
            if target_user.role == 'admin':
                return False
            return target_user.level in ['county', 'province'] and \
                   target_user.region == current_user.region
        
        # 县市级管理员只能编辑本县市的操作员和审核员
        if current_user.level == 'county':
            if target_user.role in ['admin', 'reviewer']:
                return False
            return target_user.level == 'county' and \
                   target_user.region == current_user.region
        
        return False
    
    @staticmethod
    def can_delete_user(current_user, target_user):
        """检查是否可以删除用户"""
        # 全联管理员可以删除所有用户
        if current_user.level == 'national':
            return True
        
        # 省级管理员可以删除本省的操作员
        if current_user.level == 'province':
            if target_user.role != 'operator':
                return False
            return target_user.level in ['county', 'province'] and \
                   target_user.region == current_user.region
        
        # 县市级管理员只能删除本县市的操作员
        if current_user.level == 'county':
            if target_user.role != 'operator':
                return False
            return target_user.level == 'county' and \
                   target_user.region == current_user.region
        
        return False
    
    @staticmethod
    def can_create_user(current_user, new_user_level, new_user_region):
        """检查是否可以创建用户"""
        # 不能创建高于自己权限的用户
        level_hierarchy = {'county': 1, 'province': 2, 'national': 3}
        
        if level_hierarchy.get(new_user_level, 0) > level_hierarchy.get(current_user.level, 0):
            return False
        
        # 检查地区权限
        if current_user.level == 'national':
            return True
        
        if current_user.level == 'province':
            return new_user_level in ['county', 'province'] and \
                   new_user_region == current_user.region
        
        if current_user.level == 'county':
            return new_user_level == 'county' and \
                   new_user_region == current_user.region
        
        return False


def require_permission(permission_func):
    """权限检查装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = PermissionChecker.get_current_user()
            if not current_user:
                return jsonify({'success': False, 'error': '未登录'}), 401
            
            if not permission_func(current_user):
                return jsonify({'success': False, 'error': '权限不足'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

---

## 三、API 实现

### 1. 获取用户列表
```python
@app.route('/api/portal/chamber/users', methods=['GET'])
def get_chamber_users():
    """获取工商联用户列表"""
    try:
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        keyword = request.args.get('keyword', '')
        level = request.args.get('level', '')
        role = request.args.get('role', '')
        status = request.args.get('status', '')
        
        # 构建查询
        query = db.query(ChamberUser)
        
        # 权限过滤
        if current_user.level == 'county':
            query = query.filter_by(level='county', region=current_user.region)
        elif current_user.level == 'province':
            query = query.filter(
                (ChamberUser.level.in_(['county', 'province'])) &
                (ChamberUser.region == current_user.region)
            )
        # national 可以看所有用户
        
        # 条件过滤
        if keyword:
            query = query.filter(
                (ChamberUser.username.ilike(f'%{keyword}%')) |
                (ChamberUser.email.ilike(f'%{keyword}%')) |
                (ChamberUser.real_name.ilike(f'%{keyword}%'))
            )
        
        if level:
            query = query.filter_by(level=level)
        
        if role:
            query = query.filter_by(role=role)
        
        if status:
            query = query.filter_by(status=status)
        
        # 排序和分页
        total = query.count()
        users = query.order_by(ChamberUser.created_at.desc()) \
                     .offset((page - 1) * limit) \
                     .limit(limit) \
                     .all()
        
        # 构建响应
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'real_name': user.real_name,
                'phone': user.phone,
                'level': user.level,
                'region': user.region,
                'role': user.role,
                'review_level': user.review_level,
                'department': user.department,
                'position': user.position,
                'status': user.status,
                'created_at': user.created_at.isoformat(),
                'remark': user.remark
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'page': page,
                'limit': limit,
                'users': user_list
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 2. 创建用户
```python
@app.route('/api/portal/chamber/users', methods=['POST'])
def create_chamber_user():
    """创建工商联用户"""
    try:
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'email', 'password', 'level', 'region', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
        
        # 权限检查
        if not PermissionChecker.can_create_user(current_user, data['level'], data['region']):
            return jsonify({'success': False, 'error': '权限不足，不能创建该用户'}), 403
        
        # 检查用户名和邮箱唯一性
        if db.query(ChamberUser).filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': '用户名已存在'}), 400
        
        if db.query(ChamberUser).filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': '邮箱已存在'}), 400
        
        # 密码验证
        password = data['password']
        if len(password) < 8:
            return jsonify({'success': False, 'error': '密码至少8位'}), 400
        
        # 创建用户
        user = ChamberUser(
            id=str(uuid.uuid4()),
            username=data['username'],
            email=data['email'],
            password=bcrypt.hashpw(password.encode(), bcrypt.gensalt()),
            real_name=data.get('real_name'),
            phone=data.get('phone'),
            level=data['level'],
            region=data['region'],
            role=data['role'],
            review_level=data.get('review_level'),
            department=data.get('department'),
            position=data.get('position'),
            status=data.get('status', 'pending'),
            remark=data.get('remark'),
            created_by=current_user.id
        )
        
        db.add(user)
        db.commit()
        
        # 记录操作日志
        log_operation(current_user.id, user.id, 'create', None, user.to_dict())
        
        return jsonify({
            'success': True,
            'data': {
                'id': user.id,
                'username': user.username,
                'message': '用户创建成功'
            }
        })
    
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 3. 更新用户
```python
@app.route('/api/portal/chamber/users/<user_id>', methods=['PUT'])
def update_chamber_user(user_id):
    """更新工商联用户"""
    try:
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        target_user = db.query(ChamberUser).filter_by(id=user_id).first()
        if not target_user:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
        
        # 权限检查
        if not PermissionChecker.can_edit_user(current_user, target_user):
            return jsonify({'success': False, 'error': '权限不足'}), 403
        
        data = request.get_json()
        old_value = target_user.to_dict()
        
        # 更新字段
        if 'email' in data:
            # 检查邮箱唯一性
            existing = db.query(ChamberUser).filter(
                ChamberUser.email == data['email'],
                ChamberUser.id != user_id
            ).first()
            if existing:
                return jsonify({'success': False, 'error': '邮箱已被使用'}), 400
            target_user.email = data['email']
        
        if 'password' in data and data['password']:
            if len(data['password']) < 8:
                return jsonify({'success': False, 'error': '密码至少8位'}), 400
            target_user.password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        
        if 'real_name' in data:
            target_user.real_name = data['real_name']
        
        if 'phone' in data:
            target_user.phone = data['phone']
        
        if 'role' in data:
            target_user.role = data['role']
        
        if 'review_level' in data:
            target_user.review_level = data['review_level']
        
        if 'department' in data:
            target_user.department = data['department']
        
        if 'position' in data:
            target_user.position = data['position']
        
        if 'status' in data:
            target_user.status = data['status']
        
        if 'remark' in data:
            target_user.remark = data['remark']
        
        target_user.updated_at = datetime.now()
        db.commit()
        
        # 记录操作日志
        log_operation(current_user.id, user_id, 'update', old_value, target_user.to_dict())
        
        return jsonify({
            'success': True,
            'data': {
                'id': user_id,
                'message': '用户更新成功'
            }
        })
    
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 4. 删除用户
```python
@app.route('/api/portal/chamber/users/<user_id>', methods=['DELETE'])
def delete_chamber_user(user_id):
    """删除工商联用户"""
    try:
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        target_user = db.query(ChamberUser).filter_by(id=user_id).first()
        if not target_user:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
        
        # 权限检查
        if not PermissionChecker.can_delete_user(current_user, target_user):
            return jsonify({'success': False, 'error': '权限不足'}), 403
        
        old_value = target_user.to_dict()
        db.delete(target_user)
        db.commit()
        
        # 记录操作日志
        log_operation(current_user.id, user_id, 'delete', old_value, None)
        
        return jsonify({'success': True, 'message': '用户删除成功'})
    
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 5. 获取用户详情
```python
@app.route('/api/portal/chamber/users/<user_id>', methods=['GET'])
def get_chamber_user(user_id):
    """获取用户详情"""
    try:
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        target_user = db.query(ChamberUser).filter_by(id=user_id).first()
        if not target_user:
            return jsonify({'success': False, 'error': '用户不存在'}), 404
        
        # 权限检查
        if not PermissionChecker.can_view_user(current_user, target_user):
            return jsonify({'success': False, 'error': '权限不足'}), 403
        
        return jsonify({
            'success': True,
            'data': target_user.to_dict()
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 6. 导出用户
```python
@app.route('/api/portal/chamber/users/export', methods=['GET'])
def export_chamber_users():
    """导出用户列表为Excel"""
    try:
        import openpyxl
        from io import BytesIO
        
        current_user = PermissionChecker.get_current_user()
        if not current_user:
            return jsonify({'success': False, 'error': '未登录'}), 401
        
        # 获取查询参数
        keyword = request.args.get('keyword', '')
        level = request.args.get('level', '')
        role = request.args.get('role', '')
        status = request.args.get('status', '')
        
        # 构建查询（同列表接口）
        query = db.query(ChamberUser)
        
        if current_user.level == 'county':
            query = query.filter_by(level='county', region=current_user.region)
        elif current_user.level == 'province':
            query = query.filter(
                (ChamberUser.level.in_(['county', 'province'])) &
                (ChamberUser.region == current_user.region)
            )
        
        if keyword:
            query = query.filter(
                (ChamberUser.username.ilike(f'%{keyword}%')) |
                (ChamberUser.email.ilike(f'%{keyword}%')) |
                (ChamberUser.real_name.ilike(f'%{keyword}%'))
            )
        
        if level:
            query = query.filter_by(level=level)
        
        if role:
            query = query.filter_by(role=role)
        
        if status:
            query = query.filter_by(status=status)
        
        users = query.all()
        
        # 创建Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = '工商联用户'
        
        # 写入表头
        headers = ['用户名', '邮箱', '真实姓名', '手机', '层级', '地区', '角色', 
                   '审核权限', '部门', '职位', '状态', '创建时间', '备注']
        ws.append(headers)
        
        # 写入数据
        for user in users:
            ws.append([
                user.username,
                user.email,
                user.real_name or '',
                user.phone or '',
                user.level,
                user.region or '',
                user.role,
                user.review_level or '',
                user.department or '',
                user.position or '',
                user.status,
                user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                user.remark or ''
            ])
        
        # 返回文件
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'工商联用户_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## 四、操作日志记录

```python
def log_operation(operator_id, target_user_id, action, old_value, new_value):
    """记录用户操作日志"""
    try:
        log = ChamberUserLog(
            id=str(uuid.uuid4()),
            operator_id=operator_id,
            target_user_id=target_user_id,
            action=action,
            old_value=json.dumps(old_value, default=str) if old_value else None,
            new_value=json.dumps(new_value, default=str) if new_value else None
        )
        db.add(log)
        db.commit()
    except Exception as e:
        print(f"记录日志失败: {e}")
```

---

## 五、模型定义

```python
from sqlalchemy import Column, String, Enum, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class ChamberUser(Base):
    __tablename__ = 'chamber_users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    real_name = Column(String(50))
    phone = Column(String(20))
    level = Column(Enum('county', 'province', 'national'), nullable=False)
    region = Column(String(100))
    role = Column(Enum('admin', 'reviewer', 'operator'), default='operator')
    review_level = Column(Enum('beginner', 'intermediate', 'advanced'))
    department = Column(String(100))
    position = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(Enum('active', 'inactive', 'pending'), default='pending')
    remark = Column(Text)
    created_by = Column(String(36))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'phone': self.phone,
            'level': self.level,
            'region': self.region,
            'role': self.role,
            'review_level': self.review_level,
            'department': self.department,
            'position': self.position,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'remark': self.remark
        }


class ChamberUserLog(Base):
    __tablename__ = 'chamber_user_logs'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    operator_id = Column(String(36))
    target_user_id = Column(String(36))
    action = Column(String(50))
    old_value = Column(JSON)
    new_value = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
```

---

## 六、测试用例

### 测试场景清单
```
1. 权限测试
   - [ ] 县市级管理员只能看到本县市用户
   - [ ] 省级管理员能看到本省所有用户
   - [ ] 全联管理员能看到所有用户
   - [ ] 不能创建高于自己权限的用户
   - [ ] 不能删除高于自己权限的用户

2. 数据验证测试
   - [ ] 用户名唯一性验证
   - [ ] 邮箱唯一性验证
   - [ ] 密码长度验证
   - [ ] 必填字段验证

3. CRUD测试
   - [ ] 创建用户成功
   - [ ] 更新用户信息成功
   - [ ] 删除用户成功
   - [ ] 查询用户成功
   - [ ] 分页查询成功

4. 状态管理测试
   - [ ] 用户状态转换正确
   - [ ] 停用用户无法登录
   - [ ] 激活用户可以登录

5. 日志记录测试
   - [ ] 所有操作都被记录
   - [ ] 日志内容准确
```


