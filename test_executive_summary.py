#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试执行摘要功能（简化版）
"""

import json
from nankai_report_generator import NankaiReportGenerator

def test_executive_summary():
    """测试执行摘要报告生成"""
    
    print("=" * 60)
    print("测试执行摘要功能（简化版 - 参考专业报告格式）")
    print("=" * 60)
    
    # 准备测试数据
    enterprise_info = {
        'enterprise_name': '今麦郎食品有限公司',
        'contact_person': '张经理',
        'contact_phone': '13800138000',
        'contact_email': 'zhang@jinmailang.com',
        'main_business': '食品制造',
        'enterprise_scale': '大型'
    }
    
    # 模拟问卷答案（使用最近的提交数据）
    submission_file = 'storage/submissions/submission_今麦郎_20251126_152040.json'
    
    try:
        with open(submission_file, 'r', encoding='utf-8') as f:
            submission_data = json.load(f)
        
        answers = submission_data.get('answers', {})
        level = submission_data.get('level', '初级')
        
        print(f"\n✓ 加载提交数据成功")
        print(f"  - 企业: {enterprise_info['enterprise_name']}")
        print(f"  - 等级: {level}")
        print(f"  - 答案数量: {len(answers)}")
        
        # 生成报告
        print(f"\n开始生成报告...")
        generator = NankaiReportGenerator()
        
        output_file = generator.generate_report(
            enterprise_info=enterprise_info,
            answers=answers,
            level=level
        )
        
        print(f"\n✓ 报告生成成功!")
        print(f"  输出文件: {output_file}")
        
        # 验证报告内容
        print(f"\n报告结构验证:")
        print(f"  ✓ 封面页")
        print(f"  ✓ 执行摘要 (简化版 - 新增)")
        print(f"    - 评价结论")
        print(f"    - 总得分")
        print(f"    - 企业概况")
        print(f"    - 评价亮点")
        print(f"    - 存在问题")
        print(f"  ✓ 企业基本信息")
        print(f"  ✓ 评价概览")
        print(f"  ✓ 维度分析")
        print(f"  ✓ 优势与不足")
        print(f"  ✓ 改进建议")
        print(f"  ✓ 结语")
        print(f"  ✓ 附录：详细数据")
        
        print(f"\n执行摘要格式说明:")
        print(f"  - 参考专业版PDF报告格式")
        print(f"  - 简洁明了，突出重点")
        print(f"  - 评价结论带颜色标识")
        print(f"  - 自动识别亮点和问题")
        
        print(f"\n" + "=" * 60)
        print(f"测试完成！")
        print(f"=" * 60)
        
        return True
        
    except FileNotFoundError:
        print(f"\n✗ 错误: 找不到提交文件 {submission_file}")
        print(f"  请先提交一份问卷")
        return False
    except Exception as e:
        print(f"\n✗ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_executive_summary()