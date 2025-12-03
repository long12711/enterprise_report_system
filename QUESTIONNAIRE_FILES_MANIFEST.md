# 问卷系统文件清单

**生成日期**: 2025-12-02  
**项目版本**: 1.0  
**文件总数**: 11 个  

---

## 📦 文件清单

### 核心模块（3 个文件）

#### 1. docx_questionnaire_importer.py
- **类型**: Python 模块
- **大小**: ~350 行代码
- **功能**: Word 文档导入
- **主要类**: `DocxQuestionnaireImporter`
- **关键方法**:
  - `import_questionnaire()` - 导入单个问卷
  - `import_all_questionnaires()` - 批量导入
  - `get_survey()` - 获取问卷
  - `get_survey_questions()` - 获取问题
  - `get_survey_by_level()` - 按级别获取
  - `list_surveys()` - 列出所有问卷
  - `delete_survey()` - 删除问卷
- **依赖**: python-docx, json, uuid, datetime, logging
- **数据库**: JSON (storage/questionnaires.json)

#### 2. questionnaire_management_api.py
- **类型**: Flask 蓝图模块
- **大小**: ~500 行代码
- **功能**: 问卷管理 API
- **蓝图**: `questionnaire_bp`
- **API 端点数**: 12 个
- **主要功能**:
  - 问卷导入
  - 问卷查询
  - 问卷填写
  - 答案保存
  - 问卷提交
  - 文件上传
- **依赖**: Flask, mysql-connector-python, docx_questionnaire_importer
- **装饰器**: @login_required, @enterprise_required

#### 3. file_upload_handler.py
- **类型**: Python 模块
- **大小**: ~300 行代码
- **功能**: 文件上传处理
- **主要类**: `FileUploadHandler`
- **关键方法**:
  - `save_file()` - 保存文件
  - `delete_file()` - 删除文件
  - `get_file()` - 获取文件
  - `list_submission_files()` - 列出文件
  - `cleanup_old_files()` - 清理旧文件
  - `get_submission_storage_info()` - 获取存储信息
- **配置**:
  - 允许的文件类型: pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif, bmp, txt, csv, zip, rar, 7z
  - 最大文件大小: 100MB
  - 存储目录: storage/questionnaire_uploads/
- **依赖**: os, json, uuid, datetime, werkzeug, logging

### 前端文件（1 个文件）

#### 4. templates/questionnaire_form.html
- **类型**: HTML 模板
- **大小**: ~800 行代码
- **功能**: 企业问卷填写页面
- **主要功能**:
  - 问卷级别选择
  - 问题动态渲染
  - 多种题目类型支持
  - 进度条显示
  - 文件上传
  - 草稿保存
  - 问卷提交
- **样式**: CSS3 (内联)
- **脚本**: JavaScript (内联)
- **API 调用**:
  - GET /api/questionnaire/survey/level/<level>
  - POST /api/questionnaire/submission/create
  - POST /api/questionnaire/submission/<id>/save
  - POST /api/questionnaire/submission/<id>/submit
  - POST /api/questionnaire/submission/<id>/upload
- **响应式**: 是（支持移动设备）

### 数据库文件（1 个文件）

#### 5. db/095_questionnaire_submissions.sql
- **类型**: SQL 脚本
- **大小**: ~100 行代码
- **功能**: 数据库表定义
- **表数量**: 5 个主表
- **表列表**:
  1. `questionnaire_templates` - 问卷模板
  2. `questionnaire_template_questions` - 模板问题
  3. `questionnaire_submissions` - 提交记录
  4. `questionnaire_answers` - 答案明细
  5. `questionnaire_attachments` - 附件记录
- **索引数**: 8 个
- **字符集**: utf8mb4
- **存储引擎**: InnoDB

### 测试文件（1 个文件）

#### 6. test_questionnaire_import.py
- **类型**: Python 测试脚本
- **大小**: ~250 行代码
- **功能**: 系统功能测试
- **测试函数**:
  - `test_import()` - 导入测试
  - `test_api()` - API 测试
  - `test_data_structure()` - 数据结构测试
  - `show_sample_data()` - 显示样本数据
- **测试覆盖**:
  - Word 文档导入
  - 问卷查询
  - 数据验证
  - API 接口
  - 数据结构
- **运行方式**: `python test_questionnaire_import.py`

### 文档文件（4 个文件）

#### 7. QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md
- **类型**: Markdown 文档
- **大小**: ~5,000 字
- **内容**:
  - 项目概述
  - 系统架构
  - 核心模块说明
  - 数据库设计
  - 实现步骤
  - 工作流程
  - API 调用示例
  - 常见问题
  - 性能优化
  - 安全建议
  - 扩展功能
