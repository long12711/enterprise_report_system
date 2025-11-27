# 问卷系统用户类型和分级指南

## 概述

本系统支持三类用户，每类用户都有不同的分级体系，对应不同的问卷题目和评估标准。

## 用户类型和分级体系

### 1. 工商联用户 (chamber_of_commerce)

**描述**: 工商联及其下属机构

**分级体系**:
- **国家级** (national): 国家级工商联评估
- **省级** (provincial): 省级工商联评估  
- **市级** (municipal): 市级工商联评估

**问卷特点**:
- **国家级**: 全面评估，包含所有指标类型（合规项、有效项、调节项）
- **省级**: 重点评估，包含合规项和有效项
- **市级**: 基础评估，重点关注合规项和核心治理指标

---

### 2. 企业用户 (enterprise)

**描述**: 企业自评

**分级体系**:
- **高级** (advanced): 高级企业自评
- **中级** (intermediate): 中级企业自评
- **初级** (beginner): 初级企业自评

**问卷特点**:
- **高级**: 全面自评，包含所有指标类型（合规项、有效项、调节项）
- **中级**: 标准自评，包含合规项和有效项
- **初级**: 基础自评，重点关注合规项和核心治理指标

---

### 3. 专家用户 (expert)

**描述**: 专业评估机构/专家

**分级体系**:
- **高级专家** (senior): 高级专家评估
- **中级专家** (intermediate): 中级专家评估
- **初级专家** (junior): 初级专家评估

**问卷特点**:
- **高级专家**: 深度评估，包含所有指标类型（合规项、有效项、调节项）
- **中级专家**: 标准评估，包含合规项和有效项
- **初级专家**: 基础评估，重点关注合规项和核心治理指标

---

## 问卷题目映射规则

### 指标类型分类

1. **合规项** (合规类): 企业必须满足的基本要求
2. **有效项** (有效性类): 企业应该实施的有效措施
3. **调节项** (一票否决类): 特殊的否决性指标

### 分级对应的题目范围

| 用户类型 | 分级 | 合规项 | 有效项 | 调节项 | 重点领域 |
|---------|------|--------|--------|--------|---------|
| 工商联 | 国家级 | ✓ | ✓ | ✓ | 全部 |
| 工商联 | 省级 | ✓ | ✓ | ✗ | 全部 |
| 工商联 | 市级 | ✓ | ✗ | ✗ | 党建、产权、治理、民主管理 |
| 企业 | 高级 | ✓ | ✓ | ✓ | 全部 |
| 企业 | 中级 | ✓ | ✓ | ✗ | 全部 |
| 企业 | 初级 | ✓ | ✗ | ✗ | 党建、产权、治理、民主管理 |
| 专家 | 高级 | ✓ | ✓ | ✓ | 全部 |
| 专家 | 中级 | ✓ | ✓ | ✗ | 全部 |
| 专家 | 初级 | ✓ | ✗ | ✗ | 党建、产权、治理、民主管理 |

---

## 前端使用流程

### 1. 用户选择流程

```
页面加载
  ↓
用户选择"用户类型"（下拉菜单）
  ↓
系统动态加载对应的"用户分级"选项
  ↓
用户选择"用户分级"
  ↓
系统加载对应的问卷题目
  ↓
显示问卷说明信息
```

### 2. 前端代码示例

```html
<!-- 用户类型选择 -->
<select name="用户类型" id="userType" onchange="onUserTypeChange()">
    <option value="">请选择用户类型</option>
    <option value="chamber_of_commerce">工商联用户</option>
    <option value="enterprise">企业用户</option>
    <option value="expert">专家用户</option>
</select>

<!-- 用户分级选择 -->
<select name="用户分级" id="userLevel" onchange="onUserLevelChange()">
    <option value="">请先选择用户类型</option>
</select>
```

### 3. JavaScript处理

```javascript
// 用户类型改变时，更新分级选项
function onUserTypeChange() {
    const userType = document.getElementById('userType').value;
    // 根据userType加载对应的分级选项
}

// 用户分级改变时，加载对应的问卷题目
async function onUserLevelChange() {
    const userType = document.getElementById('userType').value;
    const userLevel = document.getElementById('userLevel').value;
    // 调用API加载问卷题目
    const response = await fetch(`/api/get_questions?user_type=${userType}&user_level=${userLevel}`);
}
```

---

## 后端API接口

### 1. 获取用户类型和分级信息

**端点**: `GET /api/user-types`

**响应示例**:
```json
{
    "success": true,
    "user_types": [
        {
            "value": "chamber_of_commerce",
            "name": "工商联用户",
            "description": "工商联及其下属机构",
            "levels": [
                {"value": "national", "name": "国家级"},
                {"value": "provincial", "name": "省级"},
                {"value": "municipal", "name": "市级"}
            ]
        },
        ...
    ]
}
```

