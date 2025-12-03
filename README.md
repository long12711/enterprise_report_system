# 工商联用户管理系统

## 📋 项目概述

本项目是工商联门户系统的**用户管理模块**，提供对工商联用户的增删改查（CRUD）操作，实现基于层级和地区的权限控制。

### 核心功能
- ✅ **用户管理**: 新增、编辑、删除、查询用户
- ✅ **权限控制**: 基于层级和地区的细粒度权限管理
- ✅ **状态管理**: 用户激活、停用、待审核状态管理
- ✅ **数据导出**: 支持导出用户列表为Excel
- ✅ **操作日志**: 记录所有用户操作
- ✅ **搜索筛选**: 多条件组合搜索和筛选

---

## 🎯 用户分类与权限

### 用户层级
```
┌─────────────────────────────────────────┐
│         全联管理员 (national)            │
│    能看到所有层级的工商联管理员          │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      省级管理员 (province)               │
│  能看到本省所有县市的工商联管理员        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      县市级管理员 (county)               │
│  只能看到本县市的工商联管理员            │
└─────────────────────────────────────────┘
```

### 权限矩阵

#### 查看权限
| 当前用户 | 可查看 | 不可查看 |
|---------|--------|---------|
| 县市级 | 本县市用户 | 其他县市、省级、全联 |
| 省级 | 本省所有用户 | 其他省份、全联 |
| 全联 | 所有用户 | - |

#### 编辑权限
| 当前用户 | 可编辑 | 不可编辑 |
|---------|--------|---------|
| 县市级 | 本县市操作员 | 审核员、管理员、上级用户 |
| 省级 | 本省操作员、审核员 | 管理员、全联用户 |
| 全联 | 所有用户 | - |

#### 删除权限
| 当前用户 | 可删除 | 不可删除 |
|---------|--------|---------|
| 县市级 | 本县市操作员 | 审核员及以上、上级用户 |
| 省级 | 本省操作员 | 审核员及以上、全联用户 |
| 全联 | 所有用户 | - |

---

## 📁 项目文件结构

```
工商联用户管理/
├── README.md                                    # 项目说明文档
├── 工商联用户管理系统设计方案.md                # 完整系统设计
├── 工商联用户管理_后端API实现指南.md            # 后端实现指南
├── 工商联用户管理_实现清单.md                   # 项目任务清单
├── 工商联用户管理_快速参考.md                   # 快速参考指南
├── 数据库初始化脚本.sql                        # 数据库初始化SQL
├── chamber_users_api.py                        # Flask后端API实现
└── templates/
    └── portal_chamber.html                     # 前端HTML页面
```

---

## 🚀 快速开始

### 1. 数据库初始化

```bash
# 使用MySQL客户端执行初始化脚本
mysql -u root -p < 数据库初始化脚本.sql
```

### 2. 后端部署

```bash
# 安装依赖
pip install flask sqlalchemy bcrypt openpyxl

# 复制 chamber_users_api.py 到项目目录
cp chamber_users_api.py /path/to/your/project/

# 在Flask应用中注册蓝图
from chamber_users_api import register_chamber_users_api
register_chamber_users_api(app)
```

### 3. 前端集成

```bash
# 复制 portal_chamber.html 到模板目录
cp templates/portal_chamber.html /path/to/your/templates/
```

### 4. 启动应用

```bash
# 启动Flask应用
python app.py
```

---

## 📊 数据库设计

### chamber_users 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 用户ID |
| username | VARCHAR(50) | 用户名(唯一) |
| email | VARCHAR(100) | 邮箱(唯一) |
| password | VARCHAR(255) | 密码(bcrypt加密) |
| real_name | VARCHAR(50) | 真实姓名 |
| phone | VARCHAR(20) | 手机号 |
| level | ENUM | 层级(county/province/national) |
| region | VARCHAR(100) | 地区 |
| role | ENUM | 角色(admin/reviewer/operator) |
| review_level | ENUM | 审核权限等级 |
| department | VARCHAR(100) | 部门 |
| position | VARCHAR(100) | 职位 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |
| status | ENUM | 状态(active/inactive/pending) |
| remark | TEXT | 备注 |
| created_by | VARCHAR(36) | 创建人ID |

### chamber_user_logs 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | VARCHAR(36) | 日志ID |
| operator_id | VARCHAR(36) | 操作人ID |
| target_user_id | VARCHAR(36) | 目标用户ID |
| action | VARCHAR(50) | 操作类型(create/update/delete) |
| old_value | JSON | 旧值 |
| new_value | JSON | 新值 |
| created_at | TIMESTAMP | 创建时间 |

---

## 🔌 API 接口

### 获取用户列表
```bash
GET /api/portal/chamber/users?page=1&limit=20&level=county&region=北京市朝阳区
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "users": [
      {
        "id": "uuid",
        "username": "admin1",
        "email": "admin1@example.com",
        "real_name": "张三",
        "level": "county",
        "region": "北京市朝阳区",
        "role": "admin",
        "status": "active"
      }
    ]
  }
}
```

