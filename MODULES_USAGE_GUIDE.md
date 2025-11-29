# 独立模块使用指南

本文档说明如何使用独立的问卷生成模块和报告生成模块。

## 目录结构

```
enterprise_report_system/
├── survey_generator/          # 问卷生成模块（独立）
│   ├── __init__.py
│   └── generator.py           # 问卷生成器核心代码
├── report_generator/          # 报告生成模块（独立）
│   ├── __init__.py
│   └── professional_report.py # 专业报告生成器核心代码
├── MODULES_USAGE_GUIDE.md     # 本文档
└── ...其他文件
```

## 模块特点

### 1. 问卷生成模块 (`survey_generator`)

**独立性**：
- ✅ 完全独立，无外部依赖
- ✅ 可单独导入使用
- ✅ 支持灵活配置指标文件路径

**功能**：
- 生成标准问卷Excel文件
- 支持企业定制化问卷
- 批量生成问卷
- 自动生成企业信息表、填写说明、问卷、指标说明等工作表

### 2. 报告生成模块 (`report_generator`)

**独立性**：
- ✅ 相对独立，仅依赖评分计算器
- ✅ 支持外部传入评分计算器
- ✅ 自动处理计算器缺失情况

**功能**：
- 生成专业版企业报告
- 支持叙述性、专业性的报告内容
- 自动生成图表和数据分析
- 支持定制化报告路径

---

## 使用示例

### 方式一：直接导入使用

#### 1. 生成问卷

```python
from survey_generator import QuestionnaireGenerator

# 初始化问卷生成器
generator = QuestionnaireGenerator()

# 生成单个问卷
output_file = generator.generate_questionnaire(
    output_path='问卷_示例企业.xlsx',
    enterprise_name='示例企业有限公司'
)

print(f"问卷已生成: {output_file}")
```

#### 2. 批量生成问卷

```python
import pandas as pd
from survey_generator import QuestionnaireGenerator

# 准备企业数据
enterprises_data = {
    '企业名称': ['企业A', '企业B', '企业C']
}
enterprises_df = pd.DataFrame(enterprises_data)

# 初始化生成器
generator = QuestionnaireGenerator()

# 批量生成
files = generator.generate_batch_questionnaires(
    enterprises_df,
    output_folder='questionnaires'
)

print(f"已生成 {len(files)} 份问卷")
```

#### 3. 生成报告

```python
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator

# 初始化评分计算器和报告生成器
calculator = ScoreCalculator()
report_generator = ProfessionalReportGenerator(score_calculator=calculator)

# 生成报告
report_file = report_generator.generate_report(
    questionnaire_file='问卷_示例企业.xlsx',
    output_path='reports/报告_示例企业.docx'
)

print(f"报告已生成: {report_file}")
```

### 方式二：在Flask应用中集成

#### 在API路由中使用