- **目标读者**: 开发人员、系统管理员

#### 8. INTEGRATION_CHECKLIST.md
- **类型**: Markdown 文档
- **大小**: ~3,000 字
- **内容**:
  - 集成步骤（10 个阶段）
  - 文件清单
  - 常见问题
  - 回滚计划
  - 验证清单
  - 版本信息
- **目标读者**: 集成工程师、项目经理

#### 9. QUESTIONNAIRE_SYSTEM_SUMMARY.md
- **类型**: Markdown 文档
- **大小**: ~4,000 字
- **内容**:
  - 项目概述
  - 核心功能
  - 项目文件结构
  - 技术架构
  - 数据流
  - 快速开始
  - 接口列表
  - 数据库设计
  - 实现步骤
  - 工作流程
  - 扩展功能
  - 已知问题
  - 更新日志
- **目标读者**: 所有人员

#### 10. QUESTIONNAIRE_QUICK_REFERENCE.md
- **类型**: Markdown 文档
- **大小**: ~2,000 字
- **内容**:
  - 5 分钟快速开始
  - 常用命令
  - API 快速参考
  - 文件位置
  - 调试技巧
  - 配置调整
  - 常见问题快速解决
  - 数据统计
  - 备份和恢复
  - 获取帮助
- **目标读者**: 快速参考用户

### 项目文件（1 个文件）

#### 11. app.py (修改)
- **类型**: Flask 主应用
- **修改内容**:
  - 添加问卷管理蓝图注册
  - 添加问卷表单页面路由
- **新增代码行数**: ~10 行
- **新增路由**:
  - GET `/questionnaire/form` - 问卷表单页面
- **新增蓝图**:
  - `questionnaire_bp` - 问卷管理蓝图

---

## 📊 文件统计

### 按类型统计

| 类型 | 数量 | 行数 |
|------|------|------|
| Python 模块 | 4 | ~1,400 |
| HTML 模板 | 1 | ~800 |
| SQL 脚本 | 1 | ~100 |
| 测试脚本 | 1 | ~250 |
| 文档 | 4 | ~14,000 |
| **总计** | **11** | **~16,550** |

### 按功能统计

| 功能 | 文件数 |
|------|--------|
| 导入功能 | 1 |
| API 功能 | 1 |
| 文件处理 | 1 |
| 前端页面 | 1 |
| 数据库 | 1 |
| 测试 | 1 |
| 文档 | 4 |
| 应用集成 | 1 |

---

## 🗂️ 目录结构

```
project_root/
├── docx_questionnaire_importer.py          # 核心模块 1
├── questionnaire_management_api.py         # 核心模块 2
├── file_upload_handler.py                  # 核心模块 3
├── test_questionnaire_import.py            # 测试脚本
├── app.py                                  # 应用集成
│
├── templates/
│   └── questionnaire_form.html             # 前端页面
│
├── db/
│   └── 095_questionnaire_submissions.sql   # 数据库脚本
│
├── storage/
│   ├── questionnaires.json                 # 问卷数据库（自动生成）
│   └── questionnaire_uploads/              # 上传文件目录（自动生成）
│
└── 文档/
    ├── QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md
    ├── INTEGRATION_CHECKLIST.md
    ├── QUESTIONNAIRE_SYSTEM_SUMMARY.md
    ├── QUESTIONNAIRE_QUICK_REFERENCE.md
    ├── QUESTIONNAIRE_COMPLETION_REPORT.md
    └── QUESTIONNAIRE_FILES_MANIFEST.md     # 本文件
```

---

## 📝 文件依赖关系

```
app.py
├── questionnaire_management_api.py
│   ├── docx_questionnaire_importer.py
│   │   ├── python-docx
│   │   ├── json
│   │   ├── uuid
│   │   ├── datetime
│   │   └── logging
│   ├── file_upload_handler.py
│   │   ├── os
│   │   ├── json
│   │   ├── uuid
│   │   ├── datetime
│   │   ├── werkzeug
│   │   └── logging
│   └── mysql-connector-python
│
└── templates/questionnaire_form.html
    ├── HTML5
    ├── CSS3
    ├── JavaScript (ES6+)
    └── API 调用
```

---

## 🔄 文件使用流程

### 导入问卷流程

```
Word 文档
    ↓
docx_questionnaire_importer.py
    ↓
storage/questionnaires.json
    ↓
db/095_questionnaire_submissions.sql (可选)
```

