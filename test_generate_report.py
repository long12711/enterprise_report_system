"""
自动填写测试问卷并生成报告
用于测试报告模板样式
"""

import json
import os
import sys
from datetime import datetime
import pandas as pd

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nankai_report_generator import NankaiReportGenerator
from nankai_scoring_engine import NankaiScoringEngine

def create_test_submission():
    """创建测试问卷提交数据"""
    
    # 指标文件路径
    indicator_file = 'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx'
    
    # 读取初级问卷指标
    df = pd.read_excel(indicator_file, sheet_name='初级')
    
    # 创建测试答案（模拟一个得分约75%的企业）
    answers = {}
    partial_details = {}
    
    for idx, row in df.iterrows():
        q_id = str(int(row['序号'])) if pd.notna(row['序号']) else str(idx + 1)
        
        # 根据题号分配不同的答案，模拟真实情况
        if idx % 5 == 0:
            # 20%的题目选C（未完成）
            answers[q_id] = 'C. 均未完成'
        elif idx % 3 == 0:
            # 约33%的题目选B（部分完成）
            answers[q_id] = 'B. 部分完成'
            # 为部分完成的题目添加详细说明
            partial_details[q_id] = f'该项工作已启动，目前完成了基础框架的搭建，正在逐步完善相关制度和流程。预计在未来3-6个月内全面完成。已投入专项资金约50万元，配备专职人员2名。'
        else:
            # 约47%的题目选A（已完成）
            answers[q_id] = 'A. 全部完成'
    
    # 企业基本信息
    enterprise_info = {
        'enterprise_name': '测试科技股份有限公司',
        'contact_person': '张经理',
        'contact_phone': '13800138000',
        'contact_email': 'test@example.com',
        'main_business': '软件和信息技术服务业',
        'enterprise_scale': '中型',
        'establishment_years': '8',
        'annual_revenue': '5000',
        'rd_investment': '500',
        'rd_ratio': '10'
    }
    
    # 使用评分引擎计算得分
    print("[INFO] 正在计算得分...")
    scoring_engine = NankaiScoringEngine(indicator_file)
    score_result = scoring_engine.calculate_score(
        level='初级',
        answers=answers,
        partial_details=partial_details
    )
    
    print(f"[OK] 得分计算完成：{score_result['percentage']:.2f}分")
    
    # 创建提交数据
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    submission_data = {
        'timestamp': timestamp,
        'level': '初级',
        'enterprise_info': enterprise_info,
        'answers': answers,
        'partial_details': partial_details,
        'score': score_result,
        'submitted_at': datetime.now().isoformat()
    }
    
    # 保存提交数据
    os.makedirs('storage/nankai_submissions', exist_ok=True)
    submission_file = f'storage/nankai_submissions/submission_测试企业_{timestamp}.json'
    
    with open(submission_file, 'w', encoding='utf-8') as f:
        json.dump(submission_data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] 测试问卷数据已保存: {submission_file}")
    
    return submission_file, score_result

def generate_test_report(submission_file):
    """生成测试报告"""
    
    print("\n" + "=" * 80)
    print("开始生成测试报告...")
    print("=" * 80)
    
    # 创建报告生成器
    indicator_file = 'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx'
    generator = NankaiReportGenerator(indicator_file=indicator_file)
    
    # 生成报告（Word + PDF）
    print("\n[INFO] 正在生成专业评价报告...")
    report_path = generator.generate_report(submission_file, generate_pdf=True)
    
    print(f"\n[SUCCESS] 报告生成成功！")
    print(f"报告路径: {report_path}")
    
    # 获取文件大小
    file_size = os.path.getsize(report_path) / 1024  # KB
    print(f"文件大小: {file_size:.1f} KB")
    
    return report_path

def main():
    print("=" * 80)
    print("南开问卷自动测试 - 问卷填写 + 报告生成")
    print("=" * 80)
    print()
    
    try:
        # 步骤1：创建测试问卷提交
        print("[步骤1] 创建测试问卷提交数据...")
        submission_file, score_result = create_test_submission()
        
        print(f"\n测试企业得分情况：")
        print(f"  - 百分制得分: {score_result['percentage']:.2f}分")
        print(f"  - 实际得分: {score_result['total_score']:.2f}分")
        print(f"  - 满分: {score_result['max_score']:.2f}分")
        
        # 步骤2：生成报告
        print(f"\n[步骤2] 生成专业评价报告...")
        report_path = generate_test_report(submission_file)
        
        # 总结
        print("\n" + "=" * 80)
        print("测试完成！")
        print("=" * 80)
        print(f"\n生成的文件：")
        print(f"  1. 问卷提交数据: {submission_file}")
        print(f"  2. 专业评价报告: {report_path}")
        print(f"\n您可以打开报告文件查看模板样式。")
        print()
        
    except Exception as e:
        print(f"\n[ERROR] 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()