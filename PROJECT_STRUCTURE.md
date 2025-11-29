# 项目结构说明

## 重构后的项目结构

```
enterprise_report_system/
│
├── 📁 survey_generator/                    # 问卷生成模块（独立）
│   ├── __init__.py                         # 模块初始化
│   └── generator.py                        # 问卷生成器核心实现
│
├── 📁 report_generator/                    # 报告生成模块（独立）
│   ├── __init__.py                         # 模块初始化
│   └── professional_report.py              # 专业报告生成器核心实现
│
├── 📁 expert_portal/                       # 专家门户模块
│   ├── __init__.py
│   ├── routes.py
│   ├── api.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── matcher.py
│   ├── templates/
│   │   └── portal_expert.html
│   └── static/
│
├── 📁 survey_engine/                       # 问卷引擎
│   ├── __init__.py
│   ├── api.py
│   └── services/
│       └── loader.py
│
├── 📁 report_engine/                       # 报告引擎
│   ├── __init__.py
│   └── services/
│
├── 📁 storage/                             # 存储目录
│   ├── submissions/                        # 问卷提交
│   ├── reports/                            # 生成的报告
│   ├── uploads/                            # 上传文件
│   └── special_submissions/                # 特殊提交
│
├── 📁 templates/                           # 页面模板
│   ├── index.html
│   ├── questionnaire.html
│   ├── portal_enterprise.html
│   ├── portal_chamber.html
│   ├── admin_dashboard.html
│   └── admin_login.html
│
├── 📁 static/                              # 静态资源
│   ├── css/
│   ├── js/
│   └── images/
│
├── 📁 docs/                                # 文档
│
├── 📁 scripts/                             # 脚本
│
├── 📄 app.py                               # Flask应用主入[object Object]main.py                              # 主程序入口
│
├[object Object]MODULES_USAGE_GUIDE.md               # 模块使用指南（新建）
├── 📄 MODULES_REFACTORING_SUMMARY.md       # 重构总结（新建）
├── 📄 INTEGRATION_EXAMPLE.py               # 集成示例（新建）
├── 📄 QUICK_REFERENCE.md                   # 快速参考（新建）
├[object Object]STRUCTURE.md                 # 本文件（新建）
│
├[object Object]_calculator.py                  # 评分计算器
├── 📄 questionnaire_generator.py           # 原始问卷生成器（可删除）
├── 📄 professional_report_generator.py     # 原始报告生成器（可删除）
│
├[object Object]                     # 依赖包
├[object Object].json                          # 配置文件
├[object Object]d                            # 项目说明
└── 📄 .gitignore                           # Git忽略文件
```

---

## 模块说明

### 核心模块

#### 1. survey_generator（问卷生成模块）

**位置**: `survey_generator/`

**职责**:
- 生成标准问卷Excel文件
- 支持企业定制化问卷
- 批量生成问卷

**开发者**: 问卷生成模块开发者

**依赖**:
- pandas
- openpyxl
- 指标体系.xlsx

**输出**:
- 问卷Excel文件

**使用示例**:
```python
from survey_generator import QuestionnaireGenerator
gen = QuestionnaireGenerator()
gen.generate_questionnaire(enterprise_name='示例企业')
```

---

#### 2. report_generator（报告生成模块）

**位置**: `report_generator/`

**职责**:
- 生成专业版企业报告
- 支持叙述性、专业性的报告内容
- 自动生成图表和数据分析

**开发者**: 报告生成模块开发者

**依赖**:
- python-docx
- matplotlib
- score_calculator (可选)

**输入**:
- 已填写的问卷文件

**输出**:
- 报告Word文件

**使用示例**:
```python
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator
calc = ScoreCalculator()
gen = ProfessionalReportGenerator(score_calculator=calc)
gen.generate_report(questionnaire_file='问卷.xlsx')
```

---

### 支持模块

#### 3. expert_portal（专家门户）

**位置**: `expert_portal/`

**职责**:
- 提供专家门户页面
- 管理专家相关API

