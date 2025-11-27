#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析按级别分配的问卷题目
"""

import pandas as pd
from user_types_config_v2 import (
    get_questions_by_level,
    USER_TYPES,
    get_questionnaire_config
)

def analyze_questions():
    """分析按级别分配的问卷题目"""
    
    print("=" * 100)
    print("按级别分配的问卷题目分析")
    print("=" * 100)
    
    # 定义所有用户类型和分级组合
    test_cases = [
        ('chamber_of_commerce', 'national', '工商联-国家级'),
        ('chamber_of_commerce', 'provincial', '工商联-省级'),
        ('chamber_of_commerce', 'municipal', '工商联-市级'),
        ('enterprise', 'advanced', '企业-高级'),
        ('enterprise', 'intermediate', '企业-中级'),
        ('enterprise', 'beginner', '企业-初级'),
        ('expert', 'senior', '专家-高级'),
        ('expert', 'intermediate', '专家-中级'),
        ('expert', 'junior', '专家-初级'),
    ]
    
    # 统计数据
    summary = []
    
    for user_type, level, label in test_cases:
        print(f"\n{label}:")
        print("-" * 100)
        
        # 获取问卷配置
        config = get_questionnaire_config(user_type, level)
        if config:
            print(f"  描述: {config['description']}")
            print(f"  包含所有题目: {config['include_all']}")
            print(f"  问题类型: {', '.join(config['question_types'])}")
            print(f"  适用对象: {', '.join(config['applicable_enterprises'])}")
            if 'focus_areas' in config:
                print(f"  重点领域: {', '.join(config['focus_areas'])}")
        
        # 获取题目
        questions = get_questions_by_level(user_type, level)
        print(f"  题目总数: {len(questions)}")
        
        # 统计题目类型
        type_count = {}
        level1_count = {}
        score_total = 0
        
        for q in questions:
            q_type = q['question_type']
            level1 = q['level1']
            score = q['base_score']
            
            type_count[q_type] = type_count.get(q_type, 0) + 1
            level1_count[level1] = level1_count.get(level1, 0) + 1
            score_total += score
        
        print(f"  总分值: {score_total}")
        print(f"  按类型统计:")
        for q_type, count in sorted(type_count.items()):
            print(f"    - {q_type}: {count}题")
        
        print(f"  按一级指标统计:")
        for level1, count in sorted(level1_count.items()):
            if level1:  # 只显示非空的一级指标
                print(f"    - {level1}: {count}题")
        
        # 显示前5道题目
        print(f"  前5道题目:")
        for i, q in enumerate(questions[:5], 1):
            print(f"    {i}. [{q['question_type']}] {q['question'][:60]}...")
        
        summary.append({
            '用户类型': label,
            '题目数': len(questions),
            '总分值': score_total,
            '合规项': type_count.get('合规项', 0),
            '有效项': type_count.get('有效项', 0),
            '调节项': type_count.get('调节项', 0)
        })
    
    # 打印汇总表
    print("\n" + "=" * 100)
    print("汇总表")
    print("=" * 100)
    
    df_summary = pd.DataFrame(summary)
    print(df_summary.to_string(index=False))
    
    print("\n" + "=" * 100)
    print("分析完成！")
    print("=" * 100)

if __name__ == '__main__':
    analyze_questions()

