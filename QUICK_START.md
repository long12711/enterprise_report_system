# 快速开始指南

## 5分钟快速上手

### 第一步：理解系统架构

系统支持**三类用户**，每类用户有**三个分级**：

```
工商联用户
├── 国家级 (全面评估)
├── 省级 (重点评估)
└── 市级 (基础评估)

企业用户
├── 高级 (全面自评)
├── 中级 (标准自评)
└── 初级 (基础自评)

专家用户
├── 高级专家 (深度评估)
├── 中级专家 (标准评估)
└── 初级专家 (基础评估)
```

### 第二步：启动系统

```bash
# 进入项目目录
cd d:\Claude\ Code\enterprise_report_system

# 启动Flask应用
python app.py
```

系统将在 `http://localhost:5000` 启动

### 第三步：访问问卷页面

打开浏览器访问：
```
http://localhost:5000/questionnaire
```

### 第四步：填写问卷

1. **选择用户类型** - 从下拉菜单选择（工商联/企业/专家）
2. **选择分级** - 根据用户类型选择对应的分级
3. **查看问卷说明** - 系统会显示该分级的问卷说明
4. **填写企业信息** - 输入企业的基本信息
5. **回答问卷题目** - 根据题目类型选择答案
6. **提交问卷** - 点击提交按钮

### 第五步：查看报告

问卷提交后，系统会自动生成报告并通过邮件发送。

---

## 核心概念

### 1. 用户类型 (User Type)

| 类型 | 代码 | 描述 |
|------|------|------|
| 工商联用户 | chamber_of_commerce | 工商联及其下属机构 |
| 企业用户 | enterprise | 企业自评 |
| 专家用户 | expert | 专业评估机构/专家 |

### 2. 用户分级 (User Level)

#### 工商联用户
- `national` - 国家级
- `provincial` - 省级
- `municipal` - 市级

#### 企业用户
- `advanced` - 高级
- `intermediate` - 中级
- `beginner` - 初级

#### 专家用户
- `senior` - 高级专家
- `intermediate` - 中级专家
- `junior` - 初级专家

### 3. 问题类型 (Question Type)

| 类型 | 描述 |
|------|------|
| 合规项 | 企业必须满足的基本要求 |
| 有效项 | 企业应该实施的有效措施 |
| 调节项 | 特殊的否决性指标 |

---

## API快速参考

### 获取用户类型列表

```bash
curl http://localhost:5000/api/user-types
```

### 获取问卷题目

```bash
# 获取工商联国家级问卷
curl "http://localhost:5000/api/get_questions?user_type=chamber_of_commerce&user_level=national"

# 获取企业高级自评问卷
curl "http://localhost:5000/api/get_questions?user_type=enterprise&user_level=advanced"

# 获取所有题目（不过滤）
curl "http://localhost:5000/api/get_questions"
```

### 提交问卷

```bash
curl -X POST http://localhost:5000/api/submit_questionnaire \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "enterprise",
    "user_level": "advanced",
    "enterprise_info": {
      "企业名称": "示例企业",
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
      "3": "不适用"
    }
  }'
```

---

## 常见场景

### 场景1：工商联国家级评估

```javascript
// 1. 用户选择"工商联用户"
// 2. 系统显示分级选项：国家级、省级、市级
// 3. 用户选择"国家级"
// 4. 系统加载全部题目（包括合规项、有效项、调节项）
// 5. 用户填写问卷并提交
// 6. 系统生成全面评估报告
```

### 场景2：企业初级自评

```javascript
// 1. 用户选择"企业用户"
// 2. 系统显示分级选项：高级、中级、初级
// 3. 用户选择"初级"
// 4. 系统加载基础题目（仅合规项，重点领域）
// 5. 用户填写问卷并提交
// 6. 系统生成基础自评报告
```

### 场景3：专家中级评估

```javascript
// 1. 用户选择"专家用户"
// 2. 系统显示分级选项：高级专家、中级专家、初级专家
// 3. 用户选择"中级专家"
// 4. 系统加载标准题目（合规项和有效项）
// 5. 用户填写问卷并提交
// 6. 系统生成标准评估报告
```

---

## 文件结构

```
enterprise_report_system/
├── app.py                          # 主应用程序
├── user_types_config.py            # 用户类型和分级配置
├── templates/
│   └── questionnaire.html          # 问卷页面
├── static/
│   ├── css/                        # 样式文件
│   └── js/                         # JavaScript文件
├── submissions/                    # 问卷提交数据
├── reports/                        # 生成的报告
├── 指标体系.xlsx                   # 问卷题目数据
├── USER_TYPES_GUIDE.md             # 用户类型指南
├── API_DOCUMENTATION.md            # API文档
├── FRONTEND_INTEGRATION_GUIDE.md   # 前端集成指南
└── QUICK_START.md                  # 本文件
```

---

## 配置文件说明

### user_types_config.py

定义了用户类型、分级和问卷配置：

```python
USER_TYPES = {
    'chamber_of_commerce': {
        'name': '工商联用户',
        'levels': {
            'national': {'name': '国家级', 'value': 1},
            'provincial': {'name': '省级', 'value': 2},
            'municipal': {'name': '市级', 'value': 3}
        }
    },
    # ...
}

USER_TYPE_QUESTION_MAPPING = {
    'chamber_of_commerce': {
        'national': {
            'description': '国家级工商联评估问卷 - 全面评估',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业']
        },
        # ...
    }
}
```

---

## 故障排除

### 问题1：问卷页面不显示用户类型选择

**原因**: 前端JavaScript未正确加载

**解决方案**:
1. 检查浏览器控制台是否有错误
2. 确保 `questionnaire.html` 文件已更新
3. 清除浏览器缓存并刷新页面

### 问题2：选择分级后没有加载题目

**原因**: 后端API返回错误或网络问题

**解决方案**:
1. 检查后端是否正常运行
2. 查看浏览器网络标签，检查API请求是否成功
3. 查看后端日志是否有错误信息

### 问题3：提交问卷时报错"必须选择用户类型和分级"

**原因**: 表单中未包含用户类型和分级信息

**解决方案**:
1. 确保在提交前选择了用户类型和分级
2. 检查前端代码是否正确收集了这两个字段

### 问题4：报告生成失败

**原因**: 邮件配置错误或Excel文件格式问题

**解决方案**:
1. 检查邮件配置是否正确
2. 查看后端日志中的错误信息
3. 确保 `指标体系.xlsx` 文件存在且格式正确

---

## 下一步

-[object Object]阅读 [USER_TYPES_GUIDE.md](USER_TYPES_GUIDE.md) 了解详细的用户类型和分级体系
- 📚 阅读 [API_DOCUMENTATION.md](API_DOCUMENTATION.md) 了解所有API端点
- 💻 阅读 [FRONTEND_INTEGRATION_GUIDE.md](FRONTEND_INTEGRATION_GUIDE.md) 了解前端集成细节
- 🧪 运行 `python test_user_types.py` 测试用户类型配置

---

## 获取帮助

如有问题，请：

1. 查看相关文档
2. 检查浏览器控制台和后端日志
3. 查看 [API_DOCUMENTATION.md](API_DOCUMENTATION.md) 中的错误处理部分
4. 联系系统管理员

---

## 总结

✅ 系统支持三类用户和多个分级
✅ 根据用户类型和分级动态加载问卷题目
✅ 提供完整的API接口
✅ 自动生成和发送报告
✅ 易于扩展和定制

祝您使用愉快！

