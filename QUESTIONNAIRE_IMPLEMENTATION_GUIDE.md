# 现代企业制度指数评价问卷系统 - 实现指南

## 概述

本文档详细说明如何实现从Word文档导入问卷题目、企业填写问卷、上传附件、存储数据到数据库的完整流程。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    前端页面                                  │
│              (questionnaire_form.html)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  问卷管理 API                                │
│         (questionnaire_management_api.py)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • 导入问卷        /api/questionnaire/import          │  │
│  │ • 查询问卷        /api/questionnaire/surveys         │  │
│  │ • 创建提交        /api/questionnaire/submission/...  │  │
│  │ • 保存/提交答案   /api/questionnaire/submission/...  │  │
│  │ • 上传附件        /api/questionnaire/submission/.../upload │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   数据层                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • JSON 数据库 (questionnaires.json)                  │  │
│  │ • MySQL 数据库 (questionnaire_templates 等表)        │  │
│  │ • 文件存储 (storage/questionnaire_uploads/)          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 核心模块

### 1. Word 文档导入模块 (docx_questionnaire_importer.py)

**功能**：从Word文档中提取问卷题目并存储到数据库

**主要类**：`DocxQuestionnaireImporter`

**关键方法**：
- `import_questionnaire(docx_path, level, survey_name)` - 导入单个问卷
- `import_all_questionnaires(docx_dir)` - 批量导入问卷
- `get_survey(survey_id)` - 获取问卷信息
- `get_survey_questions(survey_id)` - 获取问卷问题
- `get_survey_by_level(level)` - 按级别获取问卷

**Word 文档格式要求**：

| 列 | 内容 | 说明 |
|---|---|---|
| A | 序号 | 问题序号 |
| B | 一级指标 | 如：党建引领、产权结构等 |
| C | 二级指标 | 如：党组织建设、权属清晰等 |
| D | 题目 | 具体问题文本 |
| E | 题目类型 | 合规类、有效性、数字等 |
| F | 分值 | 该问题的分值 |
| G | 适用对象 | 所有企业、公司制企业等 |
| H | 补充数据/说明 | 是否需要上传文件 |

**使用示例**：

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter

importer = DocxQuestionnaireImporter()

# 导入初级问卷
survey_id = importer.import_questionnaire(
    'path/to/初级问卷.docx',
    '初级',
    '现代企业制度指数评价问卷_初级'
)

# 获取问卷信息
survey = importer.get_survey(survey_id)
questions = importer.get_survey_questions(survey_id)
```

### 2. 问卷管理 API (questionnaire_management_api.py)

**功能**：提供问卷的导入、查询、填写、提交等 API 接口

**API 端点**：

#### 导入接口

```
POST /api/questionnaire/import
请求体：
{
    "docx_path": "文件路径",
    "level": "初级|中级|高级",
    "survey_name": "问卷名称（可选）"
}
```

```
POST /api/questionnaire/import-batch
请求体：
{
    "docx_dir": "包含Word文档的目录"
}
```

#### 查询接口

```
GET /api/questionnaire/surveys
返回所有问卷列表

GET /api/questionnaire/survey/<survey_id>
返回指定问卷的详细信息

GET /api/questionnaire/survey/level/<level>
按级别获取问卷（初级、中级、高级）
```

#### 问卷填写接口

```
POST /api/questionnaire/submission/create
创建新的问卷提交
请求体：
{
    "survey_level": "初级|中级|高级"
}

GET /api/questionnaire/submission/<submission_id>
获取问卷提交详情

POST /api/questionnaire/submission/<submission_id>/save
保存问卷答案（草稿）
请求体：
{
    "answers": {
        "question_id": "answer_value",
        ...
    }
}

