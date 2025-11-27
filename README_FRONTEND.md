# 企业现代制度评价系统 - 前端管理界面

## 系统概述

这是一个完整的企业现代制度评价系统，包含客户端和管理员两个不同的操作界面。系统支持在线问卷填写、Excel批量上传、自动生成报告、邮件通知等功能。

## 功能特性

### 客户端功能
1. **在线问卷填写** - 企业可直接在线填写231题评价问卷
2. **Excel批量上传** - 批量上传企业数据Excel文件
3. **自动生成报告** - 自动生成Word和PDF格式的评价报告
4. **邮件通知** - 报告生成后自动发送邮件通知

### 管理员功能
1. **系统概览** - 查看提交统计、报告数量等关键指标
2. **问卷提交管理** - 查看、搜索所有企业提交的问卷
3. **报告管理** - 查看、下载、删除已生成的报告
4. **批量生成报告** - 批量选择提交并生成报告
5. **邮件设置** - 配置SMTP邮件服务器
6. **系统设置** - 修改管理员密码等系统配置

## 系统架构

```
enterprise_report_system/
├── templates/                      # 前端页面
│   ├── index.html                 # 客户端首页
│   ├── questionnaire.html         # 在线问卷填写页面
│   ├── success.html               # 提交成功页面
│   ├── admin_login.html          # 管理员登录页面
│   └── admin_dashboard.html      # 管理员仪表板
├── app.py                         # Flask主应用
├── main.py                        # 终端主控制脚本
├─��� manage_submissions.py          # 终端问卷管理工具
├── enterprise_report_generator.py # Word报告生成器
├── pdf_report_generator.py        # PDF报告生成器
├── score_calculator.py            # 评分计算器
├── notification_service.py        # 邮件/短信通知服务
└── questionnaire_submission_manager.py  # 问卷提交管理器
```

## 快速开始

### 1. 安装依赖

```bash
pip install flask pandas openpyxl python-docx matplotlib reportlab
```

### 2. 启动系统

```bash
python app.py
```

### 3. 访问系统

启动后，您可以访问以下页面：

- **客户端首页**: http://localhost:5000
- **在线问卷填写**: http://localhost:5000/questionnaire
- **管理员登录**: http://localhost:5000/admin/login

### 4. 管理员登录

默认管理员账户：
- **用户名**: `admin`
- **密码**: `admin123`

**⚠️ 安全提示**: 首次使用后请立即修改默认密码！

## 使用指南

### 客户端使用

#### 方式一：在线填写问卷

1. 访问首页，点击"在线填写问卷"卡片
2. 填写企业基本信息
3. 逐题回答231道评价问题
4. 提交问卷
5. 系统自动生成报告并发送到邮箱

#### 方式二：批量上传Excel

1. 准备包含企业信息的Excel文件
   - 必需列：企业名称、联系人、联系人邮箱、联系人手机
2. 在首页点击"批量上传Excel"区域
3. 选择或拖拽Excel文件
4. 预览数据并配置选项
5. 点击"开始处理"批量生成报告

### 管理员使用

#### 登录系统

1. 访问 http://localhost:5000/admin/login
2. 输入用户名和密码
3. 点击登录进入管理后台

#### 查看系统概览

登录后默认显示系统概览页面，包括：
- 总提交数
- 已生成报告数
- 今日提交数
- 邮件发送数
- 最近提交列表

#### 管理问卷提交

1. 点击左侧菜单"问卷提交管理"
2. 查看所有企业提交的问卷
3. 使用搜索框筛选特定企业
4. 对每个提交可以：
   - 查看详情
   - 生成报告
   - 发送邮件

#### 批量生成报告

1. 点击左侧菜单"批量生成报告"
2. 勾选需要生成报告的提交
3. 配置报告选项：
   - 生成Word报告
   - 生成PDF报告
   - 自动发送邮件
4. 点击"开始批量生成"
5. 实时查看处理进度

#### 报告管理

1. 点击左侧菜单"报告管理"
2. 查看所有已生成的报告
3. 可以下载或删除报告文件

#### 配置邮件服务

1. 点击左侧菜单"邮件设置"
2. 填写SMTP服务器信息：
   - SMTP服务器地址
   - 端口号
   - 发件人邮箱
   - 邮箱密码
3. 保存设置
4. 发送测试邮件验证配置

## API接口文档

### 客户端API

#### 获取问卷题目
```
GET /api/get_questions
返回: { success: true, questions: [...] }
```

#### 提交问卷
```
POST /api/submit_questionnaire
请求体: { enterprise_info: {...}, answers: {...} }
返回: { success: true, message: "问卷提交成功" }
```

### 管理员API

所有管理员API需要先登录认证。

#### 登录
```
POST /api/admin/login
请求体: { username: "admin", password: "admin123" }
返回: { success: true, token: "..." }
```

#### 获取仪表板统计
```
GET /api/admin/dashboard-stats
返回: { success: true, stats: {...} }
```

#### 获取所有提交
```
GET /api/admin/submissions
返回: { success: true, submissions: [...] }
```

#### 生成报告
```
POST /api/admin/generate-report
请求体: { filename: "submission_xxx.json" }
返回: { success: true, word_report: "...", pdf_report: "..." }
```

#### 批量生成报告
```
POST /api/admin/batch-generate
请求体: {
  filenames: [...],
  generate_word: true,
  generate_pdf: true,
  send_email: true
}
返回: { success: true, task_id: "..." }
```

