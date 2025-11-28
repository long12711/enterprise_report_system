from flask import Blueprint

# 导出两个 Blueprint：
# - ui_bp: 专家门户页面（/portal/expert）
# - api_bp: 专家门户相关 API（/api/portal/expert）

# 注意：各自的 url_prefix 在 app.py 中注册时指定

# 在子模块中定义实际路由
def _load_blueprints():
    from .routes import ui_bp as _ui_bp
    from .api import api_bp as _api_bp
    return _ui_bp, _api_bp

ui_bp, api_bp = _load_blueprints()

