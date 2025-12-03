# -*- coding: utf-8 -*-
"""
问卷管理 API
处理问卷的导入、查询、填写和提交
"""
from flask import Blueprint, request, jsonify, session
from functools import wraps
import os
import json
import uuid
from datetime import datetime
import logging
from docx_questionnaire_importer import DocxQuestionnaireImporter
import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)

# 创建蓝图
questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/api/questionnaire')

# 初始化导入器（JSON 回退）
importer = DocxQuestionnaireImporter()

# 数据库配置（MySQL 主）
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', '123456'),
    'database': os.environ.get('DB_NAME', 'localhost_3306')
}


def get_db_connection():
    """获取数据库连接"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logger.error(f"数据库连接失败: {e}")
        return None


def _db_get_template_by_level(level: str):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM questionnaire_templates WHERE level=%s AND status='active'", (level,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except Exception as e:
        logger.error(f"查询模板失败: {e}")
        try:
            cur.close(); conn.close()
        except Exception:
            pass
        return None


def _db_get_template_by_id(template_id: str):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM questionnaire_templates WHERE id=%s", (template_id,))
        row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except Exception as e:
        logger.error(f"按ID查询模板失败: {e}")
        return None


def _db_get_questions_by_template(template_id: str):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM questionnaire_template_questions WHERE template_id=%s ORDER BY sort_order, id",
            (template_id,)
        )
        rows = cur.fetchall()
        cur.close(); conn.close()
        # 规范化字段
        questions = []
        for r in rows:
            questions.append({
                'id': r['id'],
                'survey_id': r['template_id'],
                'seq_no': r.get('seq_no'),
                'level1': r.get('level1'),
                'level2': r.get('level2'),
                'question_text': r.get('question_text'),
                'question_type': r.get('question_type'),
                'score': float(r['score']) if r.get('score') is not None else None,
                'applicable': r.get('applicable'),
                'remarks': r.get('remarks'),
                'requires_file': bool(r.get('requires_file'))
            })
        return questions
    except Exception as e:
        logger.error(f"查询模板题目失败: {e}")
        return []


def _survey_from_template_row(row: dict):
    if not row:
        return None
    return {
        'id': row['id'],
        'name': row['name'],
        'level': row['level'],
        'description': row.get('description') or '',
        'total_questions': row.get('total_questions') or 0,
        'status': row.get('status') or 'active',
        'source_file': row.get('source_file')
    }



def login_required(f):
    """登录检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '未登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


