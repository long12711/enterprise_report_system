"""
审核功能服务层
处理审核相关的业务逻辑
"""

from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import uuid
from review_models import (
    ReviewReport, ReviewStatus, ReportType, QuestionnaireData,
    QuestionnaireAnswer, PromotionRecord, PROMOTION_CONFIG
)


class ReviewService:
    """审核服务"""
    
    def __init__(self):
        """初始化审核服务"""
        # 模拟数据存储（实际应使用数据库）
        self.reports: Dict[str, ReviewReport] = {}
        self.questionnaires: Dict[str, QuestionnaireData] = {}
        self.promotion_records: Dict[str, PromotionRecord] = {}
    
    # ==================== 报告管理 ====================
    
    def create_review_report(
        self,
        questionnaire_id: str,
        user_id: str,
        user_name: str,
        enterprise_name: str,
        current_level: str,
        compliance_score: float,
        effectiveness_score: float,
        adjustment_score: Optional[float] = None,
        report_type: ReportType = ReportType.REVIEW_REPORT
    ) -> ReviewReport:
        """创建审核报告"""
        report_id = f"report_{uuid.uuid4().hex[:12]}"
        
        report = ReviewReport(
            report_id=report_id,
            questionnaire_id=questionnaire_id,
            user_id=user_id,
            user_name=user_name,
            enterprise_name=enterprise_name,
            current_level=current_level,
            report_type=report_type,
            compliance_score=compliance_score,
            effectiveness_score=effectiveness_score,
            adjustment_score=adjustment_score
        )
        
        # 计算总分
        report.calculate_total_score()
        
        # 存储报告
        self.reports[report_id] = report
        
        return report
    
    def get_review_report(self, report_id: str) -> Optional[ReviewReport]:
        """获取审核报告"""
        return self.reports.get(report_id)
    
    def get_reports_by_status(self, status: ReviewStatus) -> List[ReviewReport]:
        """按状态获取报告列表"""
        return [
            report for report in self.reports.values()
            if report.review_status == status
        ]
    
    def get_pending_reviews(self) -> List[ReviewReport]:
        """获取待审核的报告"""
        return self.get_reports_by_status(ReviewStatus.PENDING)
    
    def get_reports_by_user(self, user_id: str) -> List[ReviewReport]:
        """获取特定用户的所有报告"""
        return [
            report for report in self.reports.values()
            if report.user_id == user_id
        ]
    
    # ==================== 问卷管理 ====================
    
    def store_questionnaire(
        self,
        questionnaire_id: str,
        user_id: str,
        user_type: str,
        user_level: str,
        answers: List[Dict[str, Any]]
    ) -> QuestionnaireData:
        """存储原始问卷数据"""
        answer_objects = [
            QuestionnaireAnswer(
                question_id=a['question_id'],
                question_text=a['question_text'],
                question_type=a['question_type'],
                answer=a['answer'],
                score=a.get('score'),
                comment=a.get('comment')
            )
            for a in answers
        ]
        
        questionnaire = QuestionnaireData(
            questionnaire_id=questionnaire_id,
            user_id=user_id,
            user_type=user_type,
            user_level=user_level,
            submission_time=datetime.now(),
            answers=answer_objects
        )
        
        # 计算总分
        total_score = sum(a.score for a in answer_objects if a.score)
        questionnaire.total_score = total_score
        
        self.questionnaires[questionnaire_id] = questionnaire
        return questionnaire
    
    def get_questionnaire(self, questionnaire_id: str) -> Optional[QuestionnaireData]:
        """获取原始问卷数据"""
        return self.questionnaires.get(questionnaire_id)
    
    def get_questionnaire_by_report(self, report_id: str) -> Optional[QuestionnaireData]:
        """通过报告ID获取对应的问卷"""
        report = self.get_review_report(report_id)
        if report:
            return self.get_questionnaire(report.questionnaire_id)
        return None
    
    # ==================== 审核操作 ====================
    
    def submit_review(
        self,
        report_id: str,
        reviewer_id: str,
        reviewer_name: str,
        status: ReviewStatus,
        comment: Optional[str] = None,
        user_type: str = 'enterprise'
    ) -> Tuple[bool, str, ReviewReport]:
        """
        提交审核结果
        
        Args:
            report_id: 报告ID
            reviewer_id: 审核员ID
            reviewer_name: 审核员名称
            status: 审核状态
            comment: 审核意见
            user_type: 用户类型
        
        Returns:
            (success, message, report)
        """
        report = self.get_review_report(report_id)
        if not report:
            return False, "报告不存在", None
        
        # 更新报告状态
        report.review_status = status
        report.reviewer_id = reviewer_id
        report.reviewer_name = reviewer_name
        report.review_time = datetime.now()
        report.review_comment = comment
        report.updated_time = datetime.now()
        
        # 检查晋级资格
        if status == ReviewStatus.APPROVED:
            promotion_config = PROMOTION_CONFIG.get(user_type)
            if promotion_config:
                thresholds = promotion_config['thresholds']
                report.check_promotion_eligibility(thresholds)
                
                # 确定推荐晋级级别
                if report.promotion_eligible:
                    level_order = promotion_config['level_order']
                    current_index = level_order.index(report.current_level)
                    if current_index < len(level_order) - 1:
                        report.recommended_level = level_order[current_index + 1]
                        report.promotion_reason = f"评分{report.total_score}分，达到晋级标准"
        
        return True, "审核提交成功", report
    
    def approve_review(
        self,
        report_id: str,
        reviewer_id: str,
        reviewer_name: str,
        comment: Optional[str] = None,
        user_type: str = 'enterprise'
    ) -> Tuple[bool, str, ReviewReport]:
        """批准审核"""
        return self.submit_review(
            report_id, reviewer_id, reviewer_name,
            ReviewStatus.APPROVED, comment, user_type
        )
    
    def reject_review(
        self,
        report_id: str,
        reviewer_id: str,
        reviewer_name: str,
        comment: str,
        user_type: str = 'enterprise'
    ) -> Tuple[bool, str, ReviewReport]:
        """驳回审核"""
        return self.submit_review(
            report_id, reviewer_id, reviewer_name,
            ReviewStatus.REJECTED, comment, user_type
        )
    
    # ==================== 晋级操作 ====================
    
    def promote_user(
        self,
        report_id: str,
        reviewer_id: str,
        reviewer_name: str,
        reason: str,
        user_type: str = 'enterprise'
    ) -> Tuple[bool, str, Optional[PromotionRecord]]:
        """
        手动晋级用户
        
        Args:
            report_id: 报告ID
            reviewer_id: 审核员ID
            reviewer_name: 审核员名称
            reason: 晋级原因
            user_type: 用户类型
        
        Returns:
            (success, message, promotion_record)
        """
        report = self.get_review_report(report_id)
        if not report:
            return False, "报告不存在", None
        
        # 检查是否已经是最高级
        promotion_config = PROMOTION_CONFIG.get(user_type)
        if not promotion_config:
            return False, f"不支持的用户类型: {user_type}", None
        
        level_order = promotion_config['level_order']
        max_level = promotion_config['max_level']
        
        if report.current_level == max_level:
            return False, f"已是最高级别({max_level})，无法晋级", None
        
        # 获取下一级别
        try:
            current_index = level_order.index(report.current_level)
            next_level = level_order[current_index + 1]
        except (ValueError, IndexError):
            return False, "无法确定晋级级别", None
        
        # 创建晋级记录
        promotion_id = f"promotion_{uuid.uuid4().hex[:12]}"
        promotion_record = PromotionRecord(
            promotion_id=promotion_id,
            user_id=report.user_id,
            enterprise_name=report.enterprise_name,
            from_level=report.current_level,
            to_level=next_level,
            promotion_type='manual',
            reviewer_id=reviewer_id,
            reviewer_name=reviewer_name,
            reason=reason,
            report_id=report_id
        )
        
        # 存储晋级记录
        self.promotion_records[promotion_id] = promotion_record
        
        # 更新报告状态
        report.review_status = ReviewStatus.PROMOTED
        report.updated_time = datetime.now()
        
        return True, f"成功晋级为{next_level}", promotion_record
    
    def get_promotion_records(self, user_id: str) -> List[PromotionRecord]:
        """获取用户的晋级记录"""
        return [
            record for record in self.promotion_records.values()
            if record.user_id == user_id
        ]
    
    def get_promotion_record(self, promotion_id: str) -> Optional[PromotionRecord]:
        """获取晋级记录详情"""
        return self.promotion_records.get(promotion_id)
    
    # ==================== 统计分析 ====================
    
    def get_review_statistics(self) -> Dict[str, Any]:
        """获取审核统计信息"""
        total_reports = len(self.reports)
        pending = len(self.get_reports_by_status(ReviewStatus.PENDING))
        approved = len(self.get_reports_by_status(ReviewStatus.APPROVED))
        rejected = len(self.get_reports_by_status(ReviewStatus.REJECTED))
        promoted = len(self.get_reports_by_status(ReviewStatus.PROMOTED))
        
        return {
            'total_reports': total_reports,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'promoted': promoted,
            'approval_rate': approved / total_reports if total_reports > 0 else 0,
            'promotion_rate': promoted / total_reports if total_reports > 0 else 0
        }
    
    def get_average_scores(self) -> Dict[str, float]:
        """获取平均评分"""
        if not self.reports:
            return {}
        
        total_compliance = sum(r.compliance_score for r in self.reports.values())
        total_effectiveness = sum(r.effectiveness_score for r in self.reports.values())
        total_score = sum(r.total_score for r in self.reports.values())
        count = len(self.reports)
        
        return {
            'avg_compliance_score': total_compliance / count,
            'avg_effectiveness_score': total_effectiveness / count,
            'avg_total_score': total_score / count
        }


# 创建全局服务实例
review_service = ReviewService()