**开发者**: 前端/后端开发者

---

#### 4. survey_engine（问卷引擎）

**位置**: `survey_engine/`

**职责**:
- 问卷加载和管理
- 问卷相关API

**开发者**: 后端开发者

---

#### 5. report_engine（报告引擎）

**位置**: `report_engine/`

**职责**:
- 报告管理
- 报告相关API

**开发者**: 后端开发者

---

## 文件说明

### 新建文件

| 文件 | 说明 | 行数 |
|------|------|------|
| `survey_generator/__init__.py` | 问卷模块初始化 | ~10 |
| `survey_generator/generator.py` | 问卷生成器实现 | ~450 |
| `report_generator/__init__.py` | 报告模块初始化 | ~10 |
| `report_generator/professional_report.py` | 报告生成器实现 | ~800 |
| `MODULES_USAGE_GUIDE.md` | 模块使用指南 | ~300 |
| `MODULES_REFACTORING_SUMMARY.md` | 重构总结 | ~400 |
| `INTEGRATION_EXAMPLE.py` | 集成示例 | ~500 |
| `QUICK_REFERENCE.md` | 快速参考 | ~150 |
| `PROJECT_STRUCTURE.md` | 项目结构说明 | ~300 |

**总计**: ~2,920行新代码和文档

---

### 保留文件

| 文件 | 说明 | 状态 |
|------|------|------|
| `questionnaire_generator.py` | 原始问卷生成器 | 可删除 |
| `professional_report_generator.py` | 原始报告生成器 | 可删除 |
| `score_calculator.py` | 评分计算器 | 保留 |
| `app.py` | Flask应用 | 保留 |
| `main.py` | 主程序 | 保留 |

---

## 目录树详解

### survey_generator 目录

```
survey_generator/
├── __init__.py
│   └── 导出 QuestionnaireGenerator 类
│
└── generator.py
    ├── QuestionnaireGenerator 类
    │   ├── __init__()
    │   ├── load_indicators()
    │   ├── generate_questionnaire()
    │   ├── generate_batch_questionnaires()
    │   ├── _create_enterprise_info_sheet()
    │   ├── _create_instruction_sheet()
    │   ├── _create_questionnaire_sheet()
    │   └── _create_indicator_guide_sheet()
    │
    └── 辅助方法
        └── _get_default_indicator_file()
```

---

### report_generator 目录

```
report_generator/
├── __init__.py
│   └── 导出 ProfessionalReportGenerator 类
│
└── professional_report.py
    ├── ProfessionalReportGenerator 类
    │   ├── __init__()
    │   ├── generate_report()
    │   ├── _setup_professional_styles()
    │   ├── _create_professional_cover()
    │   ├── _create_enterprise_overview()
    │   ├── _create_overall_assessment()
    │   ├── _create_achievements_narrative()
    │   ├── _create_challenges_analysis()
    │   ├── _create_strategic_recommendations()
    │   ├── _create_appendix()
    │   ├── _format_table()
    │   └── 多个辅助方法...
    │
    └── 内部方法
        ├── _generate_positioning_description()
        ├── _generate_dimension_narrative()
        ├── _generate_dimension_highlights()
        ├── _generate_dimension_recommendation()
        ├── _create_dimension_bar_chart()
        ├── _create_dimension_radar_chart()
        └── _create_risk_distribution_pie_chart()
```

---

## 开发者分工

### 问卷生成模块开发者

**文件**:
- `survey_generator/generator.py`
- `survey_generator/__init__.py`

**职责**:
- 维护问卷生成逻辑
- 支持新的指标体系格式
- 优化问卷生成性能
- 处理问卷相关的bug

**测试**:
```bash
python -c "from survey_generator import QuestionnaireGenerator; gen = QuestionnaireGenerator(); gen.generate_questionnaire()"
```

---

### 报告生成模块开发者

**文件**:
- `report_generator/professional_report.py`
- `report_generator/__init__.py`