def enterprise_required(f):
    """企业用户检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'enterprise':
            return jsonify({'success': False, 'error': '仅企业用户可访问'}), 403
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# 问卷导入接口
# ============================================================================

@questionnaire_bp.route('/import', methods=['POST'])
def import_questionnaire():
    """
    导入问卷（管理员接口）
    
    请求体:
    {
        "docx_path": "文件路径",
        "level": "初级|中级|高级",
        "survey_name": "问卷名称（可选）"
    }
    """
    try:
        data = request.get_json()
        docx_path = data.get('docx_path')
        level = data.get('level')
        survey_name = data.get('survey_name')

        if not docx_path or not level:
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        if level not in ['初级', '中级', '高级']:
            return jsonify({'success': False, 'error': '无效的问卷级别'}), 400

        # 导入问卷
        survey_id = importer.import_questionnaire(docx_path, level, survey_name)
        
        if survey_id:
            survey = importer.get_survey(survey_id)
            return jsonify({
                'success': True,
                'message': f'问卷导入成功',
                'survey_id': survey_id,
                'survey': survey
            }), 201
        else:
            return jsonify({'success': False, 'error': '问卷导入失败'}), 400

    except Exception as e:
        logger.error(f"导入问卷出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/import-batch', methods=['POST'])
def import_batch_questionnaires():
    """
    批量导入问卷（初级、中级、高级）
    
    请求体:
    {
        "docx_dir": "包含Word文档的目录"
    }
    """
    try:
        data = request.get_json()
        docx_dir = data.get('docx_dir')

        if not docx_dir or not os.path.isdir(docx_dir):
            return jsonify({'success': False, 'error': '无效的目录路径'}), 400

        # 批量导入
        result = importer.import_all_questionnaires(docx_dir)
        
        # 获取导入的问卷详情
        surveys = {}
        for level, survey_id in result.items():
            if survey_id:
                survey = importer.get_survey(survey_id)
                surveys[level] = survey

        return jsonify({
            'success': True,
            'message': '问卷批量导入成功',
            'result': result,
            'surveys': surveys
        }), 201

    except Exception as e:
        logger.error(f"批量导入问卷出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# 问卷查询接口
# ============================================================================

@questionnaire_bp.route('/surveys', methods=['GET'])
def list_surveys():
    """获取所有问卷列表（优先 MySQL）"""
    try:
        # MySQL 主
        conn = get_db_connection()
        surveys = None
        if conn:
            try:
                cur = conn.cursor(dictionary=True)
                cur.execute("SELECT * FROM questionnaire_templates WHERE status='active' ORDER BY level")
                rows = cur.fetchall()
                cur.close(); conn.close()
                surveys = [_survey_from_template_row(r) for r in rows]
            except Exception as e:
                logger.warning(f"从 MySQL 读取问卷列表失败，退回 JSON: {e}")
        # JSON 备
        if surveys is None:
            surveys = importer.list_surveys()
        return jsonify({'success': True, 'surveys': surveys, 'total': len(surveys)}), 200
    except Exception as e:
        logger.error(f"获取问卷列表出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/survey/<survey_id>', methods=['GET'])
def get_survey(survey_id):
    """获取问卷详情（优先 MySQL）"""
    try:
        # MySQL 主
        row = _db_get_template_by_id(survey_id)
        if row:
            survey = _survey_from_template_row(row)
            questions = _db_get_questions_by_template(survey_id)
            return jsonify({
                'success': True,
                'survey': survey,
                'questions': questions,
                'total_questions': len(questions)
            }), 200

        # JSON 备
        survey = importer.get_survey(survey_id)
        if not survey:
            return jsonify({'success': False, 'error': '问卷不存在'}), 404
        questions = importer.get_survey_questions(survey_id)
        return jsonify({'success': True, 'survey': survey, 'questions': questions, 'total_questions': len(questions)}), 200
    except Exception as e:
        logger.error(f"获取问卷详情出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/survey/level/<level>', methods=['GET'])
def get_survey_by_level(level):
    """按级别获取问卷（优先 MySQL）"""
    try:
        if level not in ['初级', '中级', '高级']:
            return jsonify({'success': False, 'error': '无效的问卷级别'}), 400

        # MySQL 主
        row = _db_get_template_by_level(level)
        if row:
            survey = _survey_from_template_row(row)
            questions = _db_get_questions_by_template(row['id'])
            return jsonify({'success': True, 'survey': survey, 'questions': questions, 'total_questions': len(questions)}), 200

        # JSON 备
        survey = importer.get_survey_by_level(level)
        if not survey:
            return jsonify({'success': False, 'error': f'未找到{level}级问卷'}), 404
        questions = importer.get_survey_questions(survey['id'])
        return jsonify({'success': True, 'survey': survey, 'questions': questions, 'total_questions': len(questions)}), 200
    except Exception as e:
        logger.error(f"获取问卷出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# 问卷填写接口
# ============================================================================

@questionnaire_bp.route('/submission/create', methods=['POST'])
@login_required
@enterprise_required
def create_submission():
    """
    创建问卷提交（企业用户）
    
    请求体:
    {
        "survey_level": "初级|中级|高级"
    }
    """
    try:
        data = request.get_json()
        survey_level = data.get('survey_level')
        enterprise_id = session.get('enterprise_id')

        if not survey_level or survey_level not in ['初级', '中级', '高级']:
            return jsonify({'success': False, 'error': '无效的问卷级别'}), 400

        # 获取问卷
        survey = importer.get_survey_by_level(survey_level)
        if not survey:
            return jsonify({'success': False, 'error': f'未找到{survey_level}级问卷'}), 404

        # 创建提交记录
        submission_id = str(uuid.uuid4())
        submission = {
            'id': submission_id,
            'enterprise_id': enterprise_id,
            'survey_id': survey['id'],
            'survey_level': survey_level,
            'status': 'draft',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        # 保存到数据库
        db = importer.load_db()
        if 'submissions' not in db:
            db['submissions'] = []
        db['submissions'].append(submission)
        importer.save_db(db)

        # 获取问卷问题
        questions = importer.get_survey_questions(survey['id'])

        return jsonify({
            'success': True,
            'submission_id': submission_id,
            'survey': survey,
            'questions': questions,
            'message': '问卷创建成功'
        }), 201

    except Exception as e:
        logger.error(f"创建问卷提交出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/submission/<submission_id>', methods=['GET'])
@login_required
@enterprise_required
def get_submission(submission_id):
    """获取问卷提交详情"""
    try:
        db = importer.load_db()
        submission = None
        
        for sub in db.get('submissions', []):
            if sub['id'] == submission_id:
                submission = sub
                break

        if not submission:
            return jsonify({'success': False, 'error': '问卷提交不存在'}), 404

        # 权限检查
        if submission['enterprise_id'] != session.get('enterprise_id'):
            return jsonify({'success': False, 'error': '无权访问'}), 403

        # 获取问卷和问题
        survey = importer.get_survey(submission['survey_id'])
        questions = importer.get_survey_questions(submission['survey_id'])

        # 获取已填写的答案
        answers = db.get('answers', {}).get(submission_id, {})

        return jsonify({
            'success': True,
            'submission': submission,
            'survey': survey,
            'questions': questions,
            'answers': answers
        }), 200

    except Exception as e:
        logger.error(f"获取问卷提交出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/submission/<submission_id>/save', methods=['POST'])
@login_required
@enterprise_required
def save_submission(submission_id):
    """
    保存问卷答案（草稿）
    
    请求体:
    {
        "answers": {
            "question_id": "answer_value",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        answers = data.get('answers', {})

        db = importer.load_db()
        
        # 查找提交记录
        submission = None
        for sub in db.get('submissions', []):
            if sub['id'] == submission_id:
                submission = sub
                break

        if not submission:
            return jsonify({'success': False, 'error': '问卷提交不存在'}), 404

        # 权限检查
        if submission['enterprise_id'] != session.get('enterprise_id'):
            return jsonify({'success': False, 'error': '无权访问'}), 403

        # 保存答案
        if 'answers' not in db:
            db['answers'] = {}
        db['answers'][submission_id] = answers
        
        # 更新提交时间
        submission['updated_at'] = datetime.now().isoformat()
        importer.save_db(db)

        return jsonify({
            'success': True,
            'message': '答案已保存',
            'submission_id': submission_id
        }), 200

    except Exception as e:
        logger.error(f"保存问卷答案出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/submission/<submission_id>/submit', methods=['POST'])
@login_required
@enterprise_required
def submit_questionnaire(submission_id):
    """
    提交问卷
    
    请求体:
    {
        "answers": {
            "question_id": "answer_value",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        answers = data.get('answers', {})

        db = importer.load_db()
        
        # 查找提交记录
        submission = None
        for sub in db.get('submissions', []):
            if sub['id'] == submission_id:
                submission = sub
                break

        if not submission:
            return jsonify({'success': False, 'error': '问卷提交不存在'}), 404

        # 权限检查
        if submission['enterprise_id'] != session.get('enterprise_id'):
            return jsonify({'success': False, 'error': '无权访问'}), 403

        # 验证必填项
        questions = importer.get_survey_questions(submission['survey_id'])
        for question in questions:
            if question.get('requires_file') and question['id'] not in answers:
                return jsonify({
                    'success': False,
                    'error': f'问题"{question["question_text"]}"需要上传文件'
                }), 400

        # 保存答案
        if 'answers' not in db:
            db['answers'] = {}
        db['answers'][submission_id] = answers

        # 更新提交状态
        submission['status'] = 'submitted'
        submission['submitted_at'] = datetime.now().isoformat()
        submission['updated_at'] = datetime.now().isoformat()
        
        importer.save_db(db)

        return jsonify({
            'success': True,
            'message': '问卷已提交',
            'submission_id': submission_id,
            'submitted_at': submission['submitted_at']
        }), 200

    except Exception as e:
        logger.error(f"提交问卷出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# 文件上传接口
# ============================================================================

@questionnaire_bp.route('/submission/<submission_id>/upload', methods=['POST'])
@login_required
@enterprise_required
def upload_attachment(submission_id):
    """
    上传问卷附件（补充数据/说明）
    
    表单数据:
    - file: 文件
    - question_id: 问题ID
    """
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': '未找到文件'}), 400

        file = request.files['file']
        question_id = request.form.get('question_id')

        if not file or not question_id:
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        db = importer.load_db()
        
        # 查找提交记录
        submission = None
        for sub in db.get('submissions', []):
            if sub['id'] == submission_id:
                submission = sub
                break

        if not submission:
            return jsonify({'success': False, 'error': '问卷提交不存在'}), 404

        # 权限检查
        if submission['enterprise_id'] != session.get('enterprise_id'):
            return jsonify({'success': False, 'error': '无权访问'}), 403

        # 创建上传目录
        upload_dir = os.path.join('storage', 'questionnaire_uploads', submission_id)
        os.makedirs(upload_dir, exist_ok=True)

        # 保存文件
        filename = f"{question_id}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        # 记录附件信息
        if 'attachments' not in db:
            db['attachments'] = {}
        if submission_id not in db['attachments']:
            db['attachments'][submission_id] = []

        attachment = {
            'id': str(uuid.uuid4()),
            'question_id': question_id,
            'file_name': file.filename,
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'upload_time': datetime.now().isoformat()
        }
        db['attachments'][submission_id].append(attachment)
        importer.save_db(db)

        return jsonify({
            'success': True,
            'message': '文件上传成功',
            'attachment': attachment
        }), 201

    except Exception as e:
        logger.error(f"上传文件出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# 问卷管理接口
# ============================================================================

@questionnaire_bp.route('/survey/<survey_id>/delete', methods=['DELETE'])
def delete_survey(survey_id):
    """删除问卷"""
    try:
        importer.delete_survey(survey_id)
        return jsonify({
            'success': True,
            'message': '问卷已删除'
        }), 200
    except Exception as e:
        logger.error(f"删除问卷出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@questionnaire_bp.route('/submissions/list', methods=['GET'])
@login_required
def list_submissions():
    """获取当前用户的问卷提交列表"""
    try:
        enterprise_id = session.get('enterprise_id')
        db = importer.load_db()
        
        # 过滤当前企业的提交
        submissions = [
            sub for sub in db.get('submissions', [])
            if sub['enterprise_id'] == enterprise_id
        ]

        return jsonify({
            'success': True,
            'submissions': submissions,
            'total': len(submissions)
        }), 200

    except Exception as e:
        logger.error(f"获取提交列表出错: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

