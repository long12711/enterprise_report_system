# 问卷系统快速参考

## [object Object] 分钟快速开始

### 1. 安装依赖（1 分钟）

```bash
pip install python-docx mysql-connector-python
```

### 2. 导入问卷（2 分钟）

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter

importer = DocxQuestionnaireImporter()
result = importer.import_all_questionnaires(
    r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12'
)
print(result)  # 显示导入结果
```

### 3. 启动应用（1 分钟）

```bash
python run_app.py
```

### 4. 访问问卷页面（1 分钟）

```
http://localhost:5000/questionnaire/form
```

## 📋 常用命令

### 导入问卷

```bash
# 导入所有问卷
python -c "
from docx_questionnaire_importer import DocxQuestionnaireImporter
importer = DocxQuestionnaireImporter()
result = importer.import_all_questionnaires(r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12')
print('导入结果:', result)
"
```

### 查看问卷

```bash
# 列出所有问卷
python -c "
from docx_questionnaire_importer import DocxQuestionnaireImporter
importer = DocxQuestionnaireImporter()
surveys = importer.list_surveys()
for s in surveys:
    print(f'{s[\"level\"]}级: {s[\"total_questions\"]} 个问题')
"
```

### 测试系统

```bash
python test_questionnaire_import.py
```

## 🔗 API 快速参考

### 获取问卷

```bash
# 获取所有问卷
curl http://localhost:5000/api/questionnaire/surveys

# 获取初级问卷
curl http://localhost:5000/api/questionnaire/survey/level/初级

# 获取中级问卷
curl http://localhost:5000/api/questionnaire/survey/level/中级

# 获取高级问卷
curl http://localhost:5000/api/questionnaire/survey/level/高级
```

### 创建提交

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/create \
  -H "Content-Type: application/json" \
  -d '{"survey_level": "初级"}'
```

### 保存答案

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/SUBMISSION_ID/save \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "question_id_1": "是",
      "question_id_2": "很有效"
    }
  }'
```

### 提交问卷

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/SUBMISSION_ID/submit \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "question_id_1": "是",
      "question_id_2": "很有效"
    }
  }'
```

### 上传文件

```bash
curl -X POST http://localhost:5000/api/questionnaire/submission/SUBMISSION_ID/upload \
  -F "file=@/path/to/file.pdf" \
  -F "question_id=question_id_1"
```

## 📁 文件位置

| 文件 | 位置 |
|------|------|
| 问卷数据库 | `storage/questionnaires.json` |
| 上传的文件 | `storage/questionnaire_uploads/` |
| 问卷页面 | `templates/questionnaire_form.html` |
| 导入模块 | `docx_questionnaire_importer.py` |
| API 模块 | `questionnaire_management_api.py` |
| 上传处理 | `file_upload_handler.py` |

## 🔍 调试技巧

### 查看导入日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from docx_questionnaire_importer import DocxQuestionnaireImporter
importer = DocxQuestionnaireImporter()
```

### 查看数据库内容

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter
import json

importer = DocxQuestionnaireImporter()
db = importer.load_db()

# 查看问卷
print(json.dumps(db['surveys'], ensure_ascii=False, indent=2))

# 查看问题
print(json.dumps(db['questions'][:3], ensure_ascii=False, indent=2))
```

### 查看上传的文件

```python
from file_upload_handler import FileUploadHandler

handler = FileUploadHandler()
files = handler.list_submission_files('submission_id')
for f in files:
    print(f['name'], f['size'])
```

## ⚙️ 配置调整

### 修改最大文件大小

编辑 `file_upload_handler.py`：

```python
MAX_FILE_SIZE = 200 * 1024 * 1024  # 改为 200MB
```

### 修改允许的文件类型

编辑 `file_upload_handler.py`：

```python
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx',
    'jpg', 'jpeg', 'png', 'zip'
}
```

### 修改数据库路径

编辑 `docx_questionnaire_importer.py`：

```python
importer = DocxQuestionnaireImporter(
    db_path='custom/path/questionnaires.json'
)
```

## 🆘 常见问题快速解决

| 问题 | 解决方案 |
|------|--------|
| 导入失败 | 检查 Word 文件路径和格式 |
| 页面加载慢 | 检查问题数量，考虑分页 |
| 文件上传失败 | 检查文件类型和大小 |
| 数据丢失 | 检查 `storage/questionnaires.json` 文件 |
| API 返回 404 | 检查 URL 和参数 |

## 📊 数据统计

### 查看问卷统计

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter

importer = DocxQuestionnaireImporter()
surveys = importer.list_surveys()

for survey in surveys:
    questions = importer.get_survey_questions(survey['id'])
    print(f"{survey['level']}级: {len(questions)} 个问题")
```

### 查看提交统计

```python
from docx_questionnaire_importer import DocxQuestionnaireImporter

importer = DocxQuestionnaireImporter()
db = importer.load_db()

submissions = db.get('submissions', [])
print(f"总提交数: {len(submissions)}")

# 按状态统计
status_count = {}
for sub in submissions:
    status = sub.get('status', 'unknown')
    status_count[status] = status_count.get(status, 0) + 1

for status, count in status_count.items():
    print(f"  {status}: {count}")
```

## 🔄 备份和恢复

### 备份数据

```bash
# 备份 JSON 数据库
cp storage/questionnaires.json storage/questionnaires.json.backup

# 备份上传的文件
cp -r storage/questionnaire_uploads storage/questionnaire_uploads.backup
```

### 恢复数据

```bash
# 恢复 JSON 数据库
cp storage/questionnaires.json.backup storage/questionnaires.json

# 恢复上传的文件
cp -r storage/questionnaire_uploads.backup storage/questionnaire_uploads
```

## 📞 获取帮助

1. **查看详细文档**
   - 实现指南: `QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md`
   - 集成清单: `INTEGRATION_CHECKLIST.md`

2. **运行测试**
   ```bash
   python test_questionnaire_import.py
   ```

3. **查看日志**
   - 应用日志: `server_run.log`
   - 错误日志: 控制台输出

4. **检查配置**
   - 数据库配置: `questionnaire_management_api.py` 中的 `DB_CONFIG`
   - 文件配置: `file_upload_handler.py` 中的常量

## 🎯 下一步

1. ✅ 导入问卷
2. ✅ 启动应用
3. ✅ 测试问卷填写
4. ✅ 验证文件上传
5. ✅ 检查数据存储
6. ✅ 部署到生产环境

---

**快速参考版本**: 1.0
**最后更新**: 2025-12-02