POST /api/questionnaire/submission/<submission_id>/submit
提交问卷
请求体：
{
    "answers": {
        "question_id": "answer_value",
        ...
    }
}
```

#### 文件上传接口

```
POST /api/questionnaire/submission/<submission_id>/upload
上传问卷附件
表单数据：
- file: 文件
- question_id: 问题ID
```

### 3. 文件上传处理模块 (file_upload_handler.py)

**功能**：处理问卷附件的上传、存储和管理

**主要类**：`FileUploadHandler`

**关键方法**：
- `save_file(file_obj, submission_id, question_id)` - 保存上传的文件
- `delete_file(file_path)` - 删除文件
- `list_submission_files(submission_id)` - 列出提交的所有文件
- `cleanup_old_files(days)` - 清理旧文件

**配置**：
- 允许的文件类型：pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif, bmp, txt, csv, zip, rar, 7z
- 最大文件大小：100MB
- 存储目录：`storage/questionnaire_uploads/`

### 4. 前端页面 (questionnaire_form.html)

**功能**：企业用户填写问卷的前端界面

**主要特性**：
- 问卷级别选择（初级、中级、高级）
- 动态问题渲染（支持单选、多选、文本、数字等类型）
- 进度条显示
- 草稿保存功能
- 文件上传功能
- 实时验证

**页面流程**：
1. 用户选择问卷级别
2. 系统加载对应级别的问卷
3. 用户逐个填写问题
4. 对于需要附件的问题，用户上传文件
5. 用户可以保存草稿或直接提交
6. 提交后显示成功提示

## 数据库设计

### JSON 数据库结构 (questionnaires.json)

```json
{
  "surveys": [
    {
      "id": "survey_id",
      "name": "问卷名称",
      "level": "初级|中级|高级",
      "description": "问卷描述",
      "total_questions": 100,
      "status": "active|inactive",
      "created_at": "2025-12-02T...",
      "updated_at": "2025-12-02T..."
    }
  ],
  "questions": [
    {
      "id": "question_id",
      "survey_id": "survey_id",
      "seq_no": "1",
      "level1": "一级指标",
      "level2": "二级指标",
      "question_text": "问题文本",
      "question_type": "合规类|有效性|数字|文本",
      "score": "10",
      "applicable": "所有企业|公司制企业",
      "remarks": "备注说明",
      "requires_file": true
    }
  ],
  "submissions": [
    {
      "id": "submission_id",
      "enterprise_id": "enterprise_id",
      "survey_id": "survey_id",
      "survey_level": "初级|中级|高级",
      "status": "draft|submitted|reviewed",
      "total_score": 85.5,
      "created_at": "2025-12-02T...",
      "submitted_at": "2025-12-02T..."
    }
  ],
  "answers": {
    "submission_id": {
      "question_id": "answer_value",
      ...
    }
  },
  "attachments": {
    "submission_id": [
      {
        "id": "attachment_id",
        "question_id": "question_id",
        "file_name": "原始文件名",
        "file_path": "存储路径",
        "file_size": 1024,
        "upload_time": "2025-12-02T..."
      }
    ]
  }
}
```

### MySQL 数据库表

详见 `db/095_questionnaire_submissions.sql`

主要表：
- `questionnaire_templates` - 问卷模板
- `questionnaire_template_questions` - 模板问题
- `questionnaire_submissions` - 问卷提交记录
- `questionnaire_answers` - 问卷答案
- `questionnaire_attachments` - 问卷附件

## 实现步骤

### 第一步：准备 Word 文档

确保 Word 文档包含以下列：
- 序号、一级指标、二级指标、题目、题目类型、分值、适用对象、补充数据/说明

### 第二步：安装依赖

```bash
pip install python-docx mysql-connector-python
```

### 第三步：导入问卷

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter

importer = DocxQuestionnaireImporter()

# 导入三个级别的问卷
docx_dir = r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12'
result = importer.import_all_questionnaires(docx_dir)

print("导入结果:")
for level, survey_id in result.items():
    if survey_id:
        print(f"  {level}级: {survey_id}")
```

### 第四步：初始化数据库

```bash
# 执行 SQL 脚本
mysql -u root -p enterprise_system < db/095_questionnaire_submissions.sql
```

### 第五步：启动应用

```bash
python run_app.py
```

### 第六步：访问问卷页面

```
http://localhost:5000/questionnaire/form
```

## 工作流程

### 企业填写问卷的完整流程

```
1. 企业用户访问 /questionnaire/form
   ↓
2. 选择问卷级别（初级/中级/高级）
   ↓
3. 系统调用 GET /api/questionnaire/survey/level/<level>
   ↓
4. 系统调用 POST /api/questionnaire/submission/create
   ↓
5. 前端渲染问卷表单
   ↓
6. 企业填写问题答案
   ↓
7. 对于需要附件的问题，企业上传文件
   ↓
8. 企业可以：
   a) 点击"保存草稿" → POST /api/questionnaire/submission/<id>/save
   b) 点击"提交问卷" → POST /api/questionnaire/submission/<id>/submit
   ↓
9. 系统保存答案和附件到数据库
   ↓
10. 显示提交成功提示
```

### 管理员导入问卷的流程