```python
from flask import Blueprint, request, jsonify
from survey_generator import QuestionnaireGenerator
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator

# 创建蓝图
api_bp = Blueprint('api', __name__)

@api_bp.post('/generate-questionnaire')
def generate_questionnaire():
    """生成问卷API"""
    try:
        data = request.json
        enterprise_name = data.get('enterprise_name')
        
        # 使用问卷生成模块
        generator = QuestionnaireGenerator()
        output_file = generator.generate_questionnaire(
            enterprise_name=enterprise_name
        )
        
        return jsonify({
            'success': True,
            'file': output_file,
            'message': '问卷生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.post('/generate-report')
def generate_report():
    """生成报告API"""
    try:
        data = request.json
        questionnaire_file = data.get('questionnaire_file')
        
        # 使用报告生成模块
        calculator = ScoreCalculator()
        report_generator = ProfessionalReportGenerator(
            score_calculator=calculator
        )
        
        output_file = report_generator.generate_report(
            questionnaire_file=questionnaire_file
        )
        
        return jsonify({
            'success': True,
            'file': output_file,
            'message': '报告生成成功'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### 方式三：命令行使用

#### 生成问卷

```bash
python -c "
from survey_generator import QuestionnaireGenerator
gen = QuestionnaireGenerator()
gen.generate_questionnaire(
    output_path='问卷.xlsx',
    enterprise_name='示例企业'
)
"
```

#### 生成报告

```bash
python -c "
from report_generator import ProfessionalReportGenerator
from score_calculator import ScoreCalculator
calc = ScoreCalculator()
gen = ProfessionalReportGenerator(score_calculator=calc)
gen.generate_report(questionnaire_file='问卷.xlsx')
"
```

---

## API 参考

### QuestionnaireGenerator

#### 初始化

```python
generator = QuestionnaireGenerator(indicator_file=None)
```

**参数**：
- `indicator_file` (str, optional): 指标体系Excel文件路径
  - 如果为None，将自动查找默认位置
  - 支持的位置：
    - `D:\Claude Code\enterprise_report_system\指标体系.xlsx`
    - `./指标体系.xlsx`
    - `../指标体系.xlsx`

#### 方法

##### `generate_questionnaire(output_path=None, enterprise_name=None)`

生成单个问卷

**参数**：
- `output_path` (str, optional): 输出文件路径，默认为 `问卷_YYYYMMDD_HHMMSS.xlsx`
- `enterprise_name` (str, optional): 企业名称，用于问卷定制

**返回**：
- 生成的文件路径 (str)

**异常**：
- `FileNotFoundError`: 指标文件不存在
- `Exception`: 生成失败

**示例**：
```python
file = generator.generate_questionnaire(
    output_path='问卷_示例.xlsx',
    enterprise_name='示例企业'
)
```

##### `generate_batch_questionnaires(enterprises_df, output_folder='questionnaires')`

批量生成问卷

**参数**：
- `enterprises_df` (pd.DataFrame): 企业信息DataFrame，必须包含'企业名称'列
- `output_folder` (str, optional): 输出文件夹，默认为 `questionnaires`

**返回**：
- 生成的文件列表 (list)

**异常**：
- `Exception`: 生成失败

**示例**：
```python
import pandas as pd
df = pd.DataFrame({'企业名称': ['企业A', '企业B']})
files = generator.generate_batch_questionnaires(df)
```

##### `load_indicators()`

加载指标体系

**异常**：
- `FileNotFoundError`: 指标文件不存在
- `Exception`: 加载失败

---

### ProfessionalReportGenerator

#### 初始化

```python
generator = ProfessionalReportGenerator(score_calculator=None)
```

**参数**：
- `score_calculator` (ScoreCalculator, optional): 评分计算器实例
  - 如果为None，将尝试导入默认的ScoreCalculator
  - 如果导入失败，某些功能可能不可用

#### 方法

##### `generate_report(questionnaire_file, output_path=None)`

生成专业版企业报告

**参数**：
- `questionnaire_file` (str): 已填写的问卷文件路径 (必需)
- `output_path` (str, optional): 输出报告文件路径
  - 如果为None，将在 `reports/` 目录生成
  - 默认文件名：`专业报告_[问卷名称].docx`

**返回**：
- 生成的报告文件路径 (str)

**异常**：
- `FileNotFoundError`: 问卷文件不存在
- `Exception`: 生成失败

**示例**：
```python
from score_calculator import ScoreCalculator

calculator = ScoreCalculator()
generator = ProfessionalReportGenerator(score_calculator=calculator)

report = generator.generate_report(
    questionnaire_file='问卷_示例企业.xlsx',
    output_path='reports/报告_示例企业.docx'
)
```

---

## 配置说明

### 指标文件配置

问卷生成器支持多个指标文件位置，自动查找顺序：

1. `D:\Claude Code\enterprise_report_system\指标体系.xlsx` (Windows默认路径)
2. `./指标体系.xlsx` (当前目录)
3. `../指标体系.xlsx` (上级目录)
4. `<模块目录>/../指标体系.xlsx` (相对模块的上级目录)

**自定义指标文件**：

```python
generator = QuestionnaireGenerator(
    indicator_file='/path/to/custom/indicators.xlsx'
)
```

### 输出目录配置

**问卷输出**：
```python
# 默认在当前目录生成
generator.generate_questionnaire()

# 指定输出路径
generator.generate_questionnaire(output_path='./output/问卷.xlsx')

# 批量输出到指定文件夹
generator.generate_batch_questionnaires(df, output_folder='./questionnaires')
```

**报告输出**：
```python
# 默认在 reports/ 目录生成
report_generator.generate_report(questionnaire_file='问卷.xlsx')

