# 现代企业制度指数评价系统

## 项目简介

基于工商联指标体系的企业现代制度评价系统，支持问卷生成、自动评分、企业自评报告和整体分析报告生成。

系统包含两种使用方式：
1. **命令行工具** - 问卷生成、报告生成（本文档主要介绍）
2. **Web应用** - Excel文件上传、批量处理、邮件/短信通知（见文档后半部分）


## 系统功能（命令行工具）

### 1. 问卷生成
- 基于231个评价问题的完整指标体系
- 支持单个和批量生成问卷Excel文件
- 自动包含企业信息表、填写说明、问卷和指标说明
- 答案列设置下拉选择，便于填写

### 2. 自动评分
- 支持三种评分类型：合规类、有效性类、一票否决类
- 自动计算总分和各维度得分
- 根据企业类型过滤适用问题
- 生成得分率和评价等级

### 3. 企业自评报告
- Word格式的详细评价报告
- 包含雷达图、得分表等可视化元素
- 各维度详细分析
- 问题清单和改进建议

### 4. 整体分析报告
- 多企业汇总分析
- 企业排名和行业对比
- 共性问题识别
- 最佳实践推荐

## 指标体系结构

### 9大一级指标
1. **党建引领** - 组织建设、政治引领、党建参与治理等
2. **产权结构** - 权属清晰、法人财产独立、股权结构合理
3. **公司治理结构和机制** - 股东会、董事会、监事会治理
4. **战略管理** - 战略规划、导向和执行
5. **内控、风险与合规管理** - 内部控制、风险管理和合规体系
6. **科学民主管理** - 科学管理和员工权益保障
7. **科技创新** - 创新战略和成果转化
8. **社会责任与企业文化** - 社会责任履行和文化建设
9. **家族企业治理** - 家族与企业隔离、协同治理等

总计**231个评价问题**，覆盖多个二级和三级指标。

## 安装依赖

```bash
pip install pandas openpyxl python-docx matplotlib numpy flask
```

## 快速开始（命令行工具）

### 方式一：使用主控制脚本（推荐）

```bash
python main.py
```

运行后会出现菜单，按提示操作即可。

### 方式二：直接使用各模块

#### 1. 生成问卷

```python
from questionnaire_generator import QuestionnaireGenerator

generator = QuestionnaireGenerator()

# 生成单个问卷
questionnaire_path = generator.generate_questionnaire(
    output_path='问卷_测试企业.xlsx',
    enterprise_name='测试科技有限公司'
)
```

#### 2. 生成企业自评报告

```python
from enterprise_report_generator import EnterpriseReportGenerator

generator = EnterpriseReportGenerator()

# 需要已填写的问卷文件
report_path = generator.generate_report('问卷_测试企业_已填写.xlsx')
```

#### 3. 生成整体分析报告

```python
from overall_report_generator import OverallAnalysisReportGenerator

generator = OverallAnalysisReportGenerator()

# 需要多个已填写的问卷文件
questionnaire_files = [
    '问卷_企业1.xlsx',
    '问卷_企业2.xlsx',
    '问卷_企业3.xlsx'
]

report_path = generator.generate_report(questionnaire_files)
```

## 完整使用流程

### 步骤1：生成问卷
```bash
python main.py
# 选择功能1或2，生成问卷Excel文件
```

### 步骤2：填写问卷
1. 使用Excel打开生成的问卷文件
2. 在"企业信息"工作表中填写企业基本信息（必填项带*）
3. 在"问卷"工作表中逐个填写问题答案
   - 合规类：选择"是"或"否"
   - 有效性：选择"很有效"、"比较有效"、"一般"、"不太有效"、"完全无效"
   - 不适用的问题可选"不适用"
4. 保存文件

### 步骤3：生成报告
```bash
python main.py
# 选择功能3生成企业自评报告
# 或选择功能4生成整体分析报告（需要多份问卷）
```

## 评分规则

### 合规类问题
- 选择"是"：得满分
- 选择"否"：得0分