```
1. 管理员调用 POST /api/questionnaire/import-batch
   ↓
2. 系统扫描目录，查找包含"初级"、"中级"、"高级"的 Word 文件
   ↓
3. 对每个文件调用 import_questionnaire()
   ↓
4. 提取表格数据，创建问卷和问题记录
   ↓
5. 保存到 JSON 数据库和 MySQL 数据库
   ↓
6. 返回导入结果
```

## API 调用示例

### 导入问卷

```bash
curl -X POST http://localhost:5000/api/questionnaire/import \
  -H "Content-Type: application/json" \
  -d '{
    "docx_path": "path/to/初级问卷.docx",
    "level": "初级"
  }'
```

### 获取问卷列表

```bash
curl http://localhost:5000/api/questionnaire/surveys
```

### 获取指定级别的问卷

```bash
curl http://localhost:5000/api/questionnaire/survey/level/初级
```

### 创建问卷提交

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/create \
  -H "Content-Type: application/json" \
  -d '{
    "survey_level": "初级"
  }'
```

### 保存问卷答案

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/abc123/save \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "q1": "是",
      "q2": "很有效",
      "q3": "100"
    }
  }'
```

### 提交问卷

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/abc123/submit \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "q1": "是",
      "q2": "很有效",
      "q3": "100"
    }
  }'
```

### 上传附件

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/abc123/upload \
  -F "file=@/path/to/file.pdf" \
  -F "question_id=q1"
```

## 文件结构

```
project_root/
├── docx_questionnaire_importer.py      # Word 文档导入模块
├── questionnaire_management_api.py     # 问卷管理 API
├── file_upload_handler.py              # 文件上传处理模块
├── app.py                              # 主应用（已集成）
├── templates/
│   └── questionnaire_form.html         # 问卷填写页面
├── db/
│   └── 095_questionnaire_submissions.sql  # 数据库表定义
├── storage/
│   ├── questionnaires.json             # JSON 数据库
│   └── questionnaire_uploads/          # 上传的附件存储目录
│       └── <submission_id>/
│           └── <question_id>_*.pdf
└── QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md  # 本文档
```

## 常见问题

### Q1: 如何修改允许的文件类型？

编辑 `file_upload_handler.py` 中的 `ALLOWED_EXTENSIONS`：

```python
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'jpg', 'jpeg', 'png', 'gif', 'bmp',
    'txt', 'csv', 'zip', 'rar', '7z'
}
```

### Q2: 如何修改最大文件大小？

编辑 `file_upload_handler.py` 中的 `MAX_FILE_SIZE`：

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

### Q3: 如何处理中文文件名的问题？

系统已经使用 `secure_filename()` 处理文件名，并生成 UUID 作为文件标识。原始文件名保存在数据库中。

### Q4: 如何备份问卷数据？

```bash
# 备份 JSON 数据库
cp storage/questionnaires.json storage/questionnaires.json.backup

# 备份上传的文件
cp -r storage/questionnaire_uploads storage/questionnaire_uploads.backup

# 备份 MySQL 数据库
mysqldump -u root -p enterprise_system > backup.sql
```

### Q5: 如何恢复已删除的问卷？

从备份文件恢复：

```bash
cp storage/questionnaires.json.backup storage/questionnaires.json
```

## 性能优化建议

1. **数据库索引**：确保已创建必要的索引（见 SQL 脚本）
2. **文件存储**：定期清理旧的上传文件
3. **缓存**：考虑使用 Redis 缓存问卷数据
4. **异步处理**：对于大文件上传，考虑使用异步任务队列

## 安全建议

1. **文件验证**：系统已验证文件类型和大小
2. **访问控制**：使用 `@login_required` 和 `@enterprise_required` 装饰器
3. **文件隔离**：每个提交的文件存储在单独的目录中
4. **数据加密**：考虑对敏感数据进行加密存储

## 扩展功能

### 可以添加的功能

1. **问卷评分**：自动计算问卷得分
2. **报告生成**：基于问卷答案生成评价报告
3. **对比分析**：对比不同企业的问卷结果
4. **数据导出**：导出问卷数据为 Excel/PDF
5. **权限管理**：不同角色的权限控制
6. **审核流程**：问卷提交后的审核流程
7. **通知系统**：问卷提交/审核的通知

## 技术栈

- **后端**：Flask, Python 3.7+
- **前端**：HTML5, CSS3, JavaScript
- **数据库**：MySQL, JSON
- **文件处理**：python-docx, werkzeug
- **认证**：Flask Session

## 支持

如有问题，请参考：
- API 文档：`API_DOCUMENTATION.md`
- 项目结构：`PROJECT_STRUCTURE.md`
- 快速开始：`QUICK_START.md`

