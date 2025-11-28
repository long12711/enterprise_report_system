from flask import Blueprint, render_template, session, redirect

ui_bp = Blueprint('expert_ui', __name__, template_folder='templates', static_folder='static', static_url_path='static')


@ui_bp.before_request
def _ensure_expert_role():
    # 仅允许专家访问
    if session.get('role') != 'expert':
        return redirect('/')


@ui_bp.route('/')
def expert_home():
    return render_template('portal_expert.html')

