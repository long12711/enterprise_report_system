# -*- coding: utf-8 -*-
"""
现代企业制度评价系统 - Flask 主应用
集成：问卷引擎、报告生成、专家管理、工商联门户等
"""
from flask import Flask, render_template, request, jsonify, session, redirect, send_file, send_from_directory
try:
    from flask.json.provider import DefaultJSONProvider as _DefaultJSONProvider
except Exception:
    _DefaultJSONProvider = None
from functools import wraps
import os
import json
import uuid
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 Flask 应用
app = Flask(__name__)
# 让 jsonify 返回中文不再转义为 \\uXXXX，并确保新JSON提供器也关闭ASCII转义
app.config['JSON_AS_ASCII'] = False
try:
    # Flask 2.2+ 新JSON提供器
    app.json.ensure_ascii = False
except Exception:
    pass
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 注册专家门户蓝图（如果可用）
try:
    from expert_portal import ui_bp as expert_ui_bp, api_bp as expert_api_bp
    app.register_blueprint(expert_ui_bp, url_prefix='/portal/expert')
    app.register_blueprint(expert_api_bp, url_prefix='/api/portal/expert')
except Exception as _e:
    logger.warning(f'专家门户未加载: {_e}')

# 注册问卷引擎蓝图（提供 /api/get_questions 等接口）
try:
    from survey_engine.api import api_bp as survey_api_bp
    app.register_blueprint(survey_api_bp, url_prefix='/api')
except Exception as _e:
    logger.warning(f'问卷引擎未加载: {_e}')

# 注册问卷管理蓝图（新增）
try:
    from questionnaire_management_api import questionnaire_bp
    app.register_blueprint(questionnaire_bp)
except Exception as _e:
    logger.warning(f'问卷管理模块未加载: {_e}')

# 注册工商联用户管理蓝图
try:
    from chamber_users_management import chamber_users_bp
    app.register_blueprint(chamber_users_bp)
except Exception as _e:
    logger.warning(f'工商联用户管理模块未加载: {_e}')

# 配置
STORAGE_DIR = os.path.join('storage')
UPLOAD_DIR = os.path.join(STORAGE_DIR, 'uploads')
REPORTS_DIR = os.path.join(STORAGE_DIR, 'reports')
SUBMISSIONS_DIR = os.path.join(STORAGE_DIR, 'submissions')
SPECIAL_SUBMISSIONS_DIR = os.path.join(STORAGE_DIR, 'special_submissions')
TUTORING_LOGS_DIR = os.path.join(STORAGE_DIR, 'tutoring_logs')

# 数据库文件
USERS_DB = os.path.join(STORAGE_DIR, 'users.json')
ENTERPRISES_DB = os.path.join(STORAGE_DIR, 'enterprises.json')
EXPERTS_DB = os.path.join(STORAGE_DIR, 'experts.json')
EXPERT_EVALUATIONS_DB = os.path.join(STORAGE_DIR, 'expert_evaluations.json')
SPECIAL_SUBMISSIONS_DB = os.path.join(STORAGE_DIR, 'special_submissions.json')

# 确保存储目录存在
for d in [STORAGE_DIR, UPLOAD_DIR, REPORTS_DIR, SUBMISSIONS_DIR, SPECIAL_SUBMISSIONS_DIR, TUTORING_LOGS_DIR]:
    os.makedirs(d, exist_ok=True)


# ============================================================================
# 工具函数
# ============================================================================

def _ensure_json_file(path, default_data=None):
    """确保 JSON 文件存在"""
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_data or {'items': []}, f, ensure_ascii=False, indent=2)


