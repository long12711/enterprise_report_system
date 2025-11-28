from flask import Blueprint, jsonify, session, redirect
from .services.matcher import get_expert_matches

api_bp = Blueprint('expert_api', __name__)


@api_bp.before_request
def _ensure_expert_role_api():
    if session.get('role') != 'expert':
        return redirect('/')


@api_bp.get('/matches')
def api_matches():
    try:
        items = get_expert_matches()
        return jsonify({'success': True, 'items': items})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

