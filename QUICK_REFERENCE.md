# 快速参考卡片

## 模块导入

```python
# 问卷生成
from survey_generator import QuestionnaireGenerator

# 报告生成
from report_generator import ProfessionalReportGenerator
```

---

## 常用代码片段

### 生成单个问卷

```python
from survey_generator import QuestionnaireGenerator

gen = QuestionnaireGenerator()
file = gen.generate_questionnaire(
    output_path='问卷.xlsx',
    enterprise_name='企业名称'
)
print(f"问卷已生成: {file}")
```

### 批量生成问卷

```python
import pandas as pd
from survey_generator import QuestionnaireGenerator

df = pd.DataFrame({'企业名称': ['企业A', '企业B', '企业C']})
gen = QuestionnaireGenerator()
files = gen.generate_batch_questionnaires(df, output_folder='questionnaires')
print(f"已生成 {len(files)} 份问卷")
```

### 生成报告

```python
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator

calc = ScoreCalculator()
gen = ProfessionalReportGenerator(score_calculator=calc)
report = gen.generate_report(questionnaire_file='问卷.xlsx')
print(f"报告已生成: {report}")
```

### 完整工作流

```python
from survey_generator import QuestionnaireGenerator
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator

# 第一步: 生成问卷
q_gen = QuestionnaireGenerator()
questionnaire = q_gen.generate_questionnaire(enterprise_name='示例企业')

# 第二步: 生成报告
calc = ScoreCalculator()
r_gen = ProfessionalReportGenerator(score_calculator=calc)
report = r_gen.generate_report(questionnaire_file=questionnaire)

print(f"问卷: {questionnaire}")
print(f"报告: {report}")
```

---

## Flask集成

```python
from flask import Blueprint, request, jsonify
from survey_generator import QuestionnaireGenerator
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator

api = Blueprint('api', __name__)

@api.post('/questionnaire')
def create_questionnaire():
    gen = QuestionnaireGenerator()
    file = gen.generate_questionnaire(
        enterprise_name=request.json.get('name')
    )
    return {'file': file}

@api.post('/report')
def create_report():
    calc = ScoreCalculator()
    gen = ProfessionalReportGenerator(score_calculator=calc)
    file = gen.generate_report(
        questionnaire_file=request.json.get('questionnaire')
    )
    return {'file': file}
```

---

## 错误处理

```python
from survey_generator import QuestionnaireGenerator

try:
    gen = QuestionnaireGenerator()
    file = gen.generate_questionnaire()
except FileNotFoundError as e:
    print(f"文件错误: {e}")
except Exception as e:
    print(f"生成失败: {e}")
```

---

## 文件位置

| 文件 | 位置 |
|------|------|
| 问卷生成模块 | `survey_generator/` |
| 报告生成模块 | `report_generator/` |
| 使用指南 | `MODULES_USAGE_GUIDE.md` |
| 集成示例 | `INTEGRATION_EXAMPLE.py` |
| 重构总结 | `MODULES_REFACTORING_SUMMARY.md` |

---

## 常见问题

**Q: 如何自定义指标文件？**
```python
gen = QuestionnaireGenerator(indicator_file='/path/to/indicators.xlsx')
```

**Q: 如何指定输出路径？**
```python
gen.generate_questionnaire(output_path='/path/to/output.xlsx')
```

**Q: 如何处理大量生成？**
```python
files = gen.generate_batch_questionnaires(df, output_folder='output')
```

**Q: 报告生成失败怎么办？**
```python
try:
    report = gen.generate_report(questionnaire_file='问卷.xlsx')
except Exception as e:
    print(f"错误: {e}")
```

---

## 运行示例

```bash
# 快速测试
python INTEGRATION_EXAMPLE.py --quick

# 运行特定场景
python INTEGRATION_EXAMPLE.py --scenario 1

# 运行所有场景
python INTEGRATION_EXAMPLE.py
```

---

## 主要类和方法

### QuestionnaireGenerator

| 方法 | 说明 |
|------|------|
| `__init__(indicator_file=None)` | 初始化 |
| `load_indicators()` | 加载指标 |
| `generate_questionnaire()` | 生成问卷 |
| `generate_batch_questionnaires()` | 批量生成 |

### ProfessionalReportGenerator

| 方法 | 说明 |
|------|------|
| `__init__(score_calculator=None)` | 初始化 |
| `generate_report()` | 生成报告 |

---

## 依赖包

```
pandas
openpyxl
python-docx
matplotlib
```

安装:
```bash
pip install pandas openpyxl python-docx matplotlib
```

---

## 更多信息

- 详细文档: `MODULES_USAGE_GUIDE.md`
- 集成示例: `INTEGRATION_EXAMPLE.py`
- 重构总结: `MODULES_REFACTORING_SUMMARY.md`

---

**最后更新**: 2025-11-29