### 企业填写问卷流程

```
templates/questionnaire_form.html
    ↓
questionnaire_management_api.py
    ↓
docx_questionnaire_importer.py (查询)
    ↓
file_upload_handler.py (上传)
    ↓
storage/questionnaires.json (保存)
    ↓
storage/questionnaire_uploads/ (保存文件)
```

---

## ✅ 文件检查清单

- [ ] docx_questionnaire_importer.py - 已创建
- [ ] questionnaire_management_api.py - 已创建
- [ ] file_upload_handler.py - 已创建
- [ ] templates/questionnaire_form.html - 已创建
- [ ] db/095_questionnaire_submissions.sql - 已创建
- [ ] test_questionnaire_import.py - 已创建
- [ ] QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md - 已创建
- [ ] INTEGRATION_CHECKLIST.md - 已创建
- [ ] QUESTIONNAIRE_SYSTEM_SUMMARY.md - 已创建
- [ ] QUESTIONNAIRE_QUICK_REFERENCE.md - 已创建
- [ ] app.py - 已修改

---

## 🚀 部署文件清单

### 必须部署的文件

- ✅ docx_questionnaire_importer.py
- ✅ questionnaire_management_api.py
- ✅ file_upload_handler.py
- ✅ templates/questionnaire_form.html
- ✅ app.py (修改后)

### 可选部署的文件

- ✅ db/095_questionnaire_submissions.sql (如果使用 MySQL)
- ✅ test_questionnaire_import.py (测试用)

### 文档文件

- ✅ QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md
- ✅ INTEGRATION_CHECKLIST.md
- ✅ QUESTIONNAIRE_SYSTEM_SUMMARY.md
- ✅ QUESTIONNAIRE_QUICK_REFERENCE.md

---

## 📦 打包清单

### 开发包

包含所有文件用于开发和测试：

```
questionnaire-system-dev-1.0.zip
├── docx_questionnaire_importer.py
├── questionnaire_management_api.py
├── file_upload_handler.py
├── test_questionnaire_import.py
├── templates/questionnaire_form.html
├── db/095_questionnaire_submissions.sql
└── 文档/
    ├── QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md
    ├── INTEGRATION_CHECKLIST.md
    ├── QUESTIONNAIRE_SYSTEM_SUMMARY.md
    └── QUESTIONNAIRE_QUICK_REFERENCE.md
```

### 生产包

包含生产环境需要的文件：

```
questionnaire-system-prod-1.0.zip
├── docx_questionnaire_importer.py
├── questionnaire_management_api.py
├── file_upload_handler.py
├── templates/questionnaire_form.html
├── db/095_questionnaire_submissions.sql
└── 文档/
    ├── QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md
    └── QUESTIONNAIRE_QUICK_REFERENCE.md
```

---

## 🔐 文件权限

| 文件 | 权限 | 说明 |
|------|------|------|
| *.py | 644 | Python 源代码 |
| *.html | 644 | HTML 模板 |
| *.sql | 644 | SQL 脚本 |
| *.md | 644 | 文档文件 |
| storage/ | 755 | 存储目录（需要写权限） |

---

## 📋 版本控制

### 文件版本

| 文件 | 版本 | 日期 | 状态 |
|------|------|------|------|
| docx_questionnaire_importer.py | 1.0 | 2025-12-02 | ✅ 稳定 |
| questionnaire_management_api.py | 1.0 | 2025-12-02 | ✅ 稳定 |
| file_upload_handler.py | 1.0 | 2025-12-02 | ✅ 稳定 |
| questionnaire_form.html | 1.0 | 2025-12-02 | ✅ 稳定 |
| 095_questionnaire_submissions.sql | 1.0 | 2025-12-02 | ✅ 稳定 |
| test_questionnaire_import.py | 1.0 | 2025-12-02 | ✅ 稳定 |

---

## 📞 支持

### 文件相关问题

- 文件缺失: 检查 `QUESTIONNAIRE_FILES_MANIFEST.md`
- 文件损坏: 重新下载或恢复备份
- 文件权限: 检查文件权限设置

### 文档相关问题

- 查看实现指南: `QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md`
- 查看快速参考: `QUESTIONNAIRE_QUICK_REFERENCE.md`
- 查看集成清单: `INTEGRATION_CHECKLIST.md`

---

**文件清单版本**: 1.0  
**最后更新**: 2025-12-02  
**总文件数**: 11 个  
**总代码行数**: ~16,550 行  