#### 获取批量任务状态
```
GET /api/admin/batch-status/<task_id>
返回: { success: true, data: { status: "processing", ... } }
```

## 页面设计说明

### 客户端页面设计

#### 首页 (index.html)
- **设计风格**: 现代渐变色背景，卡片式布局
- **主要元素**:
  - 顶部标题栏（右上角有管理员登录入口）
  - 两个功能卡片：在线填写问卷、批量上传Excel
  - 使用建议说明
  - Excel上传拖拽区域
  - 数据预览表格
  - 处理进度显示

#### 在线问卷页面 (questionnaire.html)
- **设计风格**: 清爽的蓝色主题，专业商务风格
- **主要元素**:
  - 进度条显示答题进度
  - 企��基本信息表单
  - 按一级指标分组的问题列表
  - 单选按钮答题界面
  - 保存草稿功能
  - 提交按钮

### 管理员页面设计

#### 登录页面 (admin_login.html)
- **设计风格**: 紫色渐变背景，居中卡片式登录框
- **主要元素**:
  - 锁图标
  - 用户名/密码输入框
  - 密码显示/隐藏切换
  - 登录按钮
  - 返回客户端首页链接

#### 管理员仪表板 (admin_dashboard.html)
- **设计风格**: 现代后台管理系统设计
- **布局**:
  - 左侧导航栏（深蓝色背景）
  - 顶部栏（显示时间和管理员信息）
  - 主内容区（白色背景，卡片式布局）

- **左侧导航菜单**:
  - 📊 概览
  - 📝 问卷提交管理
  - 📄 报告管理
  - ⚡ 批量生成报告
  - ✉️ 邮件设置
  - ⚙️ 系统设置
  - 🚪 退出登录

- **概览页面**:
  - 4个统计卡片���悬浮动画效果）
  - 最近提交表格

- **问卷提交管理**:
  - 搜索框
  - 数据表格
  - 操作按钮（查看、生成报告、发送邮件）

- **批量生成报告**:
  - 复选框列表选择提交
  - 报告设置选项
  - 进度条实时显示

## 技术栈

### 前端
- HTML5 + CSS3
- 原生JavaScript (无框架依赖)
- 响应式设计
- 渐变色UI设计
- 拖拽上传功能

### 后端
- Python 3.7+
- Flask Web框架
- Session认证
- 异步任务处理
- RESTful API设计

### 数据处理
- pandas - Excel数据处理
- openpyxl - Excel文件读写
- python-docx - Word文档生成
- reportlab - PDF文档生成
- matplotlib - 数据可视化（雷达图）

## 安全建议

1. **修改默认密码**: 首次部署后立即修改管理员默认密码
2. **使用HTTPS**: 生产环境建议使用HTTPS加密传输
3. **配置SECRET_KEY**: 修改app.py中的SECRET_KEY为随机字符串
4. **数据库存储**: 生产环境建议将用户信息存储到数据库
5. **JWT认证**: 建议使用JWT token替代session认证
6. **输入验证**: 对所有用户输入进行严格验证
7. **文件上传限制**: 已设置16MB上传限制，可根据需要调整

## 常见问题

### Q1: 如何修改管理员密码？
A: 有两种方式：
1. 登录后在"系统设置"页面修改
2. 直接修改app.py中的ADMIN_USERS字典

### Q2: 如何添加新的管理员账户？
A: 在app.py的ADMIN_USERS字典中添加新条目：
```python
ADMIN_USERS = {
    'admin': hashlib.sha256('admin123'.encode()).hexdigest(),
    'newadmin': hashlib.sha256('newpassword'.encode()).hexdigest()
}
```

### Q3: 邮件发送失败怎么办？
A: 请检查：
1. SMTP服务器配置是否正确
2. 邮箱密码是否是授权码（而非登录密码）
3. 防火墙是否允许SMTP端口
4. 在"邮件设置"中发送测试邮件验证

### Q4: 如何自定义问卷题目？
A: 修改`指标体系.xlsx`文件中的题目内容

### Q5: 生成的报告保存在哪里？
A:
- Word/PDF报告: `reports/` 文件夹
- 问卷Excel文件: `submissions/` 文件夹

## 终端工具

除了Web界面，系统还提供了终端命令行工具：

### main.py - 主控制脚本
```bash
python main.py
```
功能：
- 生成单个问卷
- 批量生成问卷
- 生成企业自评报告（Word）
- 生成企业自评报告（PDF）
- 生成整体分析报告

### manage_submissions.py - 问卷管理工具
```bash
python manage_submissions.py
```
功能：
- 查看所有在���提交
- 为指定企业生成Word/PDF报告
- 批量生成报告并发送邮件
- 查看特定提交的详细信息

## 开发路线图

- [x] 客户端在线问卷填写
- [x] Excel批量上传处理
- [x] 自动生成Word报告
- [x] 自动生成PDF报告
- [x] 邮件通知功能
- [x] 管理员登录认证
- [x] 管理员仪表板
- [x] 批量报告生成
- [ ] 数据可视化图表
- [ ] 导出统计报表
- [ ] 短信通知功能
- [ ] 数据库持久化
- [ ] 用户权限管理
- [ ] 报告模板自定义

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**祝您使用愉快！** 🎉
