# 快速修复参考 - JSON 中文编码问题

## 问题
企业门户显示错误时，中文被转义为 Unicode 转义序列（如 `\u9875\u9762\u4e0d\u5b58\u5728`）

## 解决方案
在 `app.py` 第 21 行添加：
```python
app.config['JSON_AS_ASCII'] = False
```

## 验证
访问 http://localhost:5000/nonexistent-page，检查错误消息是否显示为中文

## 状态
✅ 已修复

