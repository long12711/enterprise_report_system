"""
专项反馈管理 - Flask API 实现
文件: special_feedback_api.py
描述: 提供专项反馈管理的完整API实现
"""

from flask import Blueprint, request, jsonify, session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta
import uuid
import json

# 创建蓝图
special_feedback_bp = Blueprint('special_feedback', __name__, url_prefix='/api/portal/chamber/feedbacks')


# ============================================================
# 子分类映射
# ============================================================

SUBCATEGORIES = {
    'typical_case': ['党建', '文化建设', '社会责任', '创新发展', '人才培养', '其他'],
    'issue_feedback': ['经营问题', '管理问题', '技术问题', '其他问题'],
    'chamber_feedback': ['政策建议', '服务评价', '合作建议', '其他反馈'],
    'expert_feedback': ['技术评价', '管理评价', '发展评价', '其他评价'],
    'material': ['财务报表', '荣誉证书', '项目成果', '其他材料']
}

CATEGORY_NAMES = {
    'typical_case': '典型案例',
    'issue_feedback': '问题意见反馈',
    'chamber_feedback': '工商联反馈',
    'expert_feedback': '专家评价反馈',
    'material': '自评报告佐证材料'
}


# ============================================================
# API 端点
# ============================================================

@special_feedback_bp.route('', methods=['GET'])
def get_feedbacks():
    """获取反馈列表"""
    try:
        from models import SpecialFeedback
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        keyword = request.args.get('keyword', '')
        category = request.args.get('category', '')
        status = request.args.get('status', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # 构建查询
        query = db.session.query(SpecialFeedback)
        
        # 条件过滤
        if keyword:
            query = query.filter(
                or_(
                    SpecialFeedback.title.ilike(f'%{keyword}%'),
                    SpecialFeedback.content.ilike(f'%{keyword}%')
                )
            )
        
        if category:
            query = query.filter(SpecialFeedback.category == category)
        
        if status:
            query = query.filter(SpecialFeedback.status == status)
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        # 排序和分页
        total = query.count()
        feedbacks = query.order_by(SpecialFeedback.submitted_at.desc()) \
                         .offset((page - 1) * limit) \
                         .limit(limit) \
                         .all()
        
        feedback_list = []
        for fb in feedbacks:
            feedback_list.append({
                'id': fb.id,
                'category': fb.category,
                'category_name': CATEGORY_NAMES.get(fb.category, ''),
                'subcategory': fb.subcategory,
                'title': fb.title,
                'enterprise_name': fb.enterprise_name,
                'status': fb.status,
                'rating': fb.rating,
                'submitted_at': fb.submitted_at.isoformat() if fb.submitted_at else None
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'page': page,
                'limit': limit,
                'feedbacks': feedback_list
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('', methods=['POST'])
def create_feedback():
    """创建反馈"""
    try:
        from models import SpecialFeedback
        
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['category', 'subcategory', 'title', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400
        
        # 创建反馈
        feedback = SpecialFeedback(
            id=str(uuid.uuid4()),
            category=data['category'],
            subcategory=data['subcategory'],
            title=data['title'],
            content=data['content'],
            enterprise_id=data.get('enterprise_id'),
            enterprise_name=data.get('enterprise_name'),
            status=data.get('status', 'draft'),
            priority=data.get('priority', 'medium'),
            attachments=json.dumps(data.get('attachments', [])),
            file_count=len(data.get('attachments', [])),
            tags=json.dumps(data.get('tags', [])),
            remark=data.get('remark')
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'id': feedback.id,
                'message': '反馈创建成功'
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """获取反馈详情"""
    try:
        from models import SpecialFeedback
        
        feedback = db.session.query(SpecialFeedback).filter_by(id=feedback_id).first()
        if not feedback:
            return jsonify({'success': False, 'error': '反馈不存在'}), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': feedback.id,
                'category': feedback.category,
                'subcategory': feedback.subcategory,
                'title': feedback.title,
                'content': feedback.content,
                'enterprise_name': feedback.enterprise_name,
                'status': feedback.status,
                'rating': feedback.rating,
                'priority': feedback.priority,
                'attachments': json.loads(feedback.attachments) if feedback.attachments else [],
                'tags': json.loads(feedback.tags) if feedback.tags else [],
                'submitted_at': feedback.submitted_at.isoformat() if feedback.submitted_at else None,
                'reviewed_at': feedback.reviewed_at.isoformat() if feedback.reviewed_at else None,
                'reviewer_name': feedback.reviewer_name,
                'review_comment': feedback.review_comment
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/<feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    """更新反馈"""
    try:
        from models import SpecialFeedback
        
        feedback = db.session.query(SpecialFeedback).filter_by(id=feedback_id).first()
        if not feedback:
            return jsonify({'success': False, 'error': '反馈不存在'}), 404
        
        data = request.get_json()
        
        # 更新字段
        if 'title' in data:
            feedback.title = data['title']
        
        if 'content' in data:
            feedback.content = data['content']
        
        if 'status' in data:
            feedback.status = data['status']
        
        if 'rating' in data:
            feedback.rating = data['rating']
        
        if 'priority' in data:
            feedback.priority = data['priority']
        
        if 'review_comment' in data:
            feedback.review_comment = data['review_comment']
            feedback.reviewed_at = datetime.now()
        
        feedback.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {'id': feedback_id, 'message': '反馈更新成功'}
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """删除反馈"""
    try:
        from models import SpecialFeedback
        
        feedback = db.session.query(SpecialFeedback).filter_by(id=feedback_id).first()
        if not feedback:
            return jsonify({'success': False, 'error': '反馈不存在'}), 404
        
        db.session.delete(feedback)
        db.session.commit()
        
        return jsonify({'success': True, 'message': '反馈删除成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# 分析接口
# ============================================================

@special_feedback_bp.route('/analysis/category', methods=['GET'])
def analyze_category():
    """分类分析"""
    try:
        from models import SpecialFeedback
        
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = db.session.query(SpecialFeedback)
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        # 按分类统计
        category_stats = db.session.query(
            SpecialFeedback.category,
            func.count(SpecialFeedback.id).label('count')
        ).filter(
            (SpecialFeedback.submitted_at >= date_from) if date_from else True,
            (SpecialFeedback.submitted_at <= date_to) if date_to else True
        ).group_by(SpecialFeedback.category).all()
        
        total = sum([stat[1] for stat in category_stats])
        
        categories = {}
        percentages = {}
        for category, count in category_stats:
            cat_name = CATEGORY_NAMES.get(category, category)
            categories[cat_name] = count
            percentages[cat_name] = round(count / total * 100, 2) if total > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'categories': categories,
                'percentage': percentages
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/analysis/trend', methods=['GET'])
def analyze_trend():
    """时间趋势分析"""
    try:
        from models import SpecialFeedback
        
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        period = request.args.get('period', 'day')  # day, week, month
        
        query = db.session.query(SpecialFeedback)
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        feedbacks = query.all()
        
        # 按日期分组
        trend_data = {}
        for fb in feedbacks:
            if fb.submitted_at:
                if period == 'day':
                    date_key = fb.submitted_at.strftime('%Y-%m-%d')
                elif period == 'week':
                    date_key = fb.submitted_at.strftime('%Y-W%W')
                else:  # month
                    date_key = fb.submitted_at.strftime('%Y-%m')
                
                trend_data[date_key] = trend_data.get(date_key, 0) + 1
        
        trend_list = [
            {'date': date, 'count': count}
            for date, count in sorted(trend_data.items())
        ]
        
        return jsonify({
            'success': True,
            'data': {'trend': trend_list}
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/analysis/rating', methods=['GET'])
def analyze_rating():
    """评分分析"""
    try:
        from models import SpecialFeedback
        
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = db.session.query(SpecialFeedback)
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        feedbacks = query.filter(SpecialFeedback.rating.isnot(None)).all()
        
        # 计算平均评分
        ratings = [fb.rating for fb in feedbacks if fb.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # 分布统计
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            if rating in distribution:
                distribution[rating] += 1
        
        return jsonify({
            'success': True,
            'data': {
                'average_rating': round(avg_rating, 2),
                'distribution': distribution
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/analysis/metrics', methods=['GET'])
def analyze_metrics():
    """关键指标分析"""
    try:
        from models import SpecialFeedback
        
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = db.session.query(SpecialFeedback)
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        feedbacks = query.all()
        total = len(feedbacks)
        
        # 计算指标
        approved_count = len([f for f in feedbacks if f.status == 'approved'])
        approval_rate = approved_count / total if total > 0 else 0
        
        ratings = [f.rating for f in feedbacks if f.rating]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        # 计算平均处理时间
        processing_times = []
        for f in feedbacks:
            if f.submitted_at and f.reviewed_at:
                delta = f.reviewed_at - f.submitted_at
                processing_times.append(delta.days)
        
        avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        high_priority_count = len([f for f in feedbacks if f.priority == 'urgent'])
        high_priority_ratio = high_priority_count / total if total > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_feedbacks': total,
                'average_rating': round(avg_rating, 2),
                'approval_rate': round(approval_rate, 2),
                'avg_processing_time': round(avg_processing_time, 1),
                'high_priority_ratio': round(high_priority_ratio, 2)
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@special_feedback_bp.route('/analysis/issues', methods=['GET'])
def analyze_issues():
    """问题分析"""
    try:
        from models import SpecialFeedback
        
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        query = db.session.query(SpecialFeedback).filter(
            SpecialFeedback.category == 'issue_feedback'
        )
        
        if date_from:
            query = query.filter(SpecialFeedback.submitted_at >= date_from)
        
        if date_to:
            query = query.filter(SpecialFeedback.submitted_at <= date_to)
        
        # 按子分类统计
        issue_stats = db.session.query(
            SpecialFeedback.subcategory,
            func.count(SpecialFeedback.id).label('count')
        ).filter(
            SpecialFeedback.category == 'issue_feedback',
            (SpecialFeedback.submitted_at >= date_from) if date_from else True,
            (SpecialFeedback.submitted_at <= date_to) if date_to else True
        ).group_by(SpecialFeedback.subcategory).all()
        
        total_issues = sum([stat[1] for stat in issue_stats])
        
        issues = []
        for subcategory, count in issue_stats:
            issues.append({
                'category': subcategory,
                'count': count,
                'percentage': round(count / total_issues * 100, 2) if total_issues > 0 else 0
            })
        
        return jsonify({
            'success': True,
            'data': {
                'total_issues': total_issues,
                'issues': issues
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================
# 蓝图注册
# ============================================================

def register_special_feedback_api(app):
    """注册专项反馈管理API"""
    app.register_blueprint(special_feedback_bp)

