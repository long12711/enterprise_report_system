# 工商联用户管理 - 快速启动指南

## [object Object] 分钟快速开始

### 第 1 步：初始化数据库（1 分钟）

#### 使用 MySQL 客户端（推荐）

```bash
# 进入 MySQL
mysql -h localhost -u root -p

# 创建数据库
CREATE DATABASE IF NOT EXISTS enterprise_portal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE enterprise_portal;

# 执行所有 SQL 脚本
SOURCE db/all.sql;
```

#### 或使用 Python 脚本

```bash
python init_chamber_users_db.py
```

### 第 2 步：安装依赖（1 分钟）

```bash
pip install flask flask-sqlalchemy pymysql bcrypt openpyxl
```

### 第 3 步：启动应用（1 分钟）

```bash
python app.py
```

### 第 4 步：访问页面（1 分钟）

打开浏览器访问：
- **用户管理页面**：http://localhost:5000/portal/chamber/users
- **工商联门户**：http://localhost:5000/portal/chamber

### 第 5 步：登录测试（1 分钟）

使用以下任一账号登录（密码都是 `123456`）：

| 用户名 | 密码 | 权限 |
|--------|------|------|
| admin_national | 123456 | 全联管理员（可看所有用户） |
| admin_beijing | 123456 | 北京省级管理员（只看北京用户） |
| admin_chaoyang | 123456 | 朝阳区管理员（只看朝阳用户） |

## 📋 主要功能

### ✅ 已实现的功能

1. **用户列表**
   - 分页显示
   - 搜索功能（用户名/邮箱/姓名）
   - 多条件筛选（层级/角色/状态）

2. **用户管理**
   - 新增用户
   - 编辑用户信息
   - 删除用户
   - 批量导出 Excel

3. **权限控制**
   - 全联管理员：可管理所有用户
   - 省级管理员：只能管理本省用户
   - 县市级管理员：只能管理本县市用户

4. **操作日志**
   - 记录所有用户操作
   - 查看操作历史

## 🔌 API 快速参考

### 获取用户列表

```bash
curl http://localhost:5000/api/portal/chamber/users?page=1&page_size=10
```

### 创建用户

```bash
curl -X POST http://localhost:5000/api/portal/chamber/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "new_user",
    "email": "new@example.com",
    "password": "123456",
    "real_name": "新用户",
    "level": "county",
    "region": "北京朝阳",
    "role": "operator"
  }'
```

### 更新用户

```bash
curl -X PUT http://localhost:5000/api/portal/chamber/users/user-005 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "phone": "010-87654321"
  }'
```

### 删除用户

```bash
curl -X DELETE http://localhost:5000/api/portal/chamber/users/user-005
```

### 导出用户

```bash
curl http://localhost:5000/api/portal/chamber/users/export > users.xlsx
```

## 🧪 运行测试

```bash
python test_chamber_users.py
```

**测试内容：**
- ✅ 用户登录
- ✅ 获取用户列表
- ✅ 单个用户查询
- ✅ 按条件筛选
- ✅ 创建用户
- ✅ 更新用户
- ✅ 删除用户
- ✅ 获取操作日志
- ✅ 权限检查

## 📊 数据库表结构

### chamber_users（用户表）