### 有效性问题
- 很有效：满分的100%
- 比较有效：满分的80%
- 一般：满分的60%
- 不太有效：满分的30%
- 完全无效：0分

### 一票否决类
- 选择"否"：直接扣除相应分值（负分）
- 选择"是"：不扣分

### 评价等级
- A级：得分率 ≥ 90%（优秀）
- B级：得分率 80-90%（良好）
- C级：得分率 70-80%（中等）
- D级：得分率 60-70%（及格）
- E级：得分率 < 60%（需改进）

## 项目结构

```
enterprise_report_system/
├── 指标体系.xlsx                    # 评价指标体系Excel文件（231个问题）
├── questionnaire_generator.py       # 问卷生成器
├── score_calculator.py              # 评分计算器
├── enterprise_report_generator.py   # 企业自评报告生成器
├── overall_report_generator.py      # 整体分析报告生成器
├── main.py                          # 主控制脚本（菜单界面）
├── app.py                           # Web应用（Flask）
├── notification_service.py          # 邮件/短信通知服务
└── README.md                        # 本文档
```

## 输出文件

### 问卷文件
- **格式**：Excel (.xlsx)
- **包含工作表**：
  - 企业信息
  - 问卷填写说明
  - 问卷（231个问题）
  - 指标说明

### 企业自评报告
- **格式**：Word (.docx)
- **包含章节**：
  - 封面
  - 目录
  - 报告摘要
  - 企业基本信息
  - 评价结果总览（含雷达图）
  - 各维度详细分析
  - 问题清单与分析
  - 改进建议
  - 附录：得分明细表

### 整体分析报告
- **格式**：Word (.docx)
- **包含章节**：
  - 封面
  - 报告摘要
  - 参评企业概况
  - 总体得分分析（含分布图）
  - 各维度对比分析（含对比图）
  - 企业排名
  - 行业对比分析
  - 共性问题分析
  - 最佳实践
  - 整体建议
  - 附录：企业得分明细表

## 常见问题（命令行工具）

### Q1: 为什么生成的问卷中某些问题标记为"不适用"？
A: 部分问题仅适用于特定类型的企业，例如"股份有限公司"相关问题不适用于"有限责任公司"。系统会根据企业类型自动过滤。

### Q2: 一票否决项是什么意思？
A: 一票否决项是指某些关键性问题，如果回答"否"，会直接扣分。这类问题关系到企业合规性和基本制度建设。

### Q3: 如何批量生成问卷？
A: 准备一个Excel文件，包含"企业名称"列（可选其他信息列），然后使用main.py中的功能2批量生成。

### Q4: 生成的报告可以修改吗？
A: 可以。报告是Word格式，生成后可以使用Word打开进行编辑和调整。

### Q5: 如何修改评分规则？
A: 编辑 `score_calculator.py` 文件中的 `calculate_score` 方法，调整各类问题的评分逻辑。

---

# Web应用功能（可选）

除了命令行工具，系统还提供了Web界面用于批量处理和通知发送。

## Web应用功能特点

- ✅ Web界面操作,简单易用
- ✅ 支持拖拽上传Excel文件
- ✅ 数据预览,实时查看上传内容
- ✅ 自动生成专业的Word格式评估报告
- ✅ 邮件发送报告(支持附件)
- ✅ 短信发送报告链接
- ✅ 批量处理,进度实时显示
- ✅ 错误提示和处理

## 启动Web应用
- ✅ 支持拖拽上传Excel文件
- ✅ 数据预览,实时查看上传内容
- ✅ 自动生成专业的Word格式评估报告
- ✅ 邮件发送报告(支持附件)
- ✅ 短信发送报告链接
- ✅ 批量处理,进度实时显示
- ✅ 错误提示和处理

## 技术栈

- **后端**: Flask (Python)
- **前端**: HTML5 + CSS3 + JavaScript
- **文档处理**: python-docx, openpyxl, pandas
- **邮件发送**: smtplib
- **短信发送**: 支持阿里云/腾讯云/Twilio

