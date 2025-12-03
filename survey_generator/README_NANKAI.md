# 南开大学现代企业制度指数评价问卷生成器

## 功能说明

根据南开大学指标体系Excel文件自动生成三级（初级、中级、高级）调查问卷。

### 特点

1. **三级问卷生成**：支持初级（基础指标）、中级（鼓励指标）、高级（拔高指标）
2. **智能解析**：自动从打分标准生成选择题选项
3. **完整结构**：每个问题包含选择题、填空题、佐证材料要求

## 使用方法

### 基本用法

```python
from nankai_questionnaire_generator import NankaiQuestionnaireGenerator

# 创建生成器
generator = NankaiQuestionnaireGenerator(
    excel_path="南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx"
)

# 生成单个级别问卷
generator.generate_questionnaire(level='初级', output_path='问卷_初级.docx')

# 生成所有级别问卷
results = generator.generate_all_questionnaires(output_dir='output/questionnaires')
```

### 命令行使用

```bash
cd survey_generator
python nankai_questionnaire_generator.py
```

## 问卷级别说明

- **初级问卷（基础指标）**：65个问题，适用于所有民营企业
- **中级问卷（鼓励指标）**：52个问题，适用于治理较规范的企业
- **高级问卷（拔高指标）**：42个问题，适用于治理优秀的企业

## 依赖项

```
pandas>=2.0.0
openpyxl>=3.1.0
python-docx>=1.0.0
