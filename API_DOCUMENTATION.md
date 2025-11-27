# 问卷系统API文档

## 基础信息

- **基础URL**: `http://localhost:5000`
- **请求格式**: JSON
- **响应格式**: JSON

---

## API端点列表

### 1. 获取用户类型和分级信息

#### 请求

```
GET /api/user-types
```

#### 描述

获取系统中所有可用的用户类型和对应的分级信息。

#### 参数

无

#### 响应

**成功响应 (200)**:

```json
{
    "success": true,
    "user_types": [
        {
            "value": "chamber_of_commerce",
            "name": "工商联用户",
            "description": "工商联及其下属机构",
            "levels": [
                {
                    "value": "national",
                    "name": "国家级"
                },
                {
                    "value": "provincial",
                    "name": "省级"
                },
                {
                    "value": "municipal",
                    "name": "市级"
                }
            ]
        },
        {
            "value": "enterprise",
            "name": "企业用户",
            "description": "企业自评",
            "levels": [
                {
                    "value": "advanced",
                    "name": "高级"
                },
                {
                    "value": "intermediate",
                    "name": "中级"
                },
                {
                    "value": "beginner",
                    "name": "初级"
                }
            ]
        },
        {
            "value": "expert",
            "name": "专家用户",
            "description": "专业评估机构/专家",
            "levels": [
                {
                    "value": "senior",
                    "name": "高级专家"
                },
                {
                    "value": "intermediate",
                    "name": "中级专家"
                },
                {
                    "value": "junior",
                    "name": "初级专家"
                }
            ]
        }
    ]
}
```

**错误响应**:

```json
{
    "success": false,
    "error": "错误信息"
}
```

#### 使用示例

```javascript
// JavaScript
fetch('/api/user-types')
    .then(response => response.json())
    .then(data => {
        console.log(data.user_types);
    });
```

---

### 2. 获取问卷题目

#### 请求

```
GET /api/get_questions?user_type={user_type}&user_level={user_level}
```

#### 描述

获取问卷题目。支持按用户类型和分级过滤题目。

#### 参数

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| user_type | string | 否 | 用户类型 (chamber_of_commerce, enterprise, expert) |
| user_level | string | 否 | 用户分级 (national, provincial, municipal, advanced, intermediate, beginner, senior, junior) |

#### 响应

**成功响应 (200)**:

```json
{
    "success": true,
    "questions": [
        {
            "sequence": 1,
            "level1": "党建引领",
            "level2": "组织建设",
            "question": "党组织是否依法依规建立（有三名以上正式党员、条件成熟的企业，要单独建立党的组织；暂不具备单独组建党组织条件的，可联合组建区域性党组织、行业性党组织，实现党的组织覆盖。）",
            "question_type": "合规项",
            "base_score": 0.5,
            "applicable_enterprises": "所有企业"
        },
        {
            "sequence": 2,
            "level1": "党建引领",
            "level2": "组织建设",
            "question": "企业党组织是否按要求执行党的组织生活制度",
            "question_type": "合规项",
            "base_score": 0.5,
            "applicable_enterprises": "所有企业"
        }
    ],
    "user_type": "chamber_of_commerce",
    "user_level": "national"
}
```

**错误响应**:

```json
{
    "success": false,
    "error": "获取问卷题目失败: 错误信息"
}
```

#### 使用示例

```javascript
// 获取工商联国家级问卷
fetch('/api/get_questions?user_type=chamber_of_commerce&user_level=national')
    .then(response => response.json())
    .then(data => {
        console.log(`获取了 ${data.questions.length} 道题目`);
    });

// 获取企业高级自评问卷
fetch('/api/get_questions?user_type=enterprise&user_level=advanced')
    .then(response => response.json())
    .then(data => {
        console.log(`获取了 ${data.questions.length} 道题目`);
    });

// 获取所有题目（不过滤）
fetch('/api/get_questions')
    .then(response => response.json())
    .then(data => {
        console.log(`获取了 ${data.questions.length} 道题目`);
    });
```

---

### 3. 提交问卷

#### 请求

```
POST /api/submit_questionnaire
Content-Type: application/json
```

#### 描述

提交问卷答案。系统会自动生成报告并通过邮件发送。

#### 请求体

