# 审核功能说明文档

## 功能概述

本审核功能模块提供了完整的企业审核管理系统，包括：

1. **查看报告** - 查看详细的审核报告
2. **查看原问卷** - 查看企业填写的原始问卷数据
3. **手动晋级** - 允许审核员手动将企业升级到更高级别
4. **审核操作** - 批准或驳回审核
5. **统计分析** - 查看审核统计信息

## 文件结构

```
├── user_types_config.py      # 用户类型和分级配置
├── review_models.py          # 审核数据模型
├── review_service.py         # 审核业务逻辑服务
├── review_ui.py              # 审核UI界面（Tkinter）
├── review_demo.py            # 演示脚本
└── REVIEW_FEATURE_README.md  # 本文档
```

## 核心模块说明

### 1. review_models.py - 数据模型

定义了审核功能所需的所有数据结构：

#### QuestionnaireAnswer
```python
@dataclass
class QuestionnaireAnswer:
    question_id: str          # 问题ID
    question_text: str        # 问题文本
    question_type: str        # 题目类型（合规项、有效项、调节项）
    answer: str               # 答案
    score: Optional[float]    # 得分
    comment: Optional[str]    # 备注
```

#### QuestionnaireData
```python
@dataclass
class QuestionnaireData:
    questionnaire_id: str     # 问卷ID
    user_id: str              # 用户ID
    user_type: str            # 用户类型
    user_level: str           # 用户级别
    submission_time: datetime # 提交时间
    answers: List[...]        # 答案列表
    total_score: Optional[float]  # 总分
```

#### ReviewReport
```python
@dataclass
class ReviewReport:
    report_id: str            # 报告ID
    questionnaire_id: str     # 问卷ID
    user_id: str              # 用户ID
    user_name: str            # 用户名
    enterprise_name: str      # 企业名称
    current_level: str        # 当前级别
    
    # 评分
    compliance_score: float   # 合规项得分
    effectiveness_score: float # 有效项得分
    adjustment_score: Optional[float]  # 调节项得分
    total_score: float        # 总分
    
    # 审核信息
    review_status: ReviewStatus  # 审核状态
    reviewer_id: Optional[str]   # 审核员ID
    reviewer_name: Optional[str] # 审核员名称
    review_time: Optional[datetime]  # 审核时间
    review_comment: Optional[str]    # 审核意见
    
    # 晋级信息
    promotion_eligible: bool  # 是否符合晋级条件
    recommended_level: Optional[str]  # 推荐晋级级别
    promotion_reason: Optional[str]   # 晋级原因
```

#### PromotionRecord
```python
@dataclass
class PromotionRecord:
    promotion_id: str         # 晋级记录ID
    user_id: str              # 用户ID
    enterprise_name: str      # 企业名称
    from_level: str           # 晋级前级别
    to_level: str             # 晋级后级别
    promotion_type: str       # 晋级类型（automatic/manual）
    reviewer_id: str          # 审核员ID
    reviewer_name: str        # 审核员名称
    reason: str               # 晋级原因
    report_id: Optional[str]  # 关联报告ID
    promotion_time: datetime  # 晋级时间
```

### 2. review_service.py - 业务逻辑服务

提供了所有审核相关的业务逻辑操作：

#### 主要方法

**报告管理：**
- `create_review_report()` - 创建审核报告
- `get_review_report()` - 获取审核报告
- `get_reports_by_status()` - 按状态获取报告
- `get_pending_reviews()` - 获取待审核报告
- `get_reports_by_user()` - 获取用户的所有报告

**问卷管理：**
- `store_questionnaire()` - 存储问卷数据
- `get_questionnaire()` - 获取问卷数据
- `get_questionnaire_by_report()` - 通过报告获取问卷

**审核操作：**
- `submit_review()` - 提交审核结果
- `approve_review()` - 批准审核
- `reject_review()` - 驳回审核

**晋级操作：**
- `promote_user()` - 手动晋级用户
- `get_promotion_records()` - 获取晋级记录
- `get_promotion_record()` - 获取单条晋级记录

**统计分析：**
- `get_review_statistics()` - 获取审核统计
- `get_average_scores()` - 获取平均评分

### 3. review_ui.py - 用户界面

提供了完整的Tkinter UI界面：

#### ReviewDetailWindow - 审核详情窗口

包含四个标签页：

1. **查看报告** - 显示审核报告的详细信息
   - 基本信息（企业名称、联系人、级别等）
   - 评分信息（合规项、有效项、调节项、总分）
   - 晋级信息（是否符合条件、推荐级别、晋级原因）
   - 审核意见

2. **查看原问卷** - 显示企业填写的原始问卷
   - 问卷基本信息
   - 所有答案详情（问题、答案、得分、备注）
   - 树形视图展示，支持滚动

3. **审核操作** - 进行审核操作
   - 输入审核意见
   - 批准或驳回审核

4. **手动晋级** - 进行手动晋级操作
   - 显示晋级资格信息
   - 输入晋级原因
   - 确认晋级

#### ReviewListWindow - 审核列表窗口

- 显示所有审核报告的列表
- 支持按状态筛选（待审核、已批准、已驳回、已晋级、全部）
- 支持双击打开详情窗口
- 自动刷新功能

#### ReviewDashboard - 审核仪表板

- 显示审核统计信息
- 显示平均评分
- 快速访问审核列表

## 使用示例

### 基础使用

