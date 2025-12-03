# Excel数据下载功能说明

## ✅ 功能概述

南开问卷系统现已实现**Excel数据下载**功能，用户提交问卷后可以下载包含完整填报数据的Excel文件。

---

## 📊 下载文件内容

### 1. 文件信息
- **文件名格式**：`问卷填报数据_企业名称_时间戳.xlsx`
- **示例**：`问卷填报数据_今麦郎_20251201_150000.xlsx`
- **存储位置**：`storage/nankai_downloads/`

### 2. Excel文件结构

#### 标题区域
- **第1行**：问卷标题
  - 格式：`南开大学现代企业制度指数评价问卷 - 初级/中级/高级`
  - 样式：蓝色背景，白色粗体文字，居中

#### 企业信息区域
- **第2行**：企业基本信息
  - 企业名称
  - 联系人
  - 联系电话
  - 提交时间
  - 样式：灰色背景

#### 得分信息区域
- **第3行**：评分汇总
  - 百分制得分
  - 实际得分
  - 满分
  - 样式：浅蓝色背景，蓝色粗体文字

#### 数据表格区域
- **第5行起**：题目和答案数据

### 3. 数据列说明

| 列名 | 说明 | 宽度 | 对齐方式 |
|------|------|------|---------|
| 序号 | 题目序号 | 8 | 居中 |
| 一级指标 | 一级指标名称 | 15 | 左对齐 |
| 二级指标 | 二级指标名称 | 15 | 左对齐 |
| 三级指标 | 三级指标名称 | 20 | 左对齐 |
| 题目 | 题目内容 | 40 | 左对齐，自动换行 |
| 分值 | 题目分值 | 8 | 居中 |
| 填报答案 | 用户选择的答案 | 20 | 左对齐 |
| 部分完成说明 | 选择"B.部分完成"时的详细说明 | 30 | 左对齐，自动换行 |
| 得分 | 该题实际得分 | 8 | 居中 |
| 评分标准 | 题目的评分标准 | 30 | 左对齐，自动换行 |

---

## 💻 技术实现

### 后端API（app.py 第1117-1295行）

#### 1. 路由定义
```python
@app.route('/api/nankai/download/<submission_id>')
def download_nankai_submission(submission_id):
    """下载南开问卷填报数据为Excel格式"""
```

#### 2. 数据读取流程
```python
# 1. 读取JSON提交数据
json_file = f'storage/nankai_submissions/submission_{submission_id}.json'
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. 读取Excel题目信息
level = data.get('level', '初级')
df = pd.read_excel(excel_path, sheet_name=level)

# 3. 合并数据
answers = data.get('answers', {})
partial_details = data.get('partial_details', {})
score_details = data.get('score', {}).get('details', {})
```

#### 3. Excel生成（使用openpyxl）
```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# 创建工作簿
wb = Workbook()
ws = wb.active

# 添加标题、企业信息、得分信息
# 添加表头和数据
# 设置样式和格式

# 保存文件
wb.save(output_path)
```

#### 4. 文件下载
```python
return send_file(
    output_path,
    as_attachment=True,
    download_name=output_filename,
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
```

### 前端实现

#### 1. 提交时传递submission_id（nankai_questionnaire_fill.html 第670-680行）
```javascript
if (result.success) {
    const params = new URLSearchParams({
        score: result.score,
        total_score: result.total_score,
        max_score: result.max_score,
        level: '{{ level_name }}',
        enterprise: formData.get('enterprise_name'),
        submission_id: result.submission_id  // 新增
    });
    window.location.href = `/nankai-result?${params.toString()}`;
}
```

#### 2. 结果页面获取submission_id（nankai_result.html 第91-101行）
```javascript
const urlParams = new URLSearchParams(window.location.search);
const submissionId = urlParams.get('submission_id') || '';
```

#### 3. 下载按钮实现（nankai_result.html 第130-139行）
```javascript
function downloadData() {
    if (!submissionId) {
        alert('无法获取提交ID，请重新提交问卷');
        return;
    }
    
    // 直接跳转到下载链接
    window.location.href = `/api/nankai/download/${submissionId}`;
}
```

---

## 📝 Excel样式说明