```sql
CREATE TABLE chamber_users (
  id VARCHAR(36) PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  real_name VARCHAR(50),
  phone VARCHAR(20),
  level ENUM('county', 'province', 'national'),
  region VARCHAR(100),
  role ENUM('admin', 'reviewer', 'operator'),
  review_level ENUM('beginner', 'intermediate', 'advanced'),
  department VARCHAR(100),
  position VARCHAR(100),
  status ENUM('active', 'inactive', 'pending'),
  remark TEXT,
  created_by VARCHAR(36),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### chamber_user_logs（操作日志表）

```sql
CREATE TABLE chamber_user_logs (
  id VARCHAR(36) PRIMARY KEY,
  operator_id VARCHAR(36),
  target_user_id VARCHAR(36),
  action VARCHAR(50),
  old_value JSON,
  new_value JSON,
  created_at TIMESTAMP
);
```

## 🎯 常见操作

### 1. 查看所有用户

```bash
# 全联管理员登录后
curl http://localhost:5000/api/portal/chamber/users
```

### 2. 搜索特定用户

```bash
curl "http://localhost:5000/api/portal/chamber/users?keyword=admin"
```

### 3. 按层级筛选

```bash
# 查看所有县市级用户
curl "http://localhost:5000/api/portal/chamber/users?level=county"
```

### 4. 按角色筛选

```bash
# 查看所有操作员
curl "http://localhost:5000/api/portal/chamber/users?role=operator"
```

### 5. 按状态筛选

```bash
# 查看所有激活的用户
curl "http://localhost:5000/api/portal/chamber/users?status=active"
```

## 🔐 权限说明

### 全联管理员（national）
- 可以查看所有用户
- 可以创建任何级别的用户
- 可以编辑和删除任何用户

### 省级管理员（province）
- 只能查看本省用户
- 只能创建本省的县市级和省级用户
- 只能编辑本省的非管理员用户
- 只能删除本省的操作员

### 县市级管理员（county）
- 只能查看本县市用户
- 只能创建本县市的县市级用户
- 只能编辑本县市的操作员
- 只能删除本县市的操作员

## 📝 测试数据

系统预置了 11 个测试用户，分布在不同的层级和地区：

```
全联级别（1个）
├─ admin_national（全联管理员）

北京省级（2个）
├─ admin_beijing（省级管理员）
└─ reviewer_beijing（省级审核员）

北京朝阳县市（2个）
├─ admin_chaoyang（县市管理员）
├─ operator_chaoyang_1（操作员）
└─ operator_chaoyang_2（操作员，待审核）

北京海淀县市（2个）
├─ admin_haidian（县市管理员）
└─ operator_haidian（操作员）

上海省级（1个）
└─ admin_shanghai（省级管理员）

上海浦东县市（2个）
├─ admin_pudong（县市管理员）
└─ operator_pudong（操作员，已禁用）
```

所有用户密码都是 `123456`

## 🐛 故障排除

### 问题 1：数据库连接失败

**解决方案：**
```bash
# 检查 MySQL 是否运行
mysql -h localhost -u root -p -e "SELECT 1"

# 检查数据库是否存在
mysql -h localhost -u root -p -e "SHOW DATABASES"

# 检查表是否创建
mysql -h localhost -u root -p enterprise_portal -e "SHOW TABLES"
```

### 问题 2：权限不足错误

**解决方案：**
- 确保已登录
- 检查用户权限是否足够
- 查看操作日志了解权限限制

### 问题 3：用户名或邮箱已存在

**解决方案：**
- 使用不同的用户名和邮箱
- 检查是否已有相同用户

### 问题 4：页面加载缓慢

**解决方案：**
- 检查数据库连接
- 减少分页大小
- 检查网络连接

## 📚 相关文件

- `chamber_users_management.py` - 后端 API 实现
- `templates/chamber_users_management.html` - 前端页面
- `db/015_chamber_users.sql` - 表结构定义
- `db/101_chamber_users_seed.sql` - 测试数据
- `test_chamber_users.py` - 功能测试脚本
- `CHAMBER_USERS_IMPLEMENTATION.md` - 完整实现指南

## 🎓 学习资源

### 后端开发
- Flask 文档：https://flask.palletsprojects.com/
- SQLAlchemy 文档：https://docs.sqlalchemy.org/
- bcrypt 文档：https://github.com/pyca/bcrypt

### 前端开发
- HTML/CSS/JavaScript 基础
- 异步请求（Fetch API）
- 表单验证

### 数据库
- MySQL 基础语法
- 索引优化
- 权限管理

## 💡 最佳实践

1. **安全性**
   - 始终验证用户权限
   - 使用 bcrypt 加密密码
   - 记录所有操作日志

2. **性能**
   - 使用分页加载大量数据
   - 添加适当的数据库索引
   - 缓存常用查询结果

3. **可维护性**
   - 编写清晰的代码注释
   - 遵循命名规范
   - 定期备份数据库

## 🚀 下一步

1. ✅ 快速启动
2. ⏳ 自定义配置
3. ⏳ 集成到主应用
4. ⏳ 生产环境部署
5. ⏳ 性能优化

## 📞 获取帮助

- 查看完整文档：`CHAMBER_USERS_IMPLEMENTATION.md`
- 运行测试脚本：`python test_chamber_users.py`
- 查看 API 日志：检查控制台输出

---

**版本**：1.0  
**最后更新**：2025-01-01