def _read_json(path):
    """读取 JSON 文件"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('items', []) if isinstance(data, dict) and 'items' in data else (data if isinstance(data, list) else [])
    except Exception as e:
        logger.error(f"读取 JSON 文件失败: {path}, {e}")
        return []


def _write_json(path, items):
    """写入 JSON 文件"""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({'items': items}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"写入 JSON 文件失败: {path}, {e}")


def _role_required(*roles):
    """检查用户角色装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')
            # 如果没有认证，自动设置为工商联用户（用于测试）
            if not user_role:
                session['role'] = 'chamber_of_commerce'
                session['username'] = 'test_user'
                user_role = 'chamber_of_commerce'
            if user_role not in roles:
                return jsonify({'success': False, 'error': '未授权'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============================================================================
# 初始化数据库
# ============================================================================

def init_databases():
    """初始化所有数据库文件"""
    _ensure_json_file(USERS_DB, {'items': []})
    _ensure_json_file(ENTERPRISES_DB, {'items': []})
    _ensure_json_file(EXPERTS_DB, {'items': []})
    _ensure_json_file(EXPERT_EVALUATIONS_DB, {'items': []})
    _ensure_json_file(SPECIAL_SUBMISSIONS_DB, {'items': []})


init_databases()


# ============================================================================
# 认证路由
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面与处理"""
    if request.method == 'POST':
        data = request.get_json(force=True)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', 'enterprise')  # enterprise|expert|chamber_of_commerce
        
        # 简单验证（生产环境应使用数据库）
        if username and password:
            session['username'] = username
            session['role'] = role
            session['user_id'] = uuid.uuid4().hex[:12]
            # 纠正不同角色的跳转地址
            if role == 'chamber_of_commerce':
                redirect_path = '/portal/chamber'
            elif role == 'expert':
                redirect_path = '/portal/expert'
            else:
                redirect_path = '/portal/enterprise'
            return jsonify({'success': True, 'redirect': redirect_path})
        
        return jsonify({'success': False, 'error': '用户名或密码错误'}), 401
    
    return render_template('admin_login.html')


@app.route('/logout', methods=['POST'])
def logout():
    """登出"""
    session.clear()
    return jsonify({'success': True})

# 兼容旧接口/管理路径
@app.route('/admin/login')
def admin_login_redirect():
    return redirect('/login')

@app.route('/api/login', methods=['POST'])
def api_login_proxy():
    # 兼容旧版前端调用
    return login()

@app.route('/api/logout', methods=['POST'])
def api_logout_proxy():
    return logout()


@app.route('/')
def index():
    """首页"""
    if session.get('username'):
        role = session.get('role')
        if role == 'chamber_of_commerce':
            return redirect('/portal/chamber')
        elif role == 'expert':
            return redirect('/portal/expert')
        else:
            return redirect('/portal/enterprise')
    return render_template('index.html')


@app.route('/test')
def test_api():
    """API 测试页面"""
    return render_template('api_test.html')

# 会话信息（供前端识别登录状态、角色与默认等级）
@app.route('/api/session')
def api_session():
    username = session.get('username')
    role = session.get('role')
    user_level = None
    display_name = None
    if username and role:
        # 从本地配置推断默认等级
        try:
            import json, os
            with open('user_levels.json', 'r', encoding='utf-8') as f:
                mapping = json.load(f)
            key = f"{role}:{username}"
            user_level = mapping.get(key)
        except Exception:
            pass
        # 合理的默认值
        if not user_level:
            user_level = 'advanced' if role == 'enterprise' else (
                'municipal' if role == 'chamber_of_commerce' else (
                    'junior' if role == 'expert' else 'beginner'))
        display_name = username
    return jsonify({
        'success': True,
        'logged_in': bool(username),
        'username': username,
        'display_name': display_name,
        'role': role,
        'user_level': user_level
    })

# 在线问卷页面
@app.route('/questionnaire')
def questionnaire_page():
    # 简单放行：未登录也允许填写，但会尝试沿用URL的user_type/level
    return render_template('questionnaire.html')


# 现代企业制度指数评价问卷页面（新增）
@app.route('/questionnaire/form')
def questionnaire_form():
    """现代企业制度指数评价问卷填写页面"""
    return render_template('questionnaire_form.html')


# ============================================================================
# 工商联门户/企业门户 页面
# ============================================================================

@app.route('/portal/chamber')
@_role_required('chamber_of_commerce')
def chamber_portal():
    """工商联门户页面"""
    return render_template('portal_chamber.html')


@app.route('/portal/chamber/users')
@_role_required('chamber_of_commerce')
def chamber_users_page():
    """工商联用户管理页面"""
    return render_template('chamber_users_management.html')

@app.route('/portal/enterprise')
def enterprise_portal():
    # 企业门户（简单权限判断，非企业则回首页）
    if session.get('role') not in ('enterprise', 'chamber_of_commerce', 'expert'):
        return redirect('/')
    try:
        return render_template('portal_enterprise.html')
    except Exception:
        # 若模板缺失，返回占位页面
        return '<h2>企业门户占位页面</h2>', 200


# 企业管理 API
@app.route('/api/portal/chamber/enterprises', methods=['GET', 'POST'])
@_role_required('chamber_of_commerce')
def enterprises_api():
    """企业列表"""
    if request.method == 'GET':
        q = request.args.get('q', '').strip()
        items = _read_json(ENTERPRISES_DB)
        if q:
            items = [x for x in items if q in (x.get('name', '') or '')]
        return jsonify({'success': True, 'items': items})
    
    return jsonify({'success': False, 'error': '方法不支持'}), 405


@app.route('/api/portal/chamber/enterprises/save', methods=['POST'])
@_role_required('chamber_of_commerce')
def save_enterprise():
    """保存企业信息"""
    data = request.get_json(force=True)
    items = _read_json(ENTERPRISES_DB)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    ent_id = data.get('id')
    if ent_id:
        # 更新
        for it in items:
            if it.get('id') == ent_id:
                it.update({
                    'name': data.get('name', ''),
                    'region': data.get('region', ''),
                    'industry': data.get('industry', ''),
                    'level': data.get('level', 'beginner'),
                    'contact': data.get('contact', ''),
                    'email': data.get('email', ''),
                    'phone': data.get('phone', ''),
                    'updated_at': now
                })
                _write_json(ENTERPRISES_DB, items)
                return jsonify({'success': True, 'id': ent_id})
    else:
        # 新增
        new_id = uuid.uuid4().hex[:12]
        items.append({
            'id': new_id,
            'name': data.get('name', ''),
            'region': data.get('region', ''),
            'industry': data.get('industry', ''),
            'level': data.get('level', 'beginner'),
            'contact': data.get('contact', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'created_at': now,
            'updated_at': now
        })
        _write_json(ENTERPRISES_DB, items)
        return jsonify({'success': True, 'id': new_id})
    
    return jsonify({'success': False, 'error': '保存失败'}), 400


@app.route('/api/portal/chamber/enterprises/<ent_id>', methods=['DELETE'])
@_role_required('chamber_of_commerce')
def delete_enterprise(ent_id):
    """删除企业"""
    items = _read_json(ENTERPRISES_DB)
    items = [x for x in items if x.get('id') != ent_id]
    _write_json(ENTERPRISES_DB, items)
    return jsonify({'success': True})


# 资质审核 API
@app.route('/api/portal/chamber/reviews', methods=['GET'])
@_role_required('chamber_of_commerce')
def reviews_api():
    """资质审核列表"""
    level = request.args.get('level', 'auto')
    # 这里应该从实际数据源获取，现在返回示例数据
    items = _read_json(ENTERPRISES_DB)
    reviews = []
    for ent in items:
        reviews.append({
            'username': ent.get('id'),
            'enterprise_name': ent.get('name', ''),
            'current_level': ent.get('level', 'beginner'),
            'submit_time_text': ent.get('updated_at', ''),
            'score_percentage': 75.5,
            'eligible': True,
            'upgrade_to': 'intermediate',
            'next_level': 'advanced',
            'excel_file': None,
            'report_file': None
        })
    return jsonify({'success': True, 'items': reviews})


@app.route('/api/portal/chamber/approve-upgrade', methods=['POST'])
@_role_required('chamber_of_commerce')
def approve_upgrade():
    """批准升级"""
    data = request.get_json(force=True)
    username = data.get('username')
    new_level = data.get('new_level')
    
    items = _read_json(ENTERPRISES_DB)
    for it in items:
        if it.get('id') == username:
            it['level'] = new_level
            it['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            _write_json(ENTERPRISES_DB, items)
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '企业不存在'}), 404


@app.route('/api/portal/chamber/upgrade', methods=['POST'])
@_role_required('chamber_of_commerce')
def upgrade_enterprise():
    """企业升级"""
    data = request.get_json(force=True)
    enterprise = data.get('enterprise')
    to_level = data.get('to_level')
    
    items = _read_json(ENTERPRISES_DB)
    for it in items:
        if it.get('name') == enterprise:
            it['level'] = to_level
            it['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            _write_json(ENTERPRISES_DB, items)
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '企业不存在'}), 404


# 专家匹配 API
@app.route('/api/portal/chamber/expert-match', methods=['GET'])
@_role_required('chamber_of_commerce')
def expert_match():
    """获取专家匹配方案"""
    enterprise = request.args.get('enterprise', '').strip()
    if not enterprise:
        return jsonify({'success': False, 'error': '缺少enterprise参数'}), 400
    
    return jsonify({
        'success': True,
        'data': {
            'recommend_group': '张三、李四、王五',
            'priority': '高',
            'region': '天津市',
            'industry': '制造业',
            'last_score_pct': 82.5
        }
    })


# 企业历史 API
@app.route('/api/portal/chamber/enterprise-history', methods=['GET'])
@_role_required('chamber_of_commerce')
def enterprise_history():
    """企业自评历史"""
    enterprise = request.args.get('enterprise', '').strip()
    if not enterprise:
        return jsonify({'success': False, 'error': '缺少enterprise参数'}), 400
    
    return jsonify({
        'success': True,
        'items': [
            {
                'time_text': '2024-01-15',
                'score_pct': 85.5,
                'level': 'intermediate',
                'excel_file': 'questionnaire_2024_01_15.xlsx'
            }
        ]
    })


# 辅导台账 API
@app.route('/api/portal/chamber/tutoring-ledger', methods=['GET', 'POST'])
@_role_required('chamber_of_commerce')
def tutoring_ledger():
    """辅导台账"""
    enterprise = request.args.get('enterprise', '').strip()
    
    if request.method == 'GET':
        if not enterprise:
            return jsonify({'success': False, 'error': '缺少enterprise参数'}), 400
        
        ledger_file = os.path.join(TUTORING_LOGS_DIR, f'{enterprise}.json')
        items = _read_json(ledger_file) if os.path.exists(ledger_file) else []
        return jsonify({'success': True, 'items': items})
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        enterprise = data.get('enterprise')
        if not enterprise:
            return jsonify({'success': False, 'error': '缺少enterprise参数'}), 400
        
        ledger_file = os.path.join(TUTORING_LOGS_DIR, f'{enterprise}.json')
        items = _read_json(ledger_file) if os.path.exists(ledger_file) else []
        
        items.append({
            'id': uuid.uuid4().hex[:12],
            'time': data.get('time') or datetime.now().strftime('%Y-%m-%d %H:%M'),
            'expert': data.get('expert', ''),
            'note': data.get('note', '')
        })
        
        _write_json(ledger_file, items)
        return jsonify({'success': True})


# 报告管理 API
@app.route('/api/portal/chamber/all-reports', methods=['GET'])
@_role_required('chamber_of_commerce')
def all_reports():
    """获取所有报告"""
    reports = []
    if os.path.exists(REPORTS_DIR):
        for fn in os.listdir(REPORTS_DIR):
            fp = os.path.join(REPORTS_DIR, fn)
            if os.path.isfile(fp):
                reports.append({
                    'filename': fn,
                    'enterprise_name': fn.split('_')[1] if '_' in fn else '未知',
                    'type': 'Word' if fn.endswith('.docx') else 'PDF',
                    'file_size': os.path.getsize(fp),
                    'created_time': os.path.getctime(fp)
                })
    return jsonify({'success': True, 'reports': reports})


@app.route('/api/portal/chamber/send-report', methods=['POST'])
@_role_required('chamber_of_commerce')
def send_report():
    """发送报告（邮件）"""
    data = request.get_json(force=True)
    recipient = data.get('recipient')
    report_filename = data.get('report_filename')
    
    if not recipient or not report_filename:
        return jsonify({'success': False, 'error': '缺少参数'}), 400
    
    # 这里应该实现邮件发送逻辑
    logger.info(f"发送报告 {report_filename} 到 {recipient}")
    
    return jsonify({'success': True, 'message': '邮件已发送'})


# 工商联用户管理 API
@app.route('/api/portal/chamber/users', methods=['GET'])
@_role_required('chamber_of_commerce')
def chamber_users():
    """工商联用户列表"""
    users = _read_json(USERS_DB)
    # 过滤出工商联用户
    chamber_users = [u for u in users if u.get('role') == 'chamber_of_commerce']
    return jsonify({'success': True, 'users': chamber_users})


# 问卷管理 API
@app.route('/api/portal/chamber/questionnaires', methods=['GET'])
@_role_required('chamber_of_commerce')
def questionnaires_api():
    """问卷列表"""
    questionnaires = [
        {
            'name': '现代企业制度评价问卷',
            'question_count': 50,
            'created_time': '2024-01-01',
            'status': '启用'
        }
    ]
    return jsonify({'success': True, 'questionnaires': questionnaires})


# 辅导记录 API
@app.route('/api/portal/chamber/tutoring-records', methods=['GET'])
@_role_required('chamber_of_commerce')
def tutoring_records():
    """辅导记录"""
    records = [
        {
            'expert': '张三',
            'enterprise': '示例企业',
            'message': '建议加强内部治理',
            'time': '2024-01-15 10:30'
        }
    ]
    return jsonify({'success': True, 'records': records})


# ============================================================================
# 专家管理 API
# ============================================================================

@app.route('/api/portal/chamber/experts', methods=['GET', 'POST'])
@_role_required('chamber_of_commerce')
def experts_api():
    """专家列表与保存"""
    if request.method == 'GET':
        q = request.args.get('q', '').strip()
        items = _read_json(EXPERTS_DB)
        if q:
            items = [x for x in items if q in (x.get('name', '') or '')]
        return jsonify({'success': True, 'items': items})
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        items = _read_json(EXPERTS_DB)
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        exp_id = data.get('id')
        if exp_id:
            # 更新
            for it in items:
                if it.get('id') == exp_id:
                    it.update({
                        'name': data.get('name', ''),
                        'region': data.get('region', ''),
                        'province': data.get('province', ''),
                        'industry': data.get('industry', ''),
                        'level': data.get('level', 'county'),
                        'phone': data.get('phone', ''),
                        'email': data.get('email', ''),
                        'org': data.get('org', ''),
                        'skills': data.get('skills', ''),
                        'updated_at': now
                    })
                    _write_json(EXPERTS_DB, items)
                    return jsonify({'success': True, 'id': exp_id})
        else:
            # 新增
            new_id = uuid.uuid4().hex[:12]
            items.append({
                'id': new_id,
                'name': data.get('name', ''),
                'region': data.get('region', ''),
                'province': data.get('province', ''),
                'industry': data.get('industry', ''),
                'level': data.get('level', 'county'),
                'phone': data.get('phone', ''),
                'email': data.get('email', ''),
                'org': data.get('org', ''),
                'skills': data.get('skills', ''),
                'created_at': now,
                'updated_at': now
            })
            _write_json(EXPERTS_DB, items)
            return jsonify({'success': True, 'id': new_id})
        
        return jsonify({'success': False, 'error': '保存失败'}), 400


@app.route('/api/portal/chamber/experts/<exp_id>', methods=['DELETE'])
@_role_required('chamber_of_commerce')
def delete_expert(exp_id):
    """删除专家"""
    items = _read_json(EXPERTS_DB)
    items = [x for x in items if x.get('id') != exp_id]
    _write_json(EXPERTS_DB, items)
    return jsonify({'success': True})


@app.route('/api/portal/chamber/expert-self', methods=['GET'])
@_role_required('chamber_of_commerce')
def expert_self():
    """专家自评详情"""
    expert = request.args.get('expert', '').strip()
    if not expert:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    
    return jsonify({'success': True, 'items': []})


@app.route('/api/portal/chamber/expert-rate', methods=['GET', 'POST'])
@_role_required('chamber_of_commerce')
def expert_rate():
    """专家评级管理"""
    if request.method == 'GET':
        expert = request.args.get('expert', '').strip()
        if not expert:
            return jsonify({'success': False, 'error': '缺少expert参数'}), 400
        
        items = _read_json(EXPERTS_DB)
        it = next((x for x in items if x.get('name') == expert), None)
        if not it:
            return jsonify({'success': False, 'error': '专家不存在'}), 404
        
        level = it.get('level', 'county')
        scope = '县市内企业' if level == 'county' else ('全省企业' if level == 'province' else '全国企业')
        return jsonify({'success': True, 'data': {'expert': expert, 'level': level, 'scope': scope}})
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        expert = data.get('expert')
        to_level = data.get('to_level')
        
        if not expert or not to_level:
            return jsonify({'success': False, 'error': '缺少参数'}), 400
        
        items = _read_json(EXPERTS_DB)
        for it in items:
            if it.get('name') == expert:
                it['level'] = to_level
                it['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        _write_json(EXPERTS_DB, items)
        return jsonify({'success': True})


@app.route('/api/portal/chamber/expert-tutoring', methods=['GET'])
@_role_required('chamber_of_commerce')
def expert_tutoring():
    """专家辅导详情"""
    expert = request.args.get('expert', '').strip()
    if not expert:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    
    rows = []
    if os.path.exists(TUTORING_LOGS_DIR):
        for fn in os.listdir(TUTORING_LOGS_DIR):
            if not fn.endswith('.json'):
                continue
            enterprise = fn[:-5]
            path = os.path.join(TUTORING_LOGS_DIR, fn)
            try:
                items = _read_json(path)
                for r in items:
                    if (r.get('expert') or '').strip() == expert:
                        rows.append({
                            'time': r.get('time'),
                            'enterprise': enterprise,
                            'content': r.get('note', '')
                        })
            except Exception:
                continue
    
    rows.sort(key=lambda x: x['time'] or '', reverse=True)
    return jsonify({'success': True, 'items': rows})


@app.route('/api/portal/chamber/expert-evaluations', methods=['GET', 'POST'])
@_role_required('chamber_of_commerce')
def expert_evaluations():
    """企业对专家的评价"""
    if request.method == 'GET':
        expert = request.args.get('expert', '').strip()
        if not expert:
            return jsonify({'success': False, 'error': '缺少expert参数'}), 400
        
        items = _read_json(EXPERT_EVALUATIONS_DB)
        items = [x for x in items if x.get('expert') == expert]
        items.sort(key=lambda x: x.get('time', ''), reverse=True)
        return jsonify({'success': True, 'items': items})
    
    elif request.method == 'POST':
        data = request.get_json(force=True)
        expert = data.get('expert')
        enterprise = data.get('enterprise')
        score = float(data.get('score', 0))
        comment = data.get('comment', '')
        
        if not expert or not enterprise:
            return jsonify({'success': False, 'error': '缺少参数'}), 400
        
        items = _read_json(EXPERT_EVALUATIONS_DB)
        items.append({
            'id': uuid.uuid4().hex[:12],
            'expert': expert,
            'enterprise': enterprise,
            'score': score,
            'comment': comment,
            'time': data.get('time') or datetime.now().strftime('%Y-%m-%d %H:%M')
        })
        
        _write_json(EXPERT_EVALUATIONS_DB, items)
        return jsonify({'success': True})


# ============================================================================
# 专项审核 API
# ============================================================================

@app.route('/api/special/list', methods=['GET'])
@_role_required('chamber_of_commerce')
def special_list():
    """专项申请列表"""
    items = _read_json(SPECIAL_SUBMISSIONS_DB)
    return jsonify({'success': True, 'items': items})


@app.route('/api/special/review', methods=['POST'])
@_role_required('chamber_of_commerce')
def special_review():
    """专项审核"""
    data = request.get_json(force=True)
    spec_id = data.get('id')
    action = data.get('action')  # approve|reject
    remark = data.get('remark', '')
    
    items = _read_json(SPECIAL_SUBMISSIONS_DB)
    for it in items:
        if it.get('id') == spec_id:
            it['status'] = 'approved' if action == 'approve' else 'rejected'
            it['remark'] = remark
            it['reviewed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            _write_json(SPECIAL_SUBMISSIONS_DB, items)
            return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '申请不存在'}), 404


@app.route('/api/special/download/<spec_id>/<filename>')
@_role_required('chamber_of_commerce')
def download_special_file(spec_id, filename):
    """下载专项附件"""
    file_path = os.path.join(SPECIAL_SUBMISSIONS_DIR, spec_id, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'success': False, 'error': '文件不存在'}), 404


# ============================================================================
# 文件下载
# ============================================================================

@app.route('/download/<filename>')
def download_file(filename):
    """下载报告"""
    file_path = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'success': False, 'error': '文件不存在'}), 404


@app.route('/download/submission/<filename>')
def download_submission(filename):
    """下载问卷提交"""
    file_path = os.path.join(SUBMISSIONS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'success': False, 'error': '文件不存在'}), 404


# ============================================================================
# 错误处理
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({'success': False, 'error': '页面不存在'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 错误处理"""
    logger.error(f"服务器错误: {error}")
    return jsonify({'success': False, 'error': '服务器内部错误'}), 500


# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    # 开发环境配置
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )

