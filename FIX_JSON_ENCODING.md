# Flask JSON 中文编码问题修复

## 问题描述

当访问企业门户时，如果出现错误（如 404 页面不存在），API 返回的错误消息中的中文被转义为 Unicode 转义序列（如 `\u9875\u9762\u4e0d\u5b58\u5728`），而不是正常的中文字符。

### 症状
- 前端显示：`\u9875\u9762\u4e0d\u5b58\u5728` 而不是 `页面不存在`
- 错误消息无法正常阅读

### 根本原因

Flask 的 `jsonify()` 函数默认设置 `JSON_AS_ASCII = True`，这导致所有非 ASCII 字符（包括中文）都被转义为 Unicode 转义序列。

## 解决方案

在 `app.py` 中添加以下配置：

```python
app = Flask(__name__)
# 让 jsonify 返回中文不再转义为 \uXXXX
app.config['JSON_AS_ASCII'] = False
```

这个配置会全局应用到所有使用 `jsonify()` 的地方，包括：
- `app.py` 中的错误处理
- `survey_engine/api.py` 中的 API 端点
- `expert_portal/api.py` 中的 API 端点
- 其他所有使用 `jsonify()` 的蓝图

## 修改文件

- **app.py**: 在第 21 行添加 `app.config['JSON_AS_ASCII'] = False`

## 验证方法

1. 启动应用
2. 访问一个不存在的页面（如 `/nonexistent-page`）
3. 查看浏览器开发者工具的 Network 标签
4. 检查 API 响应中的错误消息是否显示为中文而不是 Unicode 转义序列

## 相关配置

- `JSON_AS_ASCII`: 控制 jsonify 是否转义非 ASCII 字符
- `JSON_SORT_KEYS`: 控制 JSON 键是否排序
- `JSONIFY_PRETTYPRINT_REGULAR`: 控制是否格式化 JSON 输出

## 参考资源

- Flask 官方文档: https://flask.palletsprojects.com/config/#JSON_AS_ASCII

