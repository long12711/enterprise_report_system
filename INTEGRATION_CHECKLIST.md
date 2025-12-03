# 问卷系统集成检查清单

## 集成步骤

### ✅ 第一阶段：准备工作

- [ ] 确认 Word 文档位置
  - 初级问卷: `D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12\南开大学现代企业制度指数评价问卷_初级_20251202_180815.docx`
  - 中级问卷: `南开大学现代企业制度指数评价问卷_中级_20251202_180815.docx`
  - 高级问卷: `南开大学现代企业制度指数评价问卷_高级_20251202_180815.docx`

- [ ] 检查 Word 文档格式
  - [ ] 包含表格
  - [ ] 表格包含 8 列（序号、一级指标、二级指标、题目、题目类型、分值、适用对象、补充数据/说明）
  - [ ] 第一行为表头

- [ ] 安装依赖包
  ```bash
  pip install python-docx
  pip install mysql-connector-python
  ```

### ✅ 第二阶段：代码集成

- [ ] 复制文件到项目根目录
  - [ ] `docx_questionnaire_importer.py`
  - [ ] `questionnaire_management_api.py`
  - [ ] `file_upload_handler.py`
  - [ ] `templates/questionnaire_form.html`

- [ ] 更新 `app.py`
  - [ ] 添加问卷管理蓝图注册（已完成）
  - [ ] 添加问卷表单页面路由（已完成）

- [ ] 验证导入
  ```python
  from docx_questionnaire_importer import DocxQuestionnaireImporter
  from questionnaire_management_api import questionnaire_bp
  from file_upload_handler import FileUploadHandler
  ```

### ✅ 第三阶段：数据库设置

- [ ] 执行 SQL 脚本（可选，如果使用 MySQL）
  ```bash
  mysql -u root -p enterprise_system < db/095_questionnaire_submissions.sql
  ```

- [ ] 验证数据库表创建
  ```sql
  SHOW TABLES LIKE 'questionnaire%';
  ```

- [ ] 配置数据库连接
  - [ ] 检查 `questionnaire_management_api.py` 中的 `DB_CONFIG`
  - [ ] 确保环境变量正确设置

### ✅ 第四阶段：导入问卷

- [ ] 运行导入测试脚本
  ```bash
  python test_questionnaire_import.py
  ```

- [ ] 验证导入结果
  - [ ] 检查 `storage/questionnaires.json` 文件
  - [ ] 确认包含三个级别的问卷
  - [ ] 验证问题数量

- [ ] 检查导入的数据
  ```python
  from docx_questionnaire_importer import DocxQuestionnaireImporter
  
  importer = DocxQuestionnaireImporter()
  surveys = importer.list_surveys()
  for survey in surveys:
      print(f"{survey['level']}: {survey['total_questions']} 个问题")
  ```

### ✅ 第五阶段：前端集成

- [ ] 验证模板文件
  - [ ] `templates/questionnaire_form.html` 存在
  - [ ] 包含所有必要的 JavaScript 代码

- [ ] 测试页面访问
  - [ ] 启动应用: `python run_app.py`
  - [ ] 访问: `http://localhost:5000/questionnaire/form`
  - [ ] 验证页面加载正常

- [ ] 测试问卷加载
  - [ ] 点击"初级问卷"按钮
  - [ ] 验证问题加载
  - [ ] 检查问题显示正确

### ✅ 第六阶段：功能测试

- [ ] 测试问卷填写
  - [ ] 选择问卷级别
  - [ ] 填写问题答案
  - [ ] 保存草稿
  - [ ] 提交问卷

- [ ] 测试文件上传
  - [ ] 上传 PDF 文件
  - [ ] 上传 Word 文件
  - [ ] 验证文件保存
  - [ ] 检查文件大小限制

- [ ] 测试数据存储
  - [ ] 检查 `storage/questionnaires.json` 中的答案
  - [ ] 检查 `storage/questionnaire_uploads/` 中的文件
  - [ ] 验证数据库记录（如果使用 MySQL）

### ✅ 第七阶段：API 测试

- [ ] 测试导入 API
  ```bash
  curl -X POST http://localhost:5000/api/questionnaire/import \
    -H "Content-Type: application/json" \
    -d '{"docx_path": "path/to/file.docx", "level": "初级"}'
  ```

- [ ] 测试查询 API
  ```bash
  curl http://localhost:5000/api/questionnaire/surveys
  curl http://localhost:5000/api/questionnaire/survey/level/初级
  ```