## 系统要求

- Python 3.8+
- 支持的操作系统: Windows / Linux / macOS

## 安装步骤

### 1. 克隆或下载项目

```bash
cd enterprise_report_system
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置系统

编辑 `config.json` 文件,配置邮件和短信服务:

```json
{
    "email": {
        "smtp_server": "smtp.qq.com",
        "smtp_port": 587,
        "username": "your_email@qq.com",
        "password": "your_authorization_code",
        "from_name": "企业评价系统",
        "use_tls": true
    },
    "sms": {
        "provider": "aliyun",
        "access_key": "your_access_key",
        "access_secret": "your_access_secret",
        "sign_name": "企业评价系统",
        "template_code": "SMS_12345678"
    }
}
```

#### 邮件配置说明

**QQ邮箱示例:**
- `smtp_server`: smtp.qq.com
- `smtp_port`: 587 (或 465 for SSL)
- `username`: 你的QQ邮箱
- `password`: QQ邮箱授权码(不是登录密码!)

获取QQ邮箱授权码:
1. 登录QQ邮箱
2. 设置 → 账户
3. 开启POP3/SMTP服务
4. 生成授权码

**其他常用邮箱:**
- 163邮箱: smtp.163.com, 端口 25/465
- Gmail: smtp.gmail.com, 端口 587
- Outlook: smtp.office365.com, 端口 587

#### 短信配置说明

系统支持三种短信服务商:

**1. 阿里云短信 (推荐)**
```bash
pip install aliyun-python-sdk-core
```
配置:
```json
{
    "provider": "aliyun",
    "access_key": "你的AccessKey",
    "access_secret": "你的AccessSecret",
    "sign_name": "签名名称",
    "template_code": "模板CODE"
}
```

**2. 腾讯云短信**
```bash
pip install tencentcloud-sdk-python
```

**3. Twilio (国际短信)**
```bash
pip install twilio
```

### 4. 启动系统

```bash
python app.py
```

启动成功后,访问: http://localhost:5000

## Excel文件格式要求

上传的Excel文件必须包含以下列:

| 必需列 | 说明 | 示例 |
|--------|------|------|
| 企业名称 | 企业全称 | XX科技有限公司 |
| 联系人 | 联系人姓名 | 张三 |
| 联系人邮箱 | 用于接收报告 | zhangsan@example.com |
| 联系人手机 | 用于接收短信 | 13800138000 |

其他列将作为评价指标数据,可以自定义添加。

### Excel模板示例

```
企业名称 | 统一社会信用代码 | 联系人 | 联系人邮箱 | 联系人手机 | 党组织建设情况 | ...
XX科技 | 91110000XXXXXXXX | 张三 | xxx@qq.com | 13800138000 | 已建立党支部 | ...
```

## 使用流程

### 1. 上传Excel文件
- 点击或拖拽Excel文件到上传区域
- 支持.xlsx和.xls格式
- 文件大小限制: 16MB

### 2. 预览数据
- 系统会显示前5条记录供预览
- 检查数据是否正确

### 3. 配置选项
- ☑️ 通过邮件发送报告(推荐)
- ☐ 通过短信发送报告链接(可选)

### 4. 开始处理
- 点击"开始处理"按钮
- 系统自动:
  - 逐条读取企业数据
  - 生成自评报告(Word文档)
  - 发送邮件/短信通知
  - 显示实时进度

### 5. 查看结果
- 处理完成后会显示成功/失败统计
- 报告保存在 `reports/` 文件夹
- 企业可通过邮件链接下载报告

## 目录结构

```
enterprise_report_system/
├── app.py                      # 主应用程序
├── report_generator.py         # 报告生成模块
├── notification_service.py     # 通知服务模块
├── config.json                 # 配置文件
├── requirements.txt            # 依赖列表
├── README.md                   # 说明文档
├── templates/                  # HTML模板
│   └── index.html             # 主页面
├── uploads/                    # 上传文件存储目录
├── reports/                    # 生成报告存储目录
└── static/                     # 静态资源
    ├── css/                   # CSS样式
    └── js/                    # JavaScript脚本