### 2. 获取问卷题目（支持按用户类型和分级过滤）

**端点**: `GET /api/get_questions?user_type={user_type}&user_level={user_level}`

**参数**:
- `user_type` (可选): 用户类型 (chamber_of_commerce, enterprise, expert)
- `user_level` (可选): 用户分级 (national, provincial, municipal, advanced, intermediate, beginner, senior, junior)

**响应示例**:
```json
{
    "success": true,
    "questions": [
        {
            "sequence": 1,
            "level1": "党建引领",
            "level2": "组织建设",
            "question": "党组织是否依法依规建立...",
            "question_type": "合规项",
            "base_score": 0.5,
            "applicable_enterprises": "所有企业"
        },
        ...
    ],
    "user_type": "chamber_of_commerce",
    "user_level": "national"
}
```

### 3. 提交问卷

**端点**: `POST /api/submit_questionnaire`

**请求体**:
```json
{
    "user_type": "chamber_of_commerce",
    "user_level": "national",
    "enterprise_info": {
        "企业名称": "...",
        "联系人邮箱": "...",
        ...
    },
    "answers": {
        "1": "是",
        "2": "否",
        ...
    }
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "问卷提交成功，报告将通过邮件发送",
    "enterprise_name": "...",
    "user_type": "chamber_of_commerce",
    "user_level": "national"
}
```

---

## 数据模型

### 用户类型配置 (user_types_config.py)

```python
USER_TYPES = {
    'chamber_of_commerce': {
        'name': '工商联用户',
        'description': '工商联及其下属机构',
        'levels': {
            'national': {'name': '国家级', 'value': 1},
            'provincial': {'name': '省级', 'value': 2},
            'municipal': {'name': '市级', 'value': 3}
        }
    },
    ...
}

USER_TYPE_QUESTION_MAPPING = {
    'chamber_of_commerce': {
        'national': {
            'description': '国家级工商联评估问卷 - 全面评估',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业']
        },
        ...
    }
}
```

---

## 题目过滤逻辑

系统根据以下规则过滤问卷题目：

1. **问题类型过滤**: 只包含配置中允许的问题类型
2. **适用对象过滤**: 检查题目是否适用于所有企业或特定企业类型
3. **重点领域过滤**: 对于非全面评估的分级，只包含指定的重点领域题目

### 过滤函数

```python
def filter_questions_by_user_type(questions, user_type, user_level):
    """根据用户类型和分级过滤问卷题目"""
    config = get_questionnaire_config(user_type, user_level)
    
    filtered_questions = []
    for question in questions:
        # 检查问题类型
        if question['question_type'] not in config['question_types']:
            continue
        
        # 检查适用对象
        applicable = question['applicable_enterprises']
        if applicable not in config['applicable_enterprises'] and '所有企业' not in config['applicable_enterprises']:
            continue
        
        # 检查重点领域
        if not config['include_all'] and 'focus_areas' in config:
            if question['level1'] not in config['focus_areas']:
                continue
        
        filtered_questions.append(question)
    
    return filtered_questions
```

---

## 测试

### 运行测试脚本

```bash
python test_user_types.py
```

### 测试内容

1. 获取所有用户类型
2. 获取每个用户类型的分级
3. 获取每个用户类型和分级的问卷配置

---

## 常见问题

### Q1: 如何添加新的用户类型？

编辑 `user_types_config.py` 文件，在 `USER_TYPES` 字典中添加新的用户类型，然后在 `USER_TYPE_QUESTION_MAPPING` 中定义其问卷配置。

### Q2: 如何修改某个分级的问卷题目范围？

编辑 `user_types_config.py` 文件中的 `USER_TYPE_QUESTION_MAPPING`，修改对应分级的 `question_types` 和 `focus_areas` 配置。

### Q3: 如何自定义问卷说明文本？

在前端 `questionnaire.html` 的 `showUserTypeInfo` 函数中修改 `descriptions` 对象。

### Q4: 系统如何处理没有指定用户类型的请求？

如果没有指定 `user_type` 和 `user_level` 参数，系统会返回所有题目。

---

## 总结

该系统通过用户类型和分级机制，为不同的评估主体提供定制化的问卷体验，确保：

- ✓ **工商联用户**: 能够按照不同级别进行全面或重点评估
- ✓ **企业用户**: 能够根据自身能力进行自评
- ✓ **专家用户**: 能够进行专业的深度评估

所有题目都基于"南开大学-现代企业制度指数评价体系"，确保评估的科学性和规范性。

