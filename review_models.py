"""
审核功能数据模型
定义审核相关的数据结构和业务逻辑
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
import json


class ReviewStatus(Enum):
    """审核状态"""
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已批准
    REJECTED = "rejected"  # 已驳回
    PROMOTED = "promoted"  # 已晋级


class ReportType(Enum):
    """报告类型"""
    SELF_EVALUATION = "self_evaluation"  # 自评报告
    EXPERT_EVALUATION = "expert_evaluation"  # 专家评估报告
    REVIEW_REPORT = "review_report"  # 审核报告


@dataclass
class QuestionnaireAnswer:
    """问卷答案"""
    question_id: str
    question_text: str
    question_type: str  # 合规项、有效项、调节项
    answer: str
    score: Optional[float] = None
    comment: Optional[str] = None


@dataclass
class QuestionnaireData:
    """原始问卷数据"""
    questionnaire_id: str
    user_id: str
    user_type: str  # enterprise, expert, chamber_of_commerce
    user_level: str  # 当前级别
    submission_time: datetime
    answers: List[QuestionnaireAnswer] = field(default_factory=list)
    total_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'questionnaire_id': self.questionnaire_id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'user_level': self.user_level,
            'submission_time': self.submission_time.isoformat(),
            'answers': [asdict(a) for a in self.answers],
            'total_score': self.total_score
        }


@dataclass
class ReviewReport:
    """审核报告"""
    report_id: str
    questionnaire_id: str
    user_id: str
    user_name: str
    enterprise_name: str
    current_level: str  # 当前企业级别
    report_type: ReportType
    
    # 评分相关
    compliance_score: float  # 合规项得分
    effectiveness_score: float  # 有效项得分
    adjustment_score: Optional[float] = None  # 调节项得分
    total_score: float = 0.0
    
    # 审核相关
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewer_id: Optional[str] = None
    reviewer_name: Optional[str] = None
    review_time: Optional[datetime] = None
    review_comment: Optional[str] = None
    
    # 晋级相关
    promotion_eligible: bool = False  # 是否符合晋级条件
    recommended_level: Optional[str] = None  # 推荐晋级到的级别
    promotion_reason: Optional[str] = None  # 晋级原因
    
    # 时间戳
    created_time: datetime = field(default_factory=datetime.now)
    updated_time: datetime = field(default_factory=datetime.now)
    
    def calculate_total_score(self) -> float:
        """计算总分"""
        total = self.compliance_score + self.effectiveness_score
        if self.adjustment_score is not None:
            total += self.adjustment_score
        self.total_score = total
        return total
    
    def check_promotion_eligibility(self, promotion_thresholds: Dict[str, float]) -> bool:
        """
        检查是否符合晋级条件
        promotion_thresholds: {'advanced': 85, 'intermediate': 70}
        """
        threshold = promotion_thresholds.get(self.current_level, 0)
        self.promotion_eligible = self.total_score >= threshold
        return self.promotion_eligible
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'report_id': self.report_id,
            'questionnaire_id': self.questionnaire_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'enterprise_name': self.enterprise_name,
            'current_level': self.current_level,
            'report_type': self.report_type.value,
            'compliance_score': self.compliance_score,
            'effectiveness_score': self.effectiveness_score,
            'adjustment_score': self.adjustment_score,
            'total_score': self.total_score,
            'review_status': self.review_status.value,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer_name,
            'review_time': self.review_time.isoformat() if self.review_time else None,
            'review_comment': self.review_comment,
            'promotion_eligible': self.promotion_eligible,
            'recommended_level': self.recommended_level,
            'promotion_reason': self.promotion_reason,
            'created_time': self.created_time.isoformat(),
            'updated_time': self.updated_time.isoformat()
        }


@dataclass
class PromotionRecord:
    """晋级记录"""
    promotion_id: str
    user_id: str
    enterprise_name: str
    from_level: str  # 晋级前级别
    to_level: str  # 晋级后级别
    promotion_type: str  # 'automatic' 自动晋级, 'manual' 手动晋级
    reviewer_id: str  # 审核员ID
    reviewer_name: str  # 审核员名称
    reason: str  # 晋级原因
    report_id: Optional[str] = None  # 关联的报告ID
    promotion_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'promotion_id': self.promotion_id,
            'user_id': self.user_id,
            'enterprise_name': self.enterprise_name,
            'from_level': self.from_level,
            'to_level': self.to_level,
            'promotion_type': self.promotion_type,
            'reviewer_id': self.reviewer_id,
            'reviewer_name': self.reviewer_name,
            'reason': self.reason,
            'report_id': self.report_id,
            'promotion_time': self.promotion_time.isoformat()
        }


# 晋级阈值配置（企业用户）
ENTERPRISE_PROMOTION_THRESHOLDS = {
    'beginner': 70,  # 初级升中级需要70分
    'intermediate': 85,  # 中级升高级需要85分
}

# 晋级阈值配置（专家用户）
EXPERT_PROMOTION_THRESHOLDS = {
    'junior': 75,  # 初级升中级需要75分
    'intermediate': 88,  # 中级升高级需要88分
}

# 晋级配置
PROMOTION_CONFIG = {
    'enterprise': {
        'thresholds': ENTERPRISE_PROMOTION_THRESHOLDS,
        'level_order': ['beginner', 'intermediate', 'advanced'],
        'max_level': 'advanced'
    },
    'expert': {
        'thresholds': EXPERT_PROMOTION_THRESHOLDS,
        'level_order': ['junior', 'intermediate', 'senior'],
        'max_level': 'senior'
    }
}