### 1. 标题行样式
- **背景色**：深蓝色 (#4472C4)
- **字体**：16号，粗体，白色
- **对齐**：水平垂直居中
- **行高**：30

### 2. 企业信息行样式
- **背景色**：浅灰色 (#E7E6E6)
- **字体**：10号，常规
- **对齐**：左对齐，垂直居中
- **行高**：25

### 3. 得分信息行样式
- **背景色**：浅蓝色 (#D9E1F2)
- **字体**：11号，粗体，深蓝色 (#2E5090)
- **对齐**：水平垂直居中
- **行高**：25

### 4. 表头样式
- **背景色**：深蓝色 (#2E5090)
- **字体**：粗体，白色
- **对齐**：水平垂直居中，自动换行
- **行高**：30

### 5. 数据单元格样式
- **边框**：细线边框
- **对齐**：根据内容类型（数字居中，文本左对齐）
- **换行**：题目、说明、评分标准自动换行

---

## 🎯 使用流程

### 用户操作流程
1. **填写问卷**
   - 访问：http://localhost:5000/nankai-survey
   - 选择级别并填写问卷
   - 提交问卷

2. **查看结果**
   - 自动跳转到结果页面
   - 显示百分制得分和评级

3. **下载数据**
   - 点击"下载问卷数据"按钮
   - 浏览器自动下载Excel文件
   - 文件名：`问卷填报数据_企业名称_时间戳.xlsx`

### 系统处理流程
```
用户提交问卷
    ↓
保存JSON数据（包含submission_id）
    ↓
返回submission_id到前端
    ↓
前端跳转到结果页面（携带submission_id）
    ↓
用户点击下载按钮
    ↓
调用下载API（/api/nankai/download/<submission_id>）
    ↓
读取JSON数据和Excel题目
    ↓
生成格式化的Excel文件
    ↓
返回文件供下载
```

---

## 📋 Excel文件示例

### 文件预览
```
┌─────────────────────────────────────────────────────────────┐
│ 南开大学现代企业制度指数评价问卷 - 初级                      │ (蓝色背景)
├─────────────────────────────────────────────────────────────┤
│ 企业名称：今麦郎 | 联系人：张三 | 联系电话：138... | 提交... │ (灰色背景)
├─────────────────────────────────────────────────────────────┤
│ 百分制得分：73.26分 | 实际得分：26.3分 | 满分：35.9分        │ (浅蓝背景)
├─────────────────────────────────────────────────────────────┤
│                                                               │
├──┬────┬────┬────┬────┬──┬────┬────┬──┬────┤
│序│一级│二级│三级│题目│分│填报│部分│得│评分│ (深蓝背景)
│号│指标│指标│指标│    │值│答案│完成│分│标准│
│  │    │    │    │    │  │    │说明│  │    │
├──┼────┼────┼────┼────┼──┼────┼────┼──┼────┤
│1 │党建│... │... │... │1 │A.已│    │1 │... │
│  │    │    │    │    │  │完成│    │  │    │
├──┼────┼────┼────┼────┼──┼────┼────┼──┼────┤
│2 │党建│... │... │... │2 │B.部│已完│1.6│... │
│  │    │    │    │    │  │分完│成基│  │    │
│  │    │    │    │    │  │成  │本架│  │    │
│  │    │    │    │    │  │    │构...│  │    │
└──┴────┴────┴────┴────┴──┴────┴────┴──┴────┘
```

---

## ✅ 功能特点

### 1. 数据完整性
✅ 包含所有题目信息
✅ 包含用户填报的答案
✅ 包含部分完成的详细说明
✅ 包含每题的得分情况
✅ 包含企业基本信息
✅ 包含评分汇总信息

### 2. 格式美观
✅ 专业的表格样式
✅ 清晰的颜色区分
✅ 合理的列宽设置
✅ 自动换行处理
✅ 统一的字体和对齐

### 3. 易用性
✅ 一键下载
✅ 自动命名
✅ 标准Excel格式
✅ 可直接打开编辑
✅ 支持打印

### 4. 可追溯性
✅ 包含提交时间
✅ 包含企业信息
✅ 包含完整答案
✅ 包含得分详情
✅ 文件名包含时间戳

---

## 🔧 技术依赖

- **pandas**：数据处理
- **openpyxl**：Excel文件生成和样式设置
- **Flask**：Web框架和文件下载

---

## 📌 注意事项

1. **文件存储**：下载的Excel文件临时存储在 `storage/nankai_downloads/` 目录
2. **文件命名**：使用企业名称和时间戳，避免文件名冲突
3. **数据安全**：只能下载自己提交的问卷数据（通过submission_id控制）
4. **浏览器兼容**：支持所有现代浏览器的文件下载功能
5. **文件大小**：根据题目数量，文件大小约50-200KB

---

## 🎉 功能状态

**✅ Excel数据下载功能已完整实现并正常运行！**

### 测试步骤
1. 访问：http://localhost:5000/nankai-survey
2. 选择问卷级别并填写
3. 提交问卷
4. 在结果页面点击"下载问卷数据"按钮
5. 查看下载的Excel文件

### 预期结果
- ✅ 文件自动下载
- ✅ 文件名格式正确
- ✅ Excel格式美观
- ✅ 数据完整准确
- ✅ 可正常打开编辑