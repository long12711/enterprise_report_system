# 前端集成指南

## 概述

本指南说明如何在前端问卷页面中集成用户类型和分级功能。

---

## 页面结构

### HTML结构

```html
<!-- 用户类型和分级选择区域 -->
<div class="section">
    <h2 class="section-title">👤 用户类型和分级</h2>

    <!-- 用户类型选择 -->
    <div class="form-group">
        <label class="form-label required">用户类型</label>
        <select class="form-control" name="用户类型" id="userType" required onchange="onUserTypeChange()">
            <option value="">请选择用户类型</option>
            <option value="chamber_of_commerce">工商联用户</option>
            <option value="enterprise">企业用户</option>
            <option value="expert">专家用户</option>
        </select>
    </div>

    <!-- 用户分级选择 -->
    <div class="form-group">
        <label class="form-label required">用户分级</label>
        <select class="form-control" name="用户分级" id="userLevel" required onchange="onUserLevelChange()">
            <option value="">请先选择用户类型</option>
        </select>
    </div>

    <!-- 问卷说明 -->
    <div class="info-box" id="userTypeInfo" style="display: none;">
        <strong>问卷说明：</strong> <span id="userTypeDescription"></span>
    </div>
</div>
```

---

## JavaScript实现

### 1. 用户类型配置

```javascript
const userTypeConfig = {
    'chamber_of_commerce': {
        'name': '工商联用户',
        'levels': {
            'national': '国家级',
            'provincial': '省级',
            'municipal': '市级'
        }
    },
    'enterprise': {
        'name': '企业用户',
        'levels': {
            'advanced': '高级',
            'intermediate': '中级',
            'beginner': '初级'
        }
    },
    'expert': {
        'name': '专家用户',
        'levels': {
            'senior': '高级专家',
            'intermediate': '中级专家',
            'junior': '初级专家'
        }
    }
};
```

### 2. 用户类型改变事件处理

```javascript
function onUserTypeChange() {
    const userType = document.getElementById('userType').value;
    const userLevelSelect = document.getElementById('userLevel');
    
    if (!userType) {
        // 如果未选择用户类型，重置分级选择
        userLevelSelect.innerHTML = '<option value="">请先选择用户类型</option>';
        userLevelSelect.disabled = true;
        document.getElementById('userTypeInfo').style.display = 'none';
        document.getElementById('questionsContainer').innerHTML = '';
        return;
    }

    // 更新分级选项
    const levels = userTypeConfig[userType].levels;
    userLevelSelect.innerHTML = '<option value="">请选择分级</option>';
    
    Object.keys(levels).forEach(levelKey => {
        const option = document.createElement('option');
        option.value = levelKey;
        option.textContent = levels[levelKey];
        userLevelSelect.appendChild(option);
    });
    
    userLevelSelect.disabled = false;
    document.getElementById('questionsContainer').innerHTML = '';
}
```

### 3. 用户分级改变事件处理

```javascript
async function onUserLevelChange() {
    const userType = document.getElementById('userType').value;
    const userLevel = document.getElementById('userLevel').value;
    
    if (!userType || !userLevel) {
        return;
    }

    // 加载对应的问卷题目
    await loadQuestionsForUserType(userType, userLevel);
    
    // 显示问卷说明
    showUserTypeInfo(userType, userLevel);
}
```

### 4. 加载问卷题目

```javascript
async function loadQuestionsForUserType(userType, userLevel) {
    try {
        // 显示加载状态
        const container = document.getElementById('questionsContainer');
        container.innerHTML = '<div style="text-align: center; padding: 20px;"><span class="loading"></span> 加载问卷中...</div>';

        // 调用API获取题目
        const response = await fetch(`/api/get_questions?user_type=${userType}&user_level=${userLevel}`);
        const data = await response.json();

        if (data.success) {
            questionsData = data.questions;
            totalQuestions = questionsData.length;
            renderQuestions(questionsData);
            updateProgress();
        } else {
            showStatus('加载问卷失败：' + data.error, 'error');
        }
    } catch (error) {
        showStatus('加载问卷失败：' + error.message, 'error');
    }
}
```

### 5. 显示问卷说明

