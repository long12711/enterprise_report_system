# 工商联用户管理系统 - 完整实现指南

## 📋 项目概述

本项目为图片中的"工商联用户管理"界面提供完整的后端和前端实现，包括：

- **数据库表设计**：chamber_users（用户表）、chamber_user_logs（操作日志表）
- **后端 API**：完整的 CRUD 操作、权限检查、日志记录
- **前端界面**：用户列表、搜索筛选、新增编辑删除、导出 Excel
- **权限管理**：基于层级（全联/省级/县市）和角色（管理员/审核员/操作员）的权限控制

## 🗂️ 文件清单

### 数据库文件
- `db/015_chamber_users.sql` - 创建 chamber_users 和 chamber_user_logs 表
- `db/101_chamber_users_seed.sql` - 插入测试数据
- `db/all.sql` - 一键执行所有 SQL 脚本

### 后端代码
- `chamber_users_management.py` - 完整的 API 实现
- `app.py` - 已注册蓝图和路由

### 前端代码
- `templates/chamber_users_management.html` - 用户管理页面

### 工具脚本
- `init_chamber_users_db.py` - 数据库初始化脚本

## 🚀 快速开始

### 1. 创建数据库表

#### 方式一：使用 MySQL 客户端（推荐）

```bash
# 进入 MySQL 客户端
mysql -h localhost -u root -p

# 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS enterprise_portal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE enterprise_portal;

# 执行所有 SQL 脚本
SOURCE db/all.sql;
```

#### 方式二：使用 Python 脚本

```bash
# 设置环境变量（可选，默认值为 localhost:3306, root, enterprise_portal）
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=your_password
export DB_NAME=enterprise_portal

# 运行初始化脚本
python init_chamber_users_db.py
```

### 2. 启动应用

```bash
# 安装依赖
pip install flask flask-sqlalchemy pymysql bcrypt openpyxl

# 启动应用
python app.py
```

### 3. 访问页面

打开浏览器访问：
- **用户管理页面**：http://localhost:5000/portal/chamber/users
- **工商联门户**：http://localhost:5000/portal/chamber

## 📊 数据库设计

### chamber_users 表（用户表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 用户 ID（主键） |
| username | VARCHAR(50) | 用户名（唯一） |
| email | VARCHAR(100) | 邮箱（唯一） |
| password | VARCHAR(255) | 密码（bcrypt 加密） |
| real_name | VARCHAR(50) | 真实姓名 |
| phone | VARCHAR(20) | 手机号 |
| level | ENUM | 层级：county/province/national |
| region | VARCHAR(100) | 地区 |
| role | ENUM | 角色：admin/reviewer/operator |
| review_level | ENUM | 审核权限等级：beginner/intermediate/advanced |
| department | VARCHAR(100) | 部门 |
| position | VARCHAR(100) | 职位 |
| status | ENUM | 状态：active/inactive/pending |
| remark | TEXT | 备注 |
| created_by | VARCHAR(36) | 创建人 ID |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### chamber_user_logs 表（操作日志表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 日志 ID（主键） |
| operator_id | VARCHAR(36) | 操作人 ID |
| target_user_id | VARCHAR(36) | 目标用户 ID |
| action | VARCHAR(50) | 操作类型：create/update/delete/status_change |
| old_value | JSON | 旧值 |
| new_value | JSON | 新值 |
| created_at | TIMESTAMP | 创建时间 |

## 🔑 权限控制规则

### 查看用户
- **全联管理员**：可以看所有用户
- **省级管理员**：可以看本省的用户（县市和省级）
- **县市级管理员**：只能看本县市的用户

### 编辑用户
- **全联管理员**：可以编辑所有用户
- **省级管理员**：可以编辑本省的非管理员用户
- **县市级管理员**：只能编辑本县市的操作员

### 删除用户
- **全联管理员**：可以删除所有用户
- **省级管理员**：可以删除本省的操作员
- **县市级管理员**：只能删除本县市的操作员

### 创建用户
- 不能创建高于自己权限的用户
- 地区权限受限于自己的地区

## 🔌 API 接口

### 获取用户列表

```http
GET /api/portal/chamber/users?page=1&page_size=10&keyword=&level=&role=&status=
```

**参数：**
- `page` - 页码（默认 1）
- `page_size` - 每页数量（默认 10）
- `keyword` - 搜索关键词（用户名/邮箱/姓名）
- `level` - 层级过滤（county/province/national）
- `role` - 角色过滤（admin/reviewer/operator）
- `status` - 状态过滤（active/inactive/pending）

**响应：**
```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "users": [
      {
        "id": "user-001",
        "username": "admin_national",
        "email": "admin@chamber.org",
        "real_name": "全联管理员",
        "phone": "010-12345678",
        "level": "national",
        "region": "全国",
        "role": "admin",
        "review_level": "advanced",
        "department": "办公室",
        "position": "主任",
        "status": "active",
        "created_at": "2025-01-01T10:00:00"
      }
    ],
    "total": 11,
    "page": 1,
    "page_size": 10,
    "total_pages": 2
  }
}
```

### 获取单个用户

```http
GET /api/portal/chamber/users/{user_id}
```

### 创建用户

