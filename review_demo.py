"""
审核功能演示脚本
展示如何使用审核功能的各个部分
"""

from datetime import datetime
from review_service import review_service
from review_models import ReportType, ReviewStatus, QuestionnaireAnswer


def demo_create_questionnaire():
    """演示：创建和存储问卷"""
    print("=" * 60)
    print("演示1: 创建和存储问卷")
    print("=" * 60)
    
    # 创建问卷答案
    answers = [
        {
            'question_id': 'q001',
            'question_text': '企业是否建立了党的组织？',
            'question_type': '合规项',
            'answer': '是',
            'score': 10.0
        },
        {
            'question_id': 'q002',
            'question_text': '企业是否有完善的公司治理结构？',
            'question_type': '合规项',
            'answer': '是',
            'score': 10.0
        },
        {
            'question_id': 'q003',
            'question_text': '企业是否定期召开股东大会？',
            'question_type': '有效项',
            'answer': '是',
            'score': 8.0
        },
        {
            'question_id': 'q004',
            'question_text': '企业员工满意度是否高于80%？',
            'question_type': '调节项',
            'answer': '是',
            'score': 5.0
        },
    ]
    
    # 存储问卷
    questionnaire = review_service.store_questionnaire(
        questionnaire_id='qn_001',
        user_id='user_001',
        user_type='enterprise',
        user_level='beginner',
        answers=answers
    )
    
    print(f"✓ 问卷已创建: {questionnaire.questionnaire_id}")
    print(f"  用户ID: {questionnaire.user_id}")
    print(f"  用户类型: {questionnaire.user_type}")
    print(f"  用户级别: {questionnaire.user_level}")
    print(f"  总分: {questionnaire.total_score:.2f}")
    print(f"  答案数: {len(questionnaire.answers)}")
    print()


def demo_create_report():
    """演示：创建审核报告"""
    print("=" * 60)
    print("演示2: 创建审核报告")
    print("=" * 60)
    
    report = review_service.create_review_report(
        questionnaire_id='qn_001',
        user_id='user_001',
        user_name='张三',
        enterprise_name='示例企业有限公司',
        current_level='beginner',
        compliance_score=20.0,
        effectiveness_score=8.0,
        adjustment_score=5.0,
        report_type=ReportType.REVIEW_REPORT
    )
    
    print(f"✓ 报告已创建: {report.report_id}")
    print(f"  企业名称: {report.enterprise_name}")
    print(f"  当前级别: {report.current_level}")
    print(f"  合规项得分: {report.compliance_score:.2f}")
    print(f"  有效项得分: {report.effectiveness_score:.2f}")
    print(f"  调节项得分: {report.adjustment_score:.2f}")
    print(f"  总分: {report.total_score:.2f}")
    print(f"  审核状态: {report.review_status.value}")
    print()
    
    return report.report_id


def demo_approve_review(report_id):
    """演示：批准审核"""
    print("=" * 60)
    print("演示3: 批准审核")
    print("=" * 60)
    
    success, message, report = review_service.approve_review(
        report_id=report_id,
        reviewer_id='reviewer_001',
        reviewer_name='李四',
        comment='企业表现良好，符合晋级条件',
        user_type='enterprise'
    )
    
    if success:
        print(f"✓ {message}")
        print(f"  审核员: {report.reviewer_name}")
        print(f"  审核时间: {report.review_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  审核状态: {report.review_status.value}")
        print(f"  符合晋级条件: {'是' if report.promotion_eligible else '否'}")
        if report.recommended_level:
            print(f"  推荐晋级级别: {report.recommended_level}")
            print(f"  晋级原因: {report.promotion_reason}")
    else:
        print(f"✗ {message}")
    print()