**职责**:
- 维护报告生成逻辑
- 改进报告内容和格式
- 优化图表生成
- 处理报告相关的bug

**测试**:
```bash
python -c "from report_generator import ProfessionalReportGenerator; from score_calculator import ScoreCalculator; calc = ScoreCalculator(); gen = ProfessionalReportGenerator(score_calculator=calc); gen.generate_report(questionnaire_file='问卷.xlsx')"
```

---

### 主应用开发者

**文件**:
- `app.py`
- `main.py`
- `expert_portal/`
- `survey_engine/`
- `report_engine/`

**职责**:
- 集成两个模块
- 处理用户界面
- 管理文件存储
- 处理业务逻辑

**集成方式**:
```python
from survey_generator import QuestionnaireGenerator
from report_generator import ProfessionalReportGenerator

# 在Flask路由中使用
@app.route('/api/generate')
def generate():
    gen = QuestionnaireGenerator()
    file = gen.generate_questionnaire()
    return {'file': file}
```

---

## 依赖关系图

```
┌─────────────────────────────────────────────────────────┐
│                  Flask应用 (app.py)                     │
└─────────────────────────────────────────────────────────┘
           ↓                              ↓
┌──────────────────────┐      ┌──────────────────────┐
│ survey_generator     │      │ report_generator     │
│ (问卷生成模块)       │      │ (报告生成模块)       │
└──────────────────────┘      └──────────────────────┘
           ↓                              ↓
┌──────────────────────┐      ┌──────────────────────┐
│ pandas, openpyxl     │      │ python-docx,         │
│ 指标体系.xlsx        │      │ matplotlib,          │
│                      │      │ score_calculator     │
└──────────────────────┘      └──────────────────────┘
```

---

## 文件大小估计

| 模块 | 文件数 | 代码行数 | 大小 |
|------|--------|---------|------|
| survey_generator | 2 | ~460 | ~20KB |
| report_generator | 2 | ~810 | ~35KB |
| 文档 | 4 | ~1,150 | ~50KB |
| **总计** | **8** | **~2,420** | **~105KB** |

---

## 迁移检查清单

- [ ] 复制 `survey_generator/` 目录
- [ ] 复制 `report_generator/` 目录
- [ ] 更新导入语句
- [ ] 运行集成示例测试
- [ ] 更新 `requirements.txt`
- [ ] 更新项目文档
- [ ] 运行单元测试
- [ ] 运行集成测试
- [ ] 删除原始文件（可选）
- [ ] 提交代码变更

---

## 常见问题

### Q: 原始文件可以删除吗？

**A**: 可以，但建议先保留一段时间作为备份。确保新模块完全替代后再删除。

### Q: 如何处理现有的导入语句？

**A**: 使用查找替换功能：
- 替换 `from questionnaire_generator import` 为 `from survey_generator import`
- 替换 `from professional_report_generator import` 为 `from report_generator import`

### Q: 新模块与原始模块兼容吗？

**A**: 是的，新模块的API与原始模块兼容，只需更新导入语句。

### Q: 如何测试新模块？

**A**: 运行 `INTEGRATION_EXAMPLE.py` 进行完整测试：
```bash
python INTEGRATION_EXAMPLE.py
```

---

## 后续计划

### 第一阶段（已完成）
- ✅ 创建独立的问卷生成模块
- ✅ 创建独立的报告生成模块
- ✅ 编写完整文档
- ✅ 提供集成示例

### 第二阶段（计划中）
- [ ] 添加单元测试
- [ ] 添加集成测试
- [ ] 发布为Python包
- [ ] 性能优化

### 第三阶段（计划中）
- [ ] 支持更多报告格式
- [ ] 支持更多指标体系
- [ ] 支持数据库存储
- [ ] 支持云存储

---

## 联系方式

- **问卷生成模块**: [开发者邮箱]
- **报告生成模块**: [开发者邮箱]
- **主应用**: [开发者邮箱]

---

**最后更新**: 2025-11-29

**维护者**: 开发团队