```http
POST /api/portal/chamber/users
Content-Type: application/json

{
  "username": "new_user",
  "email": "new@example.com",
  "password": "123456",
  "real_name": "新用户",
  "phone": "010-12345678",
  "level": "county",
  "region": "北京朝阳",
  "role": "operator",
  "review_level": "beginner",
  "department": "部门",
  "position": "职位",
  "status": "pending",
  "remark": "备注"
}
```

### 更新用户

```http
PUT /api/portal/chamber/users/{user_id}
Content-Type: application/json

{
  "real_name": "更新后的名字",
  "phone": "010-87654321",
  "status": "active",
  "role": "reviewer"
}
```

### 删除用户

```http
DELETE /api/portal/chamber/users/{user_id}
```

### 导出用户

```http
GET /api/portal/chamber/users/export
```

返回 Excel 文件下载

### 获取操作日志

```http
GET /api/portal/chamber/logs?page=1&page_size=10
```

## 🧪 测试数据

系统已预置 11 个测试用户，密码均为 `123456`：

| 用户名 | 真实姓名 | 层级 | 地区 | 角色 | 状态 |
|--------|---------|------|------|------|------|
| admin_national | 全联管理员 | 全联 | 全国 | 管理员 | 激活 |
| admin_beijing | 北京省级管理员 | 省级 | 北京 | 管理员 | 激活 |
| reviewer_beijing | 北京审核员 | 省级 | 北京 | 审核员 | 激活 |
| admin_chaoyang | 朝阳区管理员 | 县市 | 北京朝阳 | 管理员 | 激活 |
| operator_chaoyang_1 | 朝阳操作员1 | 县市 | 北京朝阳 | 操作员 | 激活 |
| operator_chaoyang_2 | 朝阳操作员2 | 县市 | 北京朝阳 | 操作员 | 待审核 |
| admin_haidian | 海淀区管理员 | 县市 | 北京海淀 | 管理员 | 激活 |
| operator_haidian | 海淀操作员 | 县市 | 北京海淀 | 操作员 | 激活 |
| admin_shanghai | 上海省级管理员 | 省级 | 上海 | 管理员 | 激活 |
| admin_pudong | 浦东新区管理员 | 县市 | 上海浦东 | 管理员 | 激活 |
| operator_pudong | 浦东操作员 | 县市 | 上海浦东 | 操作员 | 禁用 |

## 🎨 前端功能

### 用户列表页面

**功能：**
- ✅ 用户列表展示（分页）
- ✅ 搜索用户（用户名/邮箱/姓名）
- ✅ 按层级/角色/状态筛选
- ✅ 新增用户
- ✅ 编辑用户
- ✅ 删除用户
- ✅ 导出 Excel
- ✅ 状态徽章显示
- ✅ 操作日志查看

### 用户表单

**字段：**
- 用户名（必填）
- 邮箱（必填）
- 密码（新增必填，编辑可选）
- 真实姓名（必填）
- 手机号
- 层级（必填）
- 地区（必填）
- 角色（必填）
- 审核权限等级
- 部门
- 职位
- 状态
- 备注

## 🔐 安全性

### 密码加密
- 使用 bcrypt 算法加密密码
- 密码强度要求：至少 6 位

### 权限检查
- 所有 API 都进行权限检查
- 用户只能看到自己权限范围内的数据
- 操作日志记录所有修改

### 数据验证
- 用户名和邮箱唯一性检查
- 必填字段验证
- 权限层级验证

## 📝 使用示例

### 登录

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_national",
    "password": "123456",
    "role": "chamber_of_commerce"
  }'
```

### 获取用户列表

```bash
curl http://localhost:5000/api/portal/chamber/users?page=1&page_size=10
```

### 创建新用户

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

### 编辑用户

```bash
curl -X PUT http://localhost:5000/api/portal/chamber/users/user-005 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "active",
    "role": "reviewer"
  }'
```

### 删除用户

```bash
curl -X DELETE http://localhost:5000/api/portal/chamber/users/user-005
```

## 🐛 常见问题

### Q: 如何修改密码？
A: 当前系统不支持用户自助修改密码，只能由管理员重新创建用户或编辑用户信息。

### Q: 如何重置用户密码？
A: 需要在数据库中直接更新密码字段，使用 bcrypt 加密。

### Q: 如何导出用户列表？
A: 点击"导出 Excel"按钮，系统会根据当前权限范围导出用户列表。

### Q: 权限不足时会发生什么？
A: 系统会返回 403 错误，提示"权限不足"。

### Q: 如何查看操作日志？
A: 点击"操作日志"标签页，查看所有用户操作记录。

## 📚 相关文档

- [工商联用户管理_后端API实现指南.md](./工商联用户管理_后端API实现指南.md)
- [工商联用户管理_实现清单.md](./工商联用户管理_实现清单.md)
- [工商联用户管理_快速参考.md](./工商联用户管理_快速参考.md)

## 🎯 下一步

1. ✅ 数据库表创建
2. ✅ 后端 API 实现
3. ✅ 前端页面实现
4. ✅ 测试数据填充
5. ⏳ 集成到主应用
6. ⏳ 生产环境部署

## 📞 支持

如有问题或建议，请联系开发团队。

---

**版本**：1.0  
**最后更新**：2025-01-01  
**作者**：AI Assistant