def demo_promote_user(report_id):
    """演示：手动晋级用户"""
    print("=" * 60)
    print("演示4: 手动晋级用户")
    print("=" * 60)
    
    success, message, promotion_record = review_service.promote_user(
        report_id=report_id,
        reviewer_id='reviewer_001',
        reviewer_name='李四',
        reason='企业综合表现优秀，符合晋级标准，予以晋级',
        user_type='enterprise'
    )
    
    if success:
        print(f"✓ {message}")
        print(f"  晋级记录ID: {promotion_record.promotion_id}")
        print(f"  企业名称: {promotion_record.enterprise_name}")
        print(f"  晋级前级别: {promotion_record.from_level}")
        print(f"  晋级后级别: {promotion_record.to_level}")
        print(f"  晋级类型: {promotion_record.promotion_type}")
        print(f"  审核员: {promotion_record.reviewer_name}")
        print(f"  晋级时间: {promotion_record.promotion_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"✗ {message}")
    print()


def demo_view_questionnaire(report_id):
    """演示：查看原问卷"""
    print("=" * 60)
    print("演示5: 查看原问卷")
    print("=" * 60)
    
    questionnaire = review_service.get_questionnaire_by_report(report_id)
    
    if questionnaire:
        print(f"✓ 问卷信息:")
        print(f"  问卷ID: {questionnaire.questionnaire_id}")
        print(f"  用户ID: {questionnaire.user_id}")
        print(f"  用户类型: {questionnaire.user_type}")
        print(f"  用户级别: {questionnaire.user_level}")
        print(f"  提交时间: {questionnaire.submission_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  总分: {questionnaire.total_score:.2f}")
        print(f"\n  答案详情:")
        for i, answer in enumerate(questionnaire.answers, 1):
            print(f"    {i}. {answer.question_text}")
            print(f"       类型: {answer.question_type}")
            print(f"       答案: {answer.answer}")
            print(f"       得分: {answer.score:.2f}")
    else:
        print("✗ 问卷不存在")
    print()


def demo_view_report(report_id):
    """演示：查看报告"""
    print("=" * 60)
    print("演示6: 查看报告")
    print("=" * 60)
    
    report = review_service.get_review_report(report_id)
    
    if report:
        print(f"✓ 报告信息:")
        print(f"  报告ID: {report.report_id}")
        print(f"  企业名称: {report.enterprise_name}")
        print(f"  联系人: {report.user_name}")
        print(f"  当前级别: {report.current_level}")
        print(f"  报告类型: {report.report_type.value}")
        print(f"  审核状态: {report.review_status.value}")
        print(f"\n  评分信息:")
        print(f"    合规项得分: {report.compliance_score:.2f}")
        print(f"    有效项得分: {report.effectiveness_score:.2f}")
        if report.adjustment_score:
            print(f"    调节项得分: {report.adjustment_score:.2f}")
        print(f"    总分: {report.total_score:.2f}")
        if report.review_comment:
            print(f"\n  审核意见: {report.review_comment}")
    else:
        print("✗ 报告不存在")
    print()


def demo_statistics():
    """演示：审核统计"""
    print("=" * 60)
    print("演示7: 审核统计")
    print("=" * 60)
    
    stats = review_service.get_review_statistics()
    
    print(f"✓ 审核统计信息:")
    print(f"  总报告数: {stats['total_reports']}")
    print(f"  待审核: {stats['pending']}")
    print(f"  已批准: {stats['approved']}")
    print(f"  已驳回: {stats['rejected']}")
    print(f"  已晋级: {stats['promoted']}")
    print(f"  批准率: {stats['approval_rate']:.2%}")
    print(f"  晋级率: {stats['promotion_rate']:.2%}")
    print()
    
    scores = review_service.get_average_scores()
    print(f"✓ 平均评分:")
    print(f"  平均合规项得分: {scores.get('avg_compliance_score', 0):.2f}")
    print(f"  平均有效项得分: {scores.get('avg_effectiveness_score', 0):.2f}")
    print(f"  平均总分: {scores.get('avg_total_score', 0):.2f}")
    print()


def demo_reject_review():
    """演示：驳回审核"""
    print("=" * 60)
    print("演示8: 驳回审核")
    print("=" * 60)
    
    # 创建另一个报告用于演示驳回
    report = review_service.create_review_report(
        questionnaire_id='qn_002',
        user_id='user_002',
        user_name='王五',
        enterprise_name='另一个企业有限公司',
        current_level='intermediate',
        compliance_score=15.0,
        effectiveness_score=5.0,
        adjustment_score=2.0,
        report_type=ReportType.REVIEW_REPORT
    )
    
    success, message, report = review_service.reject_review(
        report_id=report.report_id,
        reviewer_id='reviewer_001',
        reviewer_name='李四',
        comment='企业部分指标不符合要求，建议重新整改后再次提交',
        user_type='enterprise'
    )
    
    if success:
        print(f"✓ {message}")
        print(f"  报告ID: {report.report_id}")
        print(f"  企业名称: {report.enterprise_name}")
        print(f"  审核状态: {report.review_status.value}")
        print(f"  审核意见: {report.review_comment}")
    else:
        print(f"✗ {message}")
    print()


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  审核功能演示程序".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # 演示流程
    demo_create_questionnaire()
    report_id = demo_create_report()
    demo_view_report(report_id)
    demo_view_questionnaire(report_id)
    demo_approve_review(report_id)
    demo_promote_user(report_id)
    demo_statistics()
    demo_reject_review()
    
    print("=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