```

## 生成的报告内容

每个企业的自评报告包含以下部分:

1. **企业基本信息**
   - 企业名称、代码、成立时间等
   - 联系人信息

2. **评价指标自评**
   - 党建引领
   - 治理结构
   - 运营机制
   - 监督机制

3. **评分汇总**
   - 各维度得分
   - 加权综合得分

4. **评价结论**
   - 评价等级
   - 总体评价

5. **改进建议**
   - 针对性改进意见
   - 优化方向

## API接口

系统提供以下API接口:

### 1. 上传文件
```
POST /upload
Content-Type: multipart/form-data

参数:
- file: Excel文件

返回:
{
    "success": true,
    "filename": "文件名",
    "total_records": 100,
    "preview": [...],
    "columns": [...]
}
```

### 2. 处理文件
```
POST /process
Content-Type: application/json

参数:
{
    "filepath": "上传文件路径",
    "send_email": true,
    "send_sms": false
}

返回:
{
    "success": true,
    "task_id": "任务ID"
}
```

### 3. 查询进度
```
GET /status/<task_id>

返回:
{
    "status": "processing",
    "total": 100,
    "processed": 50,
    "success": 45,
    "failed": 5,
    "errors": []
}
```

### 4. 下载报告
```
GET /download/<filename>

返回: 文件下载
```

## 常见问题

### Q1: 邮件发送失败怎么办?
A:
1. 检查config.json中的邮箱配置是否正确
2. 确认使用的是授权码而不是登录密码
3. 检查网络连接和防火墙设置
4. 使用 /test_email 接口测试邮件发送

### Q2: 短信发送失败怎么办?
A:
1. 确认已安装对应的短信SDK
2. 检查access_key和access_secret是否正确
3. 确认短信签名和模板已审核通过
4. 检查账户余额是否充足

### Q3: Excel文件上传后提示缺少列?
A: 确保Excel文件包含必需的列: 企业名称、联系人、联系人邮箱、联系人手机

### Q4: 如何自定义报告模板?
A: 修改 `report_generator.py` 中的 `generate_report` 方法

### Q5: 如何修改评分规则?
A: 修改 `report_generator.py` 中的 `_calculate_scores` 方法

## 安全建议

1. **配置文件安全**
   - 不要将 config.json 提交到公开的代码仓库
   - 保护好邮箱授权码和短信API密钥

2. **生产环境部署**
   - 使用环境变量存储敏感信息
   - 启用HTTPS
   - 设置合理的文件上传限制
   - 添加用户认证机制

3. **数据安全**
   - 定期清理上传的文件
   - 加密存储敏感数据
   - 设置访问权限

## 性能优化

1. **大文件处理**
   - 增加文件大小限制: `app.config['MAX_CONTENT_LENGTH']`
   - 使用分批处理

2. **并发处理**
   - 使用Celery进行异步任务处理
   - 部署多个Worker进程

3. **缓存优化**
   - 添加Redis缓存
   - 缓存常用数据

## 扩展开发

### 添加新的短信服务商

在 `notification_service.py` 中添加新方法:

```python
def _send_custom_sms(self, phone, config, message):
    # 实现自定义短信发送逻辑
    pass
```

### 自定义报告模板

修改 `report_generator.py` 中的报告生成逻辑。

### 添加数据库支持

可以集成SQLAlchemy进行数据持久化:

```bash
pip install flask-sqlalchemy
```

## 技术支持

如有问题,请通过以下方式联系:

- 邮箱: support@example.com
- 项目地址: https://github.com/yourname/enterprise_report_system

## 更新日志

### v1.0.0 (2025-10-31)
- ✅ 初始版本发布
- ✅ 实现Excel上传功能
- ✅ 实现报告生成功能
- ✅ 实现邮件发送功能
- ✅ 实现短信发送功能
- ✅ Web界面开发完成

## 许可证

MIT License

## 致谢

感谢使用本系统!
