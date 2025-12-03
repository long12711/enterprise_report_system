# 专家管理功能完成指南

## 项目恢复完成情况

本次恢复完成了以下功能，使项目可以正常使用：

### 1. ✓ 恢复并重写 app.py
- **文件**: `app.py`
- **功能**: 完整的 Flask 主应用，集成所有 API 和路由
- **包含内容**:
  - 认证系统 (登录/登出)
  - 企业管理 API (CRUD)
  - 专家管理 API (CRUD)
  - 资质审核 API
  - 专项审核 API
  - 报告管理 API
  - 工商联用户管理 API
  - 问卷管理 API

### 2. ✓ 更新 portal_chamber.html
- **文件**: `templates/portal_chamber.html`
- **新增功能**:
  - 专家信息管理 Tab (CRUD 操作)
  - 专家自评详情 Tab (查看历史评分)
  - 专家评级管理 Tab (升级/降级)
  - 专家辅导详情 Tab (查看辅导记录)
  - 企业对专家评价 Tab (查看和添加评价)

### 3. ✓ 初始化存储文件
创建了以下 JSON 数据文件:
- `storage/experts.json` - 专家信息库 (包含 3 个示例专家)
- `storage/expert_evaluations.json` - 企业对专家的评价 (包含 3 条示例评价)
- `storage/enterprises.json` - 企业信息库 (包含 3 个示例企业)
- `storage/users.json` - 用户账户 (包含 3 个示例用户)
- `storage/special_submissions.json` - 专项申请 (包含 3 条示例申请)

## API 端点列表

### 认证相关
- `POST /login` - 用户登录
- `POST /logout` - 用户登出

### 企业管理
- `GET /api/portal/chamber/enterprises` - 获取企业列表
- `POST /api/portal/chamber/enterprises/save` - 保存企业信息
- `DELETE /api/portal/chamber/enterprises/<id>` - 删除企业

### 专家管理 (新增)
- `GET /api/portal/chamber/experts` - 获取专家列表
- `POST /api/portal/chamber/experts` - 保存专家信息
- `DELETE /api/portal/chamber/experts/<id>` - 删除专家
- `GET /api/portal/chamber/expert-self` - 获取专家自评详情
- `GET /api/portal/chamber/expert-rate` - 获取专家评级信息
- `POST /api/portal/chamber/expert-rate` - 设置专家评级
- `GET /api/portal/chamber/expert-tutoring` - 获取专家辅导详情
- `GET /api/portal/chamber/expert-evaluations` - 获取企业对专家的评价
- `POST /api/portal/chamber/expert-evaluations` - 添加企业评价

### 资质审核
- `GET /api/portal/chamber/reviews` - 获取资质审核列表
- `POST /api/portal/chamber/approve-upgrade` - 批准升级
- `POST /api/portal/chamber/upgrade` - 企业升级

### 专项审核
- `GET /api/special/list` - 获取专项申请列表
- `POST /api/special/review` - 专项审核
- `GET /api/special/download/<id>/<filename>` - 下载专项附件

### 报告管理
- `GET /api/portal/chamber/all-reports` - 获取所有报告
- `POST /api/portal/chamber/send-report` - 发送报告

### 其他
- `GET /api/portal/chamber/users` - 工商联用户列表
- `GET /api/portal/chamber/questionnaires` - 问卷列表
- `GET /api/portal/chamber/tutoring-records` - 辅导记录

## 前端功能说明

### 专家管理 Tab
**功能**: CRUD 专家信息
- 搜索专家
- 新增专家
- 编辑专家
- 删除专家
- 字段: 姓名、地区、省份、行业、等级、电话、邮箱、单位、擅长领域

### 专家自评详情 Tab
**功能**: 查看专家的自评历史
- 选择专家
- 查看历史评分
- 显示: 时间、分数、级别、问卷文件

### 专家评级管理 Tab
**功能**: 管理专家的评级
- 选择专家
- 查看当前等级和可辅导范围
- 升级/降级专家等级
- 等级: 县市级、省市级、国家级

### 专家辅导详情 Tab
**功能**: 查看专家的辅导记录
- 选择专家
- 查看辅导企业和内容
- 显示: 时间、企业、辅导内容

### 企业对专家评价 Tab
**功能**: 查看和添加企业对专家的评价
- 选择专家
- 查看现有评价
- 新增评价
- 显示: 时间、企业、评分、评价内容

## 数据结构

### 专家信息 (experts.json)
```json
{
  "id": "exp001",
  "name": "张三",
  "region": "天津市",
  "province": "天津",
  "industry": "制造业",
  "level": "county",  // county|province|national
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "org": "天津工业协会",
  "skills": "企业管理、质量控制",
  "created_at": "2024-01-01 10:00",
  "updated_at": "2024-01-01 10:00"
}
```

### 企业评价 (expert_evaluations.json)
```json
{
  "id": "eval001",
  "expert": "张三",
  "enterprise": "示例企业A",
  "score": 85,
  "comment": "专家指导非常专业",
  "time": "2024-01-15 14:30"
}
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
python start_server.py
```
或
```bash
python app.py
```

### 3. 访问应用
- 打开浏览器访问: http://localhost:5000/
- 点击"工商联门户"或直接访问: http://localhost:5000/portal/chamber
- 登录信息:
  - 用户名: admin
  - 密码: admin
  - 角色: chamber_of_commerce

### 4. 测试功能
1. 进入"专家管理"菜单
2. 点击"专家信息"查看专家列表
3. 尝试新增、编辑、删除专家
4. 进入其他 Tab 测试相应功能

## 文件结构

```
project/
├── app.py                          # Flask 主应用
├── start_server.py                 # 服务器启动脚本
├── templates/
│   └── portal_chamber.html         # 工商联门户页面
├── storage/
│   ├── experts.json                # 专家数据
│   ├── expert_evaluations.json     # 评价数据
│   ├── enterprises.json            # 企业数据
│   ├── users.json                  # 用户数据
│   ├── special_submissions.json    # 专项申请数据
│   ├── reports/                    # 报告存储
│   ├── submissions/                # 问卷提交
│   ├── uploads/                    # 文件上传
│   ├── tutoring_logs/              # 辅导记录
│   └── special_submissions/        # 专项申请文件
└── ...
```

## 注意事项

1. **认证**: 当前使用简单的 session 认证，生产环境应使用数据库和加密密码
2. **数据持久化**: 使用 JSON 文件存储，生产环境应使用数据库
3. **文件上传**: 需要实现文件上传功能
4. **邮件发送**: 需要配置邮件服务
5. **错误处理**: 需要完善错误处理和日志记录

## 后续改进建议

1. 集成数据库 (MySQL/PostgreSQL)
2. 实现文件上传和管理
3. 添加邮件发送功能
4. 完善权限控制
5. 添加数据验证和错误处理
6. 实现数据导出功能
7. 添加数据统计和报表
8. 实现消息通知功能

## 测试用例

### 测试专家 CRUD
1. 新增专家: 填写所有字段，点击"保存"
2. 编辑专家: 点击"编辑"，修改信息，点击"保存"
3. 删除专家: 点击"删除"，确认删除
4. 搜索专家: 输入专家名称，点击"查询"

### 测试专家评级
1. 选择专家
2. 查看当前等级
3. 选择新等级
4. 点击"执行评级"

### 测试企业评价
1. 选择专家
2. 输入企业名称、评分、评价内容
3. 点击"提交"
4. 查看评价列表

## 支持和帮助

如有问题，请检查:
1. 存储文件是否存在
2. 浏览器控制台是否有错误
3. 服务器日志是否有错误信息
4. 网络连接是否正常