- [ ] 测试提交 API
  ```bash
  curl -X POST http://localhost:5000/api/questionnaire/submission/create \
    -H "Content-Type: application/json" \
    -d '{"survey_level": "初级"}'
  ```

### ✅ 第八阶段：性能和安全

- [ ] 性能测试
  - [ ] 测试大文件上传（接近 100MB）
  - [ ] 测试多个并发请求
  - [ ] 检查响应时间

- [ ] 安全测试
  - [ ] 测试文件类型验证
  - [ ] 测试文件大小限制
  - [ ] 测试访问控制

- [ ] 错误处理
  - [ ] 测试无效的问卷级别
  - [ ] 测试不存在的提交 ID
  - [ ] 测试网络错误

### ✅ 第九阶段：文档和培训

- [ ] 准备文档
  - [ ] `QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md` - 实现指南
  - [ ] `INTEGRATION_CHECKLIST.md` - 本清单
  - [ ] API 文档

- [ ] 准备培训材料
  - [ ] 用户操作指南
  - [ ] 管理员操作指南
  - [ ] 常见问题解答

### ✅ 第十阶段：部署

- [ ] 生产环境准备
  - [ ] 配置环境变量
  - [ ] 设置数据库连接
  - [ ] 配置文件存储路径

- [ ] 备份策略
  - [ ] 定期备份 JSON 数据库
  - [ ] 定期备份上传的文件
  - [ ] 定期备份 MySQL 数据库

- [ ] 监控和日志
  - [ ] 配置日志记录
  - [ ] 设置错误告警
  - [ ] 监控磁盘空间

## 文件清单

### 新增文件

```
docx_questionnaire_importer.py          # Word 文档导入模块
questionnaire_management_api.py         # 问卷管理 API
file_upload_handler.py                  # 文件上传处理模块
test_questionnaire_import.py            # 测试脚本
templates/questionnaire_form.html       # 问卷填写页面
db/095_questionnaire_submissions.sql    # 数据库表定义
QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md   # 实现指南
INTEGRATION_CHECKLIST.md                # 本清单
```

### 修改的文件

```
app.py                                  # 添加问卷管理蓝图和路由
```

### 生成的目录

```
storage/
├── questionnaires.json                 # 问卷数据库
└── questionnaire_uploads/              # 上传的附件
    └── <submission_id>/
        └── <question_id>_*.pdf
```

## 常见问题

### Q: 导入失败，提示"文件不存在"

**A:** 检查 Word 文档路径是否正确。可以运行以下命令验证：

```python
import os
docx_dir = r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12'
print(os.path.isdir(docx_dir))
print(os.listdir(docx_dir))
```

### Q: 导入成功但问题数为 0

**A:** 检查 Word 文档的表格格式：
- 确保第一行是表头
- 确保有 8 列
- 确保数据行不为空

### Q: 上传文件失败，提示"不支持的文件类型"

**A:** 检查文件扩展名是否在允许列表中。编辑 `file_upload_handler.py` 中的 `ALLOWED_EXTENSIONS`。

### Q: 问卷页面加载缓慢

**A:** 
- 检查问题数量是否过多
- 检查网络连接
- 考虑添加缓存

### Q: 文件上传超时

**A:**
- 增加 Flask 的超时时间
- 考虑使用异步上传
- 检查文件大小是否超过限制

## 回滚计划

如果需要回滚，按以下步骤操作：

1. **恢复代码**
   ```bash
   git revert <commit_hash>
   ```

2. **恢复数据**
   ```bash
   cp storage/questionnaires.json.backup storage/questionnaires.json
   ```

3. **恢复数据库**
   ```bash
   mysql -u root -p enterprise_system < backup.sql
   ```

## 验证清单

部署完成后，请验证以下功能：

- [ ] 问卷页面可以访问
- [ ] 问卷可以加载
- [ ] 可以填写问卷
- [ ] 可以上传文件
- [ ] 可以保存草稿
- [ ] 可以提交问卷
- [ ] 数据正确保存
- [ ] API 接口正常工作
- [ ] 错误处理正常
- [ ] 性能满足要求

## 支持联系

如有问题，请参考：
- 实现指南: `QUESTIONNAIRE_IMPLEMENTATION_GUIDE.md`
- API 文档: `API_DOCUMENTATION.md`
- 项目结构: `PROJECT_STRUCTURE.md`

## 版本信息

- 创建日期: 2025-12-02
- 版本: 1.0
- 状态: 待部署