# 指定输出路径
report_generator.generate_report(
    questionnaire_file='问卷.xlsx',
    output_path='./output/报告.docx'
)
```

---

## 错误处理

### 常见错误及解决方案

#### 1. 指标文件不存在

**错误信息**：
```
FileNotFoundError: 指标体系文件不存在: ...
```

**解决方案**：
- 检查指标文件是否存在
- 使用自定义路径：`QuestionnaireGenerator(indicator_file='/path/to/file')`
- 确保文件名为 `指标体系.xlsx`

#### 2. 问卷文件不存在

**错误信息**：
```
FileNotFoundError: 问卷文件不存在: ...
```

**解决方案**：
- 检查问卷文件路径是否正确
- 确保问卷文件已生成
- 使用绝对路径

#### 3. 评分计算器不可用

**错误信息**：
```
[WARN] 无法导入默认的ScoreCalculator，某些功能可能不可用
```

**解决方案**：
- 确保 `score_calculator.py` 在项目根目录
- 显式传入计算器实例：
  ```python
  from score_calculator import ScoreCalculator
  calc = ScoreCalculator()
  gen = ProfessionalReportGenerator(score_calculator=calc)
  ```

#### 4. 权限错误

**错误信息**：
```
PermissionError: [Errno 13] Permission denied: ...
```

**解决方案**：
- 检查输出目录权限
- 确保输出目录存在且可写
- 关闭已打开的输出文件

---

## 最佳实践

### 1. 模块化使用

```python
# 分离问卷和报告生成
from survey_generator import QuestionnaireGenerator
from report_generator import ProfessionalReportGenerator

# 由不同的开发者维护
questionnaire_gen = QuestionnaireGenerator()
report_gen = ProfessionalReportGenerator()
```

### 2. 错误处理

```python
try:
    file = generator.generate_questionnaire(
        enterprise_name='示例企业'
    )
    print(f"成功: {file}")
except FileNotFoundError as e:
    print(f"文件错误: {e}")
except Exception as e:
    print(f"生成失败: {e}")
```

### 3. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    file = generator.generate_questionnaire()
    logger.info(f"问卷已生成: {file}")
except Exception as e:
    logger.error(f"生成失败: {e}")
```

### 4. 批量处理

```python
import pandas as pd
from survey_generator import QuestionnaireGenerator

# 读取企业列表
df = pd.read_excel('enterprises.xlsx')

# 生成问卷
generator = QuestionnaireGenerator()
files = generator.generate_batch_questionnaires(df)

# 处理结果
for file in files:
    print(f"已生成: {file}")
```

---

## 扩展开发

### 为问卷生成器添加新功能

```python
from survey_generator import QuestionnaireGenerator

class CustomQuestionnaireGenerator(QuestionnaireGenerator):
    """自定义问卷生成器"""
    
    def generate_with_template(self, template_name, **kwargs):
        """使用模板生成问卷"""
        # 自定义实现
        pass
```

### 为报告生成器添加新功能

```python
from report_generator import ProfessionalReportGenerator

class CustomReportGenerator(ProfessionalReportGenerator):
    """自定义报告生成器"""
    
    def generate_with_charts(self, questionnaire_file, **kwargs):
        """生成带图表的报告"""
        # 自定义实现
        pass
```

---

## 常见问题

### Q: 两个模块可以独立使用吗？

**A**: 是的，完全可以。
- 问卷生成模块完全独立
- 报告生成模块仅依赖评分计算器（可选）

### Q: 如何在多个项目中使用这些模块？

**A**: 有几种方式：
1. 复制模块文件夹到新项目
2. 将模块发布为Python包
3. 使用Git子模块

### Q: 支持自定义报告格式吗？

**A**: 支持，可以：
1. 继承 `ProfessionalReportGenerator` 类
2. 重写相关方法
3. 自定义报告内容和格式

### Q: 如何处理大量问卷生成？

**A**: 建议：
1. 使用批量生成方法
2. 考虑使用多线程/多进程
3. 定期清理临时文件

---

## 支持和反馈

如有问题或建议，请：
1. 检查本文档的相关部分
2. 查看代码中的注释和文档字符串
3. 查看错误日志和堆栈跟踪
4. 联系开发团队

---

## 版本历史

### v1.0.0 (2025-11-29)
- ✅ 初始版本
- ✅ 问卷生成模块独立
- ✅ 报告生成模块独立
- ✅ 完整的API文档

---

## 许可证

本模块遵循项目主许可证。

---

**最后更新**: 2025-11-29