```javascript
function showUserTypeInfo(userType, userLevel) {
    const infoBox = document.getElementById('userTypeInfo');
    const descriptionSpan = document.getElementById('userTypeDescription');
    
    const descriptions = {
        'chamber_of_commerce': {
            'national': '国家级工商联评估问卷 - 全面评估，包含所有指标类型（合规项、有效项、调节项）',
            'provincial': '省级工商联评估问卷 - 重点评估，包含合规项和有效项',
            'municipal': '市级工商联评估问卷 - 基础评估，重点关注合规项和核心治理指标'
        },
        'enterprise': {
            'advanced': '企业高级自评问卷 - 全面自评，包含所有指标类型（合规项、有效项、调节项）',
            'intermediate': '企业中级自评问卷 - 标准自评，包含合规项和有效项',
            'beginner': '企业初级自评问卷 - 基础自评，重点关注合规项和核心治理指标'
        },
        'expert': {
            'senior': '高级专家评估问卷 - 深度评估，包含所有指标类型（合规项、有效项、调节项）',
            'intermediate': '中级专家评估问卷 - 标准评估，包含合规项和有效项',
            'junior': '初级专家评估问卷 - 基础评估，重点关注合规项和核心治理指标'
        }
    };
    
    descriptionSpan.textContent = descriptions[userType][userLevel] || '';
    infoBox.style.display = 'block';
}
```

### 6. 表单提交

```javascript
document.getElementById('questionnaireForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="loading"></span> 提交中...';

    try {
        // 收集表单数据
        const formData = new FormData(e.target);
        const data = {
            user_type: formData.get('用户类型'),
            user_level: formData.get('用户分级'),
            enterprise_info: {},
            answers: {}
        };

        // 收集企业信息
        const enterpriseFields = [
            '企业名称', '统一社会信用代码', '企业类型', '所属行业',
            '注册资本（万元）', '成立时间', '员工人数', '年营业收入（万元）',
            '联系人姓名', '联系人邮箱', '联系人电话'
        ];

        enterpriseFields.forEach(field => {
            data.enterprise_info[field] = formData.get(field);
        });

        // 收集问卷答案
        questionsData.forEach(question => {
            const answer = formData.get(`question_${question.sequence}`);
            if (answer) {
                data.answers[question.sequence] = answer;
            }
        });

        // 提交数据
        const response = await fetch('/api/submit_questionnaire', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showStatus('✅ 问卷提交成功！报告将通过邮件发送给您。', 'success');
            setTimeout(() => {
                window.location.href = '/success';
            }, 2000);
        } else {
            showStatus('❌ 提交失败：' + result.error, 'error');
            submitButton.disabled = false;
            submitButton.innerHTML = '✅ 提交问卷';
        }
    } catch (error) {
        showStatus('❌ 提交失败：' + error.message, 'error');
        submitButton.disabled = false;
        submitButton.innerHTML = '✅ 提交问卷';
    }
});
```

---

## 样式美化

### CSS样式

```css
/* 用户类型和分级选择区域 */
.section {
    margin-bottom: 40px;
    padding: 25px;
    background: #f9fafb;
    border-radius: 10px;
    border-left: 4px solid #2E5090;
}

.section-title {
    font-size: 20px;
    color: #2E5090;
    margin-bottom: 20px;
    font-weight: bold;
}

.form-group {
    margin-bottom: 20px;
}

.form-label {
    display: block;
    font-size: 14px;
    color: #333;
    margin-bottom: 8px;
    font-weight: 500;
}

.form-label.required::after {
    content: " *";
    color: red;
}

.form-control {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    transition: border-color 0.3s;
}

.form-control:focus {
    outline: none;
    border-color: #2E5090;
}

.info-box {
    background: #f0f7ff;
    border-left: 4px solid #2E5090;
    padding: 15px;
    margin: 20px 0;
    border-radius: 5px;
    font-size: 14px;
    line-height: 1.6;
}
```

---

## 用户交互流程

