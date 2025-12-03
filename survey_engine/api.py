# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Blueprint, request, jsonify
from .services.loader import SurveyLoader

api_bp = Blueprint('survey_api', __name__)
_loader = SurveyLoader()


@api_bp.route('/get_questions', methods=['GET'])
def get_questions():
    try:
        user_type = request.args.get('user_type')
        user_level = request.args.get('user_level')
        excel_level = request.args.get('excel_level')  # beginner|intermediate|advanced（可选直指sheet）

        level_key = _loader.resolve_level_key(user_type, user_level, excel_level)

        questions = _loader.get_questions(level_key)
        source_file = _loader.nk_excel_path

        return jsonify({
            'success': True,
            'questions': questions,
            'user_type': user_type,
            'user_level': user_level,
            'excel_level': level_key,
            'source_file': source_file,
            'total_questions': len(questions)
        })
    except FileNotFoundError as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'获取问卷题目失败: {str(e)}'}), 500


@api_bp.route('/health', methods=['GET'])
def health():
    try:
        path = _loader.nk_excel_path
        exists = bool(path) and __import__('os').path.exists(path)
        result = {
            'success': True,
            'nk_excel_path': path,
            'file_exists': exists,
        }
        if exists:
            try:
                overview = {}
                for lv in ['beginner', 'intermediate', 'advanced']:
                    qs = _loader.get_questions(lv)
                    overview[lv] = len(qs)
                result['overview'] = overview
            except Exception as e:
                result['overview_error'] = str(e)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@api_bp.route('/indicators/overview', methods=['GET'])
def indicators_overview():
    try:
        import os
        path = _loader.nk_excel_path
        if not path or not os.path.exists(path):
            return jsonify({'success': False, 'error': '指标文件不存在'}), 500
        data = {}
        for lv in ['beginner', 'intermediate', 'advanced']:
            qs = _loader.get_questions(lv)
            data[lv] = {
                'count': len(qs),
                'samples': qs[:3]
            }
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

