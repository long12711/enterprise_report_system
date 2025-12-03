from flask import Flask, session, redirect
from datetime import timedelta
import os

# 最小可运行 Runner：仅注册专家门户蓝图与必要目录
# 用法：
#   1) python -m venv .venv && .venv\Scripts\activate (或 source .venv/bin/activate)
#   2) pip install -r requirements.txt  (或手动安装 flask/pandas/openpyxl)
#   3) python run_expert_portal.py
#   4) 打开 http://localhost:5000 ，点击“临时登录为专家”进入专家门户

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# 必需目录（供专家门户 API 读取/写入）
app.config['SUBMISSIONS_FOLDER'] = 'storage/submissions'
app.config['REPORT_FOLDER'] = 'storage/reports'
for d in [
    app.config['SUBMISSIONS_FOLDER'],
    app.config['REPORT_FOLDER'],
    'storage/expert_ledgers',
    'storage/expert_feedbacks',
    'storage/enterprise_reviews',
]:
    os.makedirs(d, exist_ok=True)

# 注册专家门户蓝图
from expert_portal import ui_bp as expert_ui_bp, api_bp as expert_api_bp  # noqa: E402
app.register_blueprint(expert_ui_bp, url_prefix='/portal/expert')
app.register_blueprint(expert_api_bp, url_prefix='/api/portal/expert')


@app.route('/')
def home():
    return '<h2>专家门户最小运行环境</h2><p><a href="/login-as-expert">临时登录为专家</a> | <a href="/portal/expert">进入专家门户</a></p>'


@app.route('/login-as-expert')
def login_as_expert():
    # 临时登录（无完整账号系统时使用）
    session['logged_in'] = True
    session['role'] = 'expert'
    session['username'] = 'expert_demo'
    session['display_name'] = '专家-演示'
    # junior / intermediate / senior
    session['user_level'] = 'junior'
    session.permanent = True
    return redirect('/portal/expert')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)