```json
{
    "user_type": "chamber_of_commerce",
    "user_level": "national",
    "enterprise_info": {
        "企业名称": "示例企业有限公司",
        "统一社会信用代码": "91110000123456789X",
        "企业类型": "有限责任公司",
        "所属行业": "制造业",
        "注册资本（万元）": 1000,
        "成立时间": "2020-01-01",
        "员工人数": 100,
        "年营业收入（万元）": 5000,
        "联系人姓名": "张三",
        "联系人邮箱": "zhangsan@example.com",
        "联系人电话": "13800138000"
    },
    "answers": {
        "1": "是",
        "2": "否",
        "3": "不适用",
        "4": "很有效",
        "5": "比较有效"
    }
}
```

#### 参数说明

| 字段 | 类型 | 必需 | 描述 |
|------|------|------|------|
| user_type | string | 是 | 用户类型 |
| user_level | string | 是 | 用户分级 |
| enterprise_info | object | 是 | 企业基本信息 |
| answers | object | 是 | 问卷答案，key为题目序号，value为答案 |

#### 响应

**成功响应 (200)**:

```json
{
    "success": true,
    "message": "问卷提交成功，报告将通过邮件发送",
    "enterprise_name": "示例企业有限公司",
    "user_type": "chamber_of_commerce",
    "user_level": "national"
}
```

**错误响应**:

```json
{
    "success": false,
    "error": "提交失败: 错误信息"
}
```

#### 使用示例

```javascript
// JavaScript
const data = {
    user_type: 'enterprise',
    user_level: 'advanced',
    enterprise_info: {
        企业名称: '示例企业',
        统一社会信用代码: '91110000123456789X',
        // ... 其他企业信息
    },
    answers: {
        1: '是',
        2: '否',
        // ... 其他答案
    }
};

fetch('/api/submit_questionnaire', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log('问卷提交成功');
    } else {
        console.error('提交失败:', result.error);
    }
});
```

---

## 数据类型说明

### 用户类型 (user_type)

| 值 | 名称 | 描述 |
|---|------|------|
| chamber_of_commerce | 工商联用户 | 工商联及其下属机构 |
| enterprise | 企业用户 | 企业自评 |
| expert | 专家用户 | 专业评估机构/专家 |

### 用户分级 (user_level)

#### 工商联用户分级

| 值 | 名称 | 描述 |
|---|------|------|
| national | 国家级 | 国家级工商联 |
| provincial | 省级 | 省级工商联 |
| municipal | 市级 | 市级工商联 |

#### 企业用户分级

| 值 | 名称 | 描述 |
|---|------|------|
| advanced | 高级 | 高级企业自评 |
| intermediate | 中级 | 中级企业自评 |
| beginner | 初级 | 初级企业自评 |

#### 专家用户分级

| 值 | 名称 | 描述 |
|---|------|------|
| senior | 高级专家 | 高级专家评估 |
| intermediate | 中级专家 | 中级专家评估 |
| junior | 初级专家 | 初级专家评估 |

### 指标类型 (question_type)

| 值 | 名称 | 描述 |
|---|------|------|
| 合规项 | 合规类 | 企业必须满足的基本要求 |
| 有效项 | 有效性类 | 企业应该实施的有效措施 |
| 调节项 | 一票否决类 | 特殊的否决性指标 |

### 问卷答案

根据题目类型，答案可以是以下值之一：

**合规项/调节项答案**:
- "是"
- "否"
- "不适用"

**有效项答案**:
- "很有效"
- "比较有效"
- "一般"
- "不太有效"
- "完全无效"
- "不适用"

---

## 错误处理

### 常见错误

| 错误代码 | 错误信息 | 原因 |
|---------|---------|------|
| 400 | 数据格式错误 | 请求体格式不正确 |
| 400 | 必须选择用户类型和分级 | 缺少user_type或user_level |
| 500 | 获取问卷题目失败 | 服务器内部错误 |
| 500 | 提交失败 | 服务器内部错误 |

### 错误响应示例

```json
{
    "success": false,
    "error": "必须选择用户类型和分级"
}
```

---

## 速率限制

目前没有速率限制。

---

## 版本历史

### v1.0 (2025-11-23)

- 初始版本
- 支持三类用户和分级体系
- 支持按用户类型和分级过滤问卷题目
- 支持问卷提交和报告生成

---

## 联系方式

如有问题，请联系系统管理员。

