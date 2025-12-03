"""
指标体系管理API路由
"""

from flask import Blueprint, request, jsonify, session
from functools import wraps
from .models import IndicatorModel, ScoringRuleModel, QuestionnaireVersionModel

# 创建蓝图
indicator_management_bp = Blueprint('indicator_management', __name__, url_prefix='/api/admin/indicator-management')

# 初始化模型
indicator_model = IndicatorModel()
scoring_rule_model = ScoringRuleModel()
questionnaire_version_model = QuestionnaireVersionModel()


def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return jsonify({'success': False, 'error': '需要管理员权限'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ==================== 指标管理 API ====================

@indicator_management_bp.route('/indicators', methods=['GET'])
@admin_required
def get_indicators():
    """获取指标列表"""
    try:
        level = request.args.get('level')
        status = request.args.get('status', 'active')
        
        indicators = indicator_model.get_all(level=level, status=status)
        
        return jsonify({
            'success': True,
            'data': indicators,
            'total': len(indicators)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/indicators/<indicator_id>', methods=['GET'])
@admin_required
def get_indicator(indicator_id):
    """获取指标详情"""
    try:
        indicator = indicator_model.get_by_id(indicator_id)
        
        if not indicator:
            return jsonify({'success': False, 'error': '指标不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': indicator
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/indicators', methods=['POST'])
@admin_required
def create_indicator():
    """创建新指标"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['level1', 'level2', 'level3', 'question']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
        
        indicator = indicator_model.create(data)
        
        return jsonify({
            'success': True,
            'data': indicator,
            'message': '指标创建成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/indicators/<indicator_id>', methods=['PUT'])
@admin_required
def update_indicator(indicator_id):
    """更新指标"""
    try:
        data = request.get_json()
        
        indicator = indicator_model.update(indicator_id, data)
        
        if not indicator:
            return jsonify({'success': False, 'error': '指标不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': indicator,
            'message': '指标更新成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/indicators/<indicator_id>', methods=['DELETE'])
@admin_required
def delete_indicator(indicator_id):
    """删除指标"""
    try:
        success = indicator_model.delete(indicator_id)
        
        if not success:
            return jsonify({'success': False, 'error': '指标不存在'}), 404
        
        return jsonify({
            'success': True,
            'message': '指标删除成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 评分规则管理 API ====================

@indicator_management_bp.route('/scoring-rules/by-level/<level>', methods=['GET'])
@admin_required
def get_scoring_rules_by_level(level):
    """按级别获取评分规则"""
    try:
        rules = scoring_rule_model.get_by_level(level)
        
        return jsonify({
            'success': True,
            'data': rules,
            'total': len(rules),
            'level': level
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/scoring-rules', methods=['POST'])
@admin_required
def create_scoring_rule():
    """创建评分规则"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['indicator_id', 'level', 'rule_type', 'rule_text']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
        
        rule = scoring_rule_model.create(data)
        
        return jsonify({
            'success': True,
            'data': rule,
            'message': '评分规则创建成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/scoring-rules/<rule_id>', methods=['PUT'])
@admin_required
def update_scoring_rule(rule_id):
    """更新评分规则"""
    try:
        data = request.get_json()
        
        rule = scoring_rule_model.update(rule_id, data)
        
        if not rule:
            return jsonify({'success': False, 'error': '评分规则不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': rule,
            'message': '评分规则更新成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/scoring-rules/<rule_id>', methods=['DELETE'])
@admin_required
def delete_scoring_rule(rule_id):
    """删除评分规则"""
    try:
        success = scoring_rule_model.delete(rule_id)
        
        if not success:
            return jsonify({'success': False, 'error': '评分规则不存在'}), 404
        
        return jsonify({
            'success': True,
            'message': '评分规则删除成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== 问卷版本管理 API ====================

@indicator_management_bp.route('/questionnaires', methods=['GET'])
@admin_required
def get_questionnaires():
    """获取问卷列表"""
    try:
        level = request.args.get('level')
        status = request.args.get('status')
        
        questionnaires = questionnaire_version_model.get_all(level=level, status=status)
        
        return jsonify({
            'success': True,
            'data': questionnaires,
            'total': len(questionnaires)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires/<version_id>', methods=['GET'])
@admin_required
def get_questionnaire(version_id):
    """获取问卷详情"""
    try:
        questionnaire = questionnaire_version_model.get_by_id(version_id)
        
        if not questionnaire:
            return jsonify({'success': False, 'error': '问卷不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': questionnaire
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires', methods=['POST'])
@admin_required
def create_questionnaire():
    """创建问卷"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['name', 'level', 'version']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
        
        # 添加创建者信息
        data['created_by'] = session.get('admin_username', 'admin')
        
        questionnaire = questionnaire_version_model.create(data)
        
        return jsonify({
            'success': True,
            'data': questionnaire,
            'message': '问卷创建成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires/<version_id>', methods=['PUT'])
@admin_required
def update_questionnaire(version_id):
    """更新问卷"""
    try:
        data = request.get_json()
        
        questionnaire = questionnaire_version_model.update(version_id, data)
        
        if not questionnaire:
            return jsonify({'success': False, 'error': '问卷不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': questionnaire,
            'message': '问卷更新成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires/<version_id>/publish', methods=['POST'])
@admin_required
def publish_questionnaire(version_id):
    """发布问卷"""
    try:
        questionnaire = questionnaire_version_model.publish(version_id)
        
        if not questionnaire:
            return jsonify({'success': False, 'error': '问卷不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': questionnaire,
            'message': '问卷发布成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires/<version_id>/clone', methods=['POST'])
@admin_required
def clone_questionnaire(version_id):
    """克隆问卷（创建新版本）"""
    try:
        data = request.get_json()
        new_version = data.get('version')
        
        if not new_version:
            return jsonify({'success': False, 'error': '缺少新版本号'}), 400
        
        questionnaire = questionnaire_version_model.clone(version_id, new_version)
        
        if not questionnaire:
            return jsonify({'success': False, 'error': '原问卷不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': questionnaire,
            'message': '问卷克隆成功'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@indicator_management_bp.route('/questionnaires/<version_id>/versions', methods=['GET'])
@admin_required
def get_questionnaire_versions(version_id):
    """获取问卷的所有版本"""
    try:
        questionnaire = questionnaire_version_model.get_by_id(version_id)
        
        if not questionnaire:
            return jsonify({'success': False, 'error': '问卷不存在'}), 404
        
        questionnaire_id = questionnaire.get('questionnaire_id', version_id)
        versions = questionnaire_version_model.get_versions(questionnaire_id)
        
        return jsonify({
            'success': True,
            'data': versions,
            'total': len(versions)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500