```python
from review_service import review_service
from review_models import ReportType

# 1. 存储问卷数据
answers = [
    {
        'question_id': 'q001',
        'question_text': '企业是否建立了党的组织？',
        'question_type': '合规项',
        'answer': '是',
        'score': 10.0
    },
    # ... 更多答案
]

questionnaire = review_service.store_questionnaire(
    questionnaire_id='qn_001',
    user_id='user_001',
    user_type='enterprise',
    user_level='beginner',
    answers=answers
)

# 2. 创建审核报告
report = review_service.create_review_report(
    questionnaire_id='qn_001',
    user_id='user_001',
    user_name='张三',
    enterprise_name='示例企业有限公司',
    current_level='beginner',
    compliance_score=20.0,
    effectiveness_score=8.0,
    adjustment_score=5.0,
    report_type=ReportType.REVIEW_REPORT
)

# 3. 批准审核
success, message, report = review_service.approve_review(
    report_id=report.report_id,
    reviewer_id='reviewer_001',
    reviewer_name='李四',
    comment='企业表现良好，符合晋级条件',
    user_type='enterprise'
)

# 4. 手动晋级
success, message, promotion_record = review_service.promote_user(
    report_id=report.report_id,
    reviewer_id='reviewer_001',
    reviewer_name='李四',
    reason='企业综合表现优秀，符合晋级标准',
    user_type='enterprise'
)

# 5. 查看原问卷
questionnaire = review_service.get_questionnaire_by_report(report.report_id)
for answer in questionnaire.answers:
    print(f"问题: {answer.question_text}")
    print(f"答案: {answer.answer}")
    print(f"得分: {answer.score}")

# 6. 查看报告
report = review_service.get_review_report(report.report_id)
print(f"企业: {report.enterprise_name}")
print(f"总分: {report.total_score}")
print(f"审核状态: {report.review_status.value}")

# 7. 获取统计信息
stats = review_service.get_review_statistics()
print(f"总报告数: {stats['total_reports']}")
print(f"批准率: {stats['approval_rate']:.2%}")
print(f"晋级率: {stats['promotion_rate']:.2%}")
```

### 启动UI界面

```python
import tkinter as tk
from review_ui import ReviewDashboard, ReviewListWindow

root = tk.Tk()
root.title("审核功能")
root.geometry("400x300")

# 打开仪表板
dashboard = ReviewDashboard(root)

# 或打开审核列表
review_list = ReviewListWindow(root)

root.mainloop()
```

### 运行演示

```bash
python review_demo.py
```

## 晋级规则

### 企业用户晋级规则

| 当前级别 | 晋级到 | 所需分数 |
|---------|--------|---------|
| 初级 (beginner) | 中级 (intermediate) | ≥ 70 分 |
| 中级 (intermediate) | 高级 (advanced) | ≥ 85 分 |
| 高级 (advanced) | - | 最高级 |

### 专家用户晋级规则

| 当前级别 | 晋级到 | 所需分数 |
|---------|--------|---------|
| 初级 (junior) | 中级 (intermediate) | ≥ 75 分 |
| 中级 (intermediate) | 高级 (senior) | ≥ 88 分 |
| 高级 (senior) | - | 最高级 |

## 审核状态流转

```
创建报告 (PENDING)
    ↓
审核员审核
    ├→ 批准 (APPROVED) → 可选：手动晋级 (PROMOTED)
    └→ 驳回 (REJECTED)
```

## 关键特性

### 1. 自动晋级资格判断
- 批准审核时自动检查是否符合晋级条件
- 根据总分和晋级阈值自动判断
- 推荐下一级别

### 2. 手动晋级
- 审核员可以手动晋级企业
- 需要填写晋级原因
- 自动检查是否已是最高级
- 生成晋级记录

### 3. 完整的审核追踪
- 记录审核员信息
- 记录审核时间
- 保存审核意见
- 维护晋级历史

### 4. 灵活的查询功能
- 按状态查询报告
- 按用户查询报告
- 查看晋级记录
- 统计分析

## 数据持久化

当前实现使用内存存储。如需持久化，可以：

1. **集成数据库**
   - 修改 `review_service.py` 中的存储方式
   - 使用 SQLAlchemy 或其他ORM

2. **集成文件存储**
   - 使用 JSON 或 CSV 格式保存数据
   - 实现序列化和反序列化

3. **集成缓存**
   - 使用 Redis 等缓存系统
   - 提高查询性能

## 扩展建议

1. **权限管理**
   - 添加角色权限控制
   - 限制不同审核员的操作权限

2. **工作流管理**
   - 支持多级审核
   - 添加审核队列管理

3. **通知系统**
   - 审核完成时发送通知
   - 晋级时发送通知

4. **报表导出**
   - 导出审核报告为PDF/Excel
   - 生成统计报表

5. **审计日志**
   - 记录所有操作
   - 支持操作回溯

## 常见问题

### Q: 如何修改晋级阈值？
A: 修改 `review_models.py` 中的 `ENTERPRISE_PROMOTION_THRESHOLDS` 和 `EXPERT_PROMOTION_THRESHOLDS`

### Q: 如何添加新的用户类型？
A: 修改 `user_types_config.py` 中的 `USER_TYPES` 和 `PROMOTION_CONFIG`

### Q: 如何集成到现有系统？
A: 导入 `review_service` 和相关模型，调用对应的方法即可

### Q: 如何处理并发操作？
A: 当前实现不支持并发，建议使用数据库事务或锁机制

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系开发团队。

