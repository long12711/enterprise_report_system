from flask import Blueprint, jsonify, request, session
import os, json, uuid
from datetime import datetime

expert_bp = Blueprint('expert_bp', __name__)

STORAGE_DIR = os.path.join('storage')
EXPERT_DB = os.path.join(STORAGE_DIR, 'experts.json')
EXPERT_EVAL_DB = os.path.join(STORAGE_DIR, 'expert_evaluations.json')
TUTORING_LOG_DIR = os.path.join(STORAGE_DIR, 'tutoring_logs')  # 复用企业台账


def _ensure_storage():
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(TUTORING_LOG_DIR, exist_ok=True)
    for fp, init in [(EXPERT_DB, {'items': []}), (EXPERT_EVAL_DB, {'items': []})]:
        if not os.path.exists(fp):
            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(init, f, ensure_ascii=False, indent=2)


def _read_json_list(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        return d['items'] if isinstance(d, dict) and 'items' in d else (d if isinstance(d, list) else [])
    except Exception:
        return []


def _write_json_list(path, items):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'items': items}, f, ensure_ascii=False, indent=2)


def _role_required():
    # 仅允许工商联门户用户
    return session.get('role') == 'chamber_of_commerce'


@expert_bp.before_request
def _init():
    _ensure_storage()


# 1) 专家信息 CRUD
@expert_bp.get('/experts')
def experts_list():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    q = (request.args.get('q') or '').strip()
    items = _read_json_list(EXPERT_DB)
    if q:
        items = [x for x in items if q in (x.get('name') or '')]
    return jsonify({'success': True, 'items': items})


@expert_bp.post('/experts/save')
def experts_save():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    data = request.get_json(force=True)
    items = _read_json_list(EXPERT_DB)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    exp_id = data.get('id')
    if exp_id:
        for it in items:
            if it.get('id') == exp_id:
                it.update({
                    'name': data.get('name',''),
                    'region': data.get('region',''),
                    'province': data.get('province',''),
                    'industry': data.get('industry',''),
                    'level': data.get('level','county'),  # county|province|national
                    'phone': data.get('phone',''),
                    'email': data.get('email',''),
                    'org': data.get('org',''),
                    'skills': data.get('skills',''),
                    'updated_at': now
                })
                _write_json_list(EXPERT_DB, items)
                return jsonify({'success': True, 'id': exp_id})
    new_id = uuid.uuid4().hex[:12]
    items.append({
        'id': new_id,
        'name': data.get('name',''),
        'region': data.get('region',''),
        'province': data.get('province',''),
        'industry': data.get('industry',''),
        'level': data.get('level','county'),
        'phone': data.get('phone',''),
        'email': data.get('email',''),
        'org': data.get('org',''),
        'skills': data.get('skills',''),
        'created_at': now,
        'updated_at': now
    })
    _write_json_list(EXPERT_DB, items)
    return jsonify({'success': True, 'id': new_id})


@expert_bp.delete('/experts/<exp_id>')
def experts_delete(exp_id):
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    items = _read_json_list(EXPERT_DB)
    items = [x for x in items if x.get('id') != exp_id]
    _write_json_list(EXPERT_DB, items)
    return jsonify({'success': True})


# 2) 专家自评详情（占位实现）
@expert_bp.get('/expert-self')
def expert_self():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    name = (request.args.get('expert') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    # TODO: 接入真实专家自评数据源
    return jsonify({'success': True, 'items': []})


# 3) 专家评级管理（GET查看、POST设置）
@expert_bp.get('/expert-rate')
def expert_rate_get():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    name = (request.args.get('expert') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    items = _read_json_list(EXPERT_DB)
    it = next((x for x in items if x.get('name') == name), None)
    if not it:
        return jsonify({'success': False, 'error': '专家不存在'}), 404
    level = it.get('level', 'county')
    scope = '县市内企业' if level == 'county' else ('全省企业' if level == 'province' else '全国企业')
    return jsonify({'success': True, 'data': {'expert': name, 'level': level, 'scope': scope}})


@expert_bp.post('/expert-rate')
def expert_rate_post():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    data = request.get_json(force=True)
    name = data.get('expert')
    to_level = data.get('to_level')  # county|province|national
    if not name or not to_level:
        return jsonify({'success': False, 'error': '缺少参数'}), 400
    items = _read_json_list(EXPERT_DB)
    for it in items:
        if it.get('name') == name:
            it['level'] = to_level
            it['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    _write_json_list(EXPERT_DB, items)
    return jsonify({'success': True})


# 4) 专家辅导详情（从企业台账聚合）
@expert_bp.get('/expert-tutoring')
def expert_tutoring():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    name = (request.args.get('expert') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    rows = []
    for fn in os.listdir(TUTORING_LOG_DIR):
        if not fn.endswith('.json'):
            continue
        enterprise = fn[:-5]
        path = os.path.join(TUTORING_LOG_DIR, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            for r in logs:
                if (r.get('expert') or '').strip() == name:
                    rows.append({'time': r.get('time'), 'enterprise': enterprise, 'note': r.get('note')})
        except Exception:
            continue
    rows.sort(key=lambda x: x['time'] or '', reverse=True)
    return jsonify({'success': True, 'items': rows})


# 5) 企业对专家评价（列表与新增）
@expert_bp.get('/expert-evaluations')
def expert_evals_get():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    name = (request.args.get('expert') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': '缺少expert参数'}), 400
    items = _read_json_list(EXPERT_EVAL_DB)
    items = [x for x in items if x.get('expert') == name]
    items.sort(key=lambda x: x.get('time', ''), reverse=True)
    return jsonify({'success': True, 'items': items})


@expert_bp.post('/expert-evaluations')
def expert_evals_post():
    if not _role_required():
        return jsonify({'success': False, 'error': '未授权'}), 401
    data = request.get_json(force=True)
    expert = data.get('expert')
    enterprise = data.get('enterprise')
    score = float(data.get('score', 0))
    comment = data.get('comment', '')
    if not expert or not enterprise:
        return jsonify({'success': False, 'error': '缺少参数'}), 400
    items = _read_json_list(EXPERT_EVAL_DB)
    items.append({
        'id': uuid.uuid4().hex[:12],
        'expert': expert,
        'enterprise': enterprise,
        'score': score,
        'comment': comment,
        'time': data.get('time') or datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    _write_json_list(EXPERT_EVAL_DB, items)
    return jsonify({'success': True})

