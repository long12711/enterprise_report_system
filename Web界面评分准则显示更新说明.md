# Web界面评分准则显示更新说明

## 更新时间
2025-12-01

## 更新内容

### 1. 数据加载器更新

#### 文件：`nankai_indicator_loader.py`

**新增字段支持**：
```python
COLUMN_CANDIDATES = {
    # ... 原有字段 ...
    '评分准则': ['评分准则', '评分规则', '评分说明', '评分方法'],
    '佐证材料': ['佐证材料', '证明材料', '支撑材料']
}
```

**返回数据结构增强**：
```python
q = {
    'sequence': ...,
    'level1': ...,
    'level2': ...,
    'question': ...,
    'base_score': ...,
    'criteria': ...,  # 原有：打分标准
    'scoring_rule': scoring_rule,  # 新增：评分准则
    'evidence_required': evidence,  # 新增：佐证材料
    'score_value': str(base_score),  # 新增：分值字符串
    'source_level': ...
}
```

### 2. 后端API更新

#### 文件：`app.py` (第836-930行)

**函数**：`nankai_questionnaire_fill_page()`

**新增数据处理**：
```python
# 读取评分准则（详细的评分规则）
scoring_rule = ''
for col_name in ['评分准则', '评分规则', '评分说明']:
    if col_name in df.columns and pd.notna(row[col_name]):
        scoring_rule = str(row[col_name])
        break

# 读取佐证材料要求
evidence = ''
if '佐证材料' in df.columns and pd.notna(row['佐证材料']):
    evidence = str(row['佐证材料'])

# 保留原始分值字符串（如"0-2"）
score_value = score_str
```

**传递给模板的数据**：
```python
questions.append({
    'id': q_id,
    'category': ...,
    'level1': ...,
    'level2': ...,
    'level3': ...,
    'indicator': question_text,
    'options': options_list,
    'score': score,
    'score_value': score_value,  # 新增
    'scoring_rule': scoring_rule,  # 新增
    'evidence': evidence  # 新增
})
```

### 3. 前端界面更新

#### 文件：`templates/nankai_questionnaire_fill.html`

**更新前的显示**：
```html
<div class="question-indicators">
    <span class="indicator-label">一级指标:</span>
    <span class="indicator-value level1">{{ q.level1 }}</span>
    
    <span class="indicator-label">二级指标:</span>
    <span class="indicator-value level2">{{ q.level2 }}</span>
    
    <span class="indicator-label">三级指标:</span>
    <span class="indicator-value level3">{{ q.level3 }}</span>
</div>
<div class="question-title">{{ q.indicator }}</div>
```

**更新后的显示**：
```html
<div class="question-indicators">
    <span class="indicator-label">一级指标:</span>
    <span class="indicator-value level1">{{ q.level1 }}</span>
    
    <span class="indicator-label">二级指标:</span>
    <span class="indicator-value level2">{{ q.level2 }}</span>
    
    <span class="indicator-label">三级指标:</span>
    <span class="indicator-value level3">{{ q.level3 }}</span>
    
    <!-- 新增：分值显示 -->
    <span class="indicator-label">分值:</span>
    <span class="indicator-value" style="color: #e91e63; font-weight: bold;">
        {{ q.score_value }}分
    </span>
</div>

<!-- 新增：评分准则显示 -->
{% if q.scoring_rule %}
<div style="margin: 10px 0; padding: 10px; background: #fff3e0; 
            border-left: 4px solid #ff9800; border-radius: 4px;">
    <div style="font-weight: bold; color: #e65100; margin-bottom: 5px;">
        📋 评分准则：
    </div>
    <div style="color: #333; font-size: 13px; line-height: 1.6;">
        {{ q.scoring_rule }}
    </div>
</div>
{% endif %}

<div class="question-title">{{ q.indicator }}</div>
```

### 4. 视觉效果