### 创建用户
```bash
POST /api/portal/chamber/users
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "Password123!",
  "real_name": "李四",
  "phone": "13800138000",
  "level": "county",
  "region": "北京市朝阳区",
  "role": "operator"
}
```

### 更新用户
```bash
PUT /api/portal/chamber/users/{user_id}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "real_name": "李四",
  "status": "active"
}
```

### 删除用户
```bash
DELETE /api/portal/chamber/users/{user_id}
```

### 导出用户
```bash
GET /api/portal/chamber/users/export?level=county&status=active
```

---

## 🎨 前端功能

### 用户列表页面
- 表格显示用户信息（用户名、邮箱、真实姓名、手机、层级、地区、角色等）
- 搜索框：按用户名、邮箱、真实姓名搜索
- 筛选条件：层级、地区、角色、状态
- 分页控制：上一页、下一页、页码显示
- 操作按钮：编辑、删除、启用/停用

### 新增/编辑模态框
- 基本信息：用户名、邮箱、密码、真实姓名、手机号
- 权限设置：层级、地区、角色、审核权限等级
- 部门信息：部门、职位
- 状态：激活/停用/待审核
- 备注

### 搜索和筛选
- 关键字搜索
- 多条件组合筛选
- 实时查询

---

## 🔐 安全特性

### 密码安全
- ✅ 使用bcrypt加密存储
- ✅ 密码最少8位
- ✅ 支持密码修改
- ✅ 定期修改提醒

### 权限安全
- ✅ 后端严格验证权限
- ✅ 不能跨越权限层级
- ✅ 操作日志记录
- ✅ 定期审计日志

### 数据安全
- ✅ 敏感信息加密
- ✅ 定期数据备份
- ✅ 支持数据导出
- ✅ 数据恢复机制

---

## 📚 文档说明

### 1. 工商联用户管理系统设计方案.md
完整的系统设计文档，包括：
- 需求分析
- 用户分类与权限
- 用户基本信息字段
- 数据库设计
- 权限控制规则
- API接口设计
- 前端界面设计
- 业务流程
- 安全考虑

### 2. 工商联用户管理_后端API实现指南.md
后端实现详解，包括：
- 数据库表设计
- 权限检查工具类
- 6个核心API实现
- 操作日志记录
- 模型定义
- 测试用例

### 3. 工商联用户管理_实现清单.md
项目任务清单，包括：
- 后端实现任务
- 前端实现任务
- 测试计划
- 部署清单
- 项目进度

### 4. 工商联用户管理_快速参考.md
快速参考指南，包括：
- 系统架构
- 核心功能速查表
- 数据字段说明
- 权限检查流程
- 前端关键代码片段
- 常见操作流程
- 常见错误处理
- 快速问题解答

---

## 🧪 测试

### 单元测试
```python
# 权限检查测试
def test_can_view_user():
    current_user = create_county_user()
    target_user = create_county_user(region='其他地区')
    assert not PermissionChecker.can_view_user(current_user, target_user)

# 密码验证测试
def test_validate_password():
    valid, msg = validate_password('short')
    assert not valid
    assert msg == '密码至少8位'
```

### 集成测试
```bash
# 运行测试
pytest tests/

# 生成覆盖率报告
pytest --cov=chamber_users_api tests/
```

---

## 🐛 常见问题

**Q: 如何重置用户密码？**
A: 编辑用户，在密码字段输入新密码，点击保存即可

**Q: 如何导出用户列表？**
A: 点击"导出"按钮，系统会生成Excel文件下载

**Q: 停用用户后还能恢复吗？**
A: 可以，编辑用户，将状态改为"激活"即可

**Q: 能否修改用户名？**
A: 不能，用户名是唯一标识，创建后不可修改

**Q: 如何查看操作日志？**
A: 在用户管理页面的"日志"标签页查看

---

## 📈 性能优化

### 数据库优化
- 使用复合索引：`idx_level_region`, `idx_status`
- 分页查询：每页20条
- 缓存常用查询结果

### 前端优化
- 虚拟滚动显示大列表
- 防抖搜索输入
- 缓存用户数据

### 后端优化
- 使用连接池
- 异步处理导出
- 批量操作优化

---

## 🚀 部署建议

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
mysql -u root -p < 数据库初始化脚本.sql

# 运行应用
python app.py
```

### 生产环境
```bash
# 使用Gunicorn部署
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 使用Nginx反向代理
# 配置SSL证书
# 启用HTTPS
```

---

## 📞 技术支持

如有问题或建议，请联系项目团队。

### 相关文档
- [系统设计方案](./工商联用户管理系统设计方案.md)
- [后端实现指南](./工商联用户管理_后端API实现指南.md)
- [实现清单](./工商联用户管理_实现清单.md)
- [快速参考](./工商联用户管理_快速参考.md)

---

## 📄 许可证

本项目采用 MIT 许可证。

---

## 🙏 致谢

感谢所有为本项目做出贡献的人员。

---

**版本**: 1.0.0  
**最后更新**: 2024-11-30  
**维护者**: 项目团队