```
┌─────────────────────────────────────┐
│   页面加载                          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   显示用户类型选择下拉菜单          │
└────────────┬────────────────────────┘
             │
             ▼ 用户选择用户类型
┌─────────────────────────────────────┐
│   动态加载对应的分级选项            │
│   清空问卷题目区域                  │
└────────────┬────────────────────────┘
             │
             ▼ 用户选择分级
┌─────────────────────────────────────┐
│   调用API获取问卷题目               │
│   显示加载动画                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   渲染问卷题目                      │
│   显示问卷说明                      │
│   更新进度条                        │
└────────────┬────────────────────────┘
             │
             ▼ 用户填写问卷
┌─────────────────────────────────────┐
│   用户点击提交按钮                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   收集表单数据                      │
│   包括用户类型和分级                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   提交到后端API                     │
│   显示提交动画                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   成功提示                          │
│   跳转到成功页面                    │
└─────────────────────────────────────┘
```

---

## 测试检查清单

- [ ] 用户类型下拉菜单正常显示
- [ ] 选择用户类型后，分级选项正确更新
- [ ] 选择分级后，问卷题目正确加载
- [ ] 问卷说明文本正确显示
- [ ] 不同用户类型和分级的题目数量不同
- [ ] 问卷提交时，用户类型和分级信息被正确收集
- [ ] 后端正确接收用户类型和分级信息
- [ ] 报告生成时，包含用户类型和分级信息

---

## 常见问题

### Q1: 如何在页面加载时预选用户类型？

```javascript
// 在页面加载时设置默认值
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('userType').value = 'enterprise';
    onUserTypeChange();
});
```

### Q2: 如何禁用某些用户类型选项？

```javascript
// 在初始化时禁用某些选项
const userTypeSelect = document.getElementById('userType');
const options = userTypeSelect.querySelectorAll('option');
options.forEach(option => {
    if (option.value === 'expert') {
        option.disabled = true;
    }
});
```

### Q3: 如何在用户选择分级后立即验证？

```javascript
async function onUserLevelChange() {
    const userType = document.getElementById('userType').value;
    const userLevel = document.getElementById('userLevel').value;
    
    if (!userType || !userLevel) {
        showStatus('请选择用户类型和分级', 'error');
        return;
    }

    // 验证选择是否有效
    const response = await fetch(`/api/get_questions?user_type=${userType}&user_level=${userLevel}`);
    const data = await response.json();
    
    if (!data.success) {
        showStatus('无效的用户类型或分级组合', 'error');
        return;
    }

    // 继续加载问卷
    await loadQuestionsForUserType(userType, userLevel);
    showUserTypeInfo(userType, userLevel);
}
```

### Q4: 如何保存用户选择的用户类型和分级？

```javascript
// 保存到localStorage
function saveUserSelection() {
    const userType = document.getElementById('userType').value;
    const userLevel = document.getElementById('userLevel').value;
    
    localStorage.setItem('selectedUserType', userType);
    localStorage.setItem('selectedUserLevel', userLevel);
}

// 从localStorage恢复
function restoreUserSelection() {
    const userType = localStorage.getItem('selectedUserType');
    const userLevel = localStorage.getItem('selectedUserLevel');
    
    if (userType && userLevel) {
        document.getElementById('userType').value = userType;
        onUserTypeChange();
        
        // 等待分级选项加载后再设置
        setTimeout(() => {
            document.getElementById('userLevel').value = userLevel;
            onUserLevelChange();
        }, 100);
    }
}
```

---

## 性能优化建议

1. **缓存问卷题目**: 使用localStorage缓存已加载的问卷题目，避免重复请求
2. **延迟加载**: 只在用户选择分级后才加载问卷题目
3. **虚拟滚动**: 对于题目数量很多的问卷，使用虚拟滚动提高性能
4. **防抖处理**: 对用户选择事件进行防抖处理，避免频繁请求

---

## 无障碍设计

- 为所有表单控件添加标签
- 使用语义化的HTML元素
- 提供键盘导航支持
- 使用适当的颜色对比度
- 为动态内容提供ARIA标签

---

## 浏览器兼容性

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 总结

通过集成用户类型和分级功能，前端问卷页面能够：

✓ 为不同的用户提供定制化的问卷体验
✓ 根据用户选择动态加载相应的题目
✓ 提供清晰的问卷说明和指导
✓ 确保提交的数据包含完整的用户信息
✓ 提高用户体验和系统的可用性