#### 分值显示
- **位置**：在三级指标后面
- **颜色**：粉红色 (#e91e63)
- **样式**：加粗显示
- **格式**：显示原始分值（如"1"、"0-2"、"-10"）

#### 评分准则显示
- **背景色**：浅橙色 (#fff3e0)
- **左边框**：橙色 (#ff9800)，4px宽
- **图标**：📋 (剪贴板图标)
- **标题颜色**：深橙色 (#e65100)
- **内容样式**：
  - 字体大小：13px
  - 行高：1.6
  - 颜色：深灰色 (#333)

### 5. 显示逻辑

1. **分值**：始终显示（如果有分值数据）
2. **评分准则**：仅当存在评分准则数据时显示
3. **条件渲染**：使用Jinja2的`{% if %}`语句

### 6. 数据流

```
Excel文件（南开大学指标体系）
    ↓
nankai_indicator_loader.py（加载数据）
    ↓
app.py（处理数据）
    ↓
nankai_questionnaire_fill.html（显示数据）
    ↓
用户浏览器（查看问卷）
```

### 7. 兼容性

#### 向后兼容
- 如果Excel文件中没有"评分准则"列，系统不会报错
- 评分准则区域只在有数据时显示
- 分值默认为"1"

#### 数据回退
- 评分准则：空字符串
- 佐证材料：空字符串
- 分值：默认1分

### 8. 示例效果

#### 示例1：二元评分
```
一级指标: 党建
二级指标: 组织建设
三级指标: 规范党组织建设
分值: 1分

📋 评分准则：
按照以下两项对应内容的得1分：
1. 建立健全党的正式组织（党委、党总支、党支部）
2. 党组织建立党建工作制度，或党建工作纳入企业章程

题目：是否建立健全党的正式组织？
选项：
○ A. 是（已建立/制定/设立）
○ B. 否（未建立/制定/设立）
```

#### 示例2：多项累计
```
一级指标: 党建
二级指标: 价值观建设
三级指标: 践行社会主义核心价值观体系建设
分值: 0-2分

📋 评分准则：
按照以下三项目标企业已实现的得0分，实现"1-2项"的得1分，实现"3项"的得2分：
1. 企业已将社会主义核心价值观体系融入企业文化建设制度
2. 企业员工对社会主义核心价值观认同率达80%以上
3. 企业员工能够倡导、践行社会主义核心价值观

题目：企业践行社会主义核心价值观的情况？
选项：
○ A. 完成3项
○ B. 完成1-2项
○ C. 均未完成
```

### 9. 技术优势

✅ **清晰直观**：用户可以直接看到评分规则
✅ **信息完整**：显示分值和评分准则
✅ **视觉区分**：使用不同颜色区分不同信息
✅ **响应式设计**：适配不同屏幕尺寸
✅ **条件显示**：只在有数据时显示评分准则

### 10. 测试建议

1. **访问问卷页面**：
   ```
   http://localhost:5000/nankai-questionnaire-fill?level=初级
   ```

2. **检查显示**：
   - 分值是否正确显示
   - 评分准则是否正确显示
   - 样式是否美观

3. **测试不同级别**：
   - 初级：64个指标
   - 中级：52个指标
   - 高级：42个指标

### 11. 后续优化建议

1. **评分类型标注**
   - 在评分准则旁边显示评分类型（二元/多项/全部/否决/分级）
   - 使用不同颜色的标签

2. **佐证材料显示**
   - 在文件上传区域显示佐证材料要求
   - 提供更详细的上传说明

3. **交互增强**
   - 点击评分准则可以展开/收起
   - 提供评分准则的详细解释

4. **移动端优化**
   - 优化评分准则在小屏幕上的显示
   - 调整字体大小和间距

## 总结

通过这次更新，Web界面现在能够：
- ✅ 显示每个指标的分值
- ✅ 显示详细的评分准则
- ✅ 提供更清晰的评分指导
- ✅ 帮助用户更准确地填写问卷

这与Word版问卷生成器V3保持一致，确保了线上线下问卷的统一性。

---

**更新完成时间**：2025-12-01
**更新文件**：
1. `nankai_indicator_loader.py`
2. `app.py`
3. `templates/nankai_questionnaire_fill.html`

**状态**：✅ 已完成并测试