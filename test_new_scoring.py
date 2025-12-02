"""
测试新的评分系统（基于评分细则）
"""

import json
from datetime import datetime
from nankai_scoring_engine import NankaiScoringEngine


def test_scoring_engine():
    """测试评分引擎"""
    print("=" * 80)
    print("测试南开评分引擎（基于评分细则）")
    print("=" * 80)
    
    # 初始化评分引擎
    engine = NankaiScoringEngine(
        'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx'
    )
    
    # 模拟答案数据
    test_answers = {
        '1': 'A. 已完成',
        '2': 'A. 已完成',
        '3': 'B. 部分完成',
        '4': 'C. 未完成',
        '5': 'A. 已完成',
        '6': 'B. 部分完成',
        '7': 'A. 已完成',
        '8': 'A. 已完成',
        '9': 'A. 已完成',
        '10': 'B. 部分完成',
    }
    
    partial_details = {
        '3': '该项工作已完成约80%，正在持续推进中。',
        '6': '已完成2项，第3项正在推进中。',
        '10': '部分材料已准备，正在补充完善。'
    }
    
    print("\n测试数据:")
    print(f"- 答案数量: {len(test_answers)}")
    print(f"- 部分完成说明: {len(partial_details)}项")
    
    # 计算得分
    print("\n开始计算得分...")
    try:
        result = engine.calculate_score(
            level='初级',
            answers=test_answers,
            partial_details=partial_details
        )
        
        print("\n" + "=" * 80)
        print("评分结果")
        print("=" * 80)
        print(f"实际得分: {result['total_score']:.2f}分")
        print(f"满分: {result['max_score']:.2f}分")
        print(f"百分制得分: {result['percentage']:.2f}分")
        
        print("\n详细得分:")
        print("-" * 80)
        for q_id, detail in list(result['details'].items())[:10]:
            print(f"题目{q_id}: {detail['earned_score']:.2f}/{detail['max_score']:.2f}分 "
                  f"(规则类型: {detail['rule_type']}) - {detail['answer']}")
        
        if len(result['details']) > 10:
            print(f"... 还有 {len(result['details']) - 10} 个题目")
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] 评分失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_scoring_methods():
    """对比新旧评分方法"""
    print("\n" + "=" * 80)
    print("对比新旧评分方法")
    print("=" * 80)
    
    # 模拟相同的答案
    answers = {}
    for i in range(1, 65):  # 初级有64个指标
        # 70%选A，20%选B，10%选C
        import random
        rand = random.random()
        if rand < 0.7:
            answers[str(i)] = 'A. 已完成'
        elif rand < 0.9:
            answers[str(i)] = 'B. 部分完成'
        else:
            answers[str(i)] = 'C. 未完成'
    
    # 新方法（基于评分细则）
    engine = NankaiScoringEngine(
        'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx'
    )
    
    try:
        new_result = engine.calculate_score('初级', answers, {})
        print(f"\n新方法（基于评分细则）:")
        print(f"  实际得分: {new_result['total_score']:.2f}分")
        print(f"  满分: {new_result['max_score']:.2f}分")
        print(f"  百分制得分: {new_result['percentage']:.2f}分")
    except Exception as e:
        print(f"\n新方法计算失败: {e}")
        new_result = None
    
    # 旧方法（简化评分A=100%, B=80%, C=0%）
    import pandas as pd
    df = pd.read_excel(
        'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx',
        sheet_name='初级'
    )
    
    old_total = 0
    old_max = 0
    
    for idx, row in df.iterrows():
        q_id = str(int(row['序号'])) if pd.notna(row['序号']) else str(idx + 1)
        score_value = row.get('分值', 1)
        
        # 解析分值
        if pd.notna(score_value):
            score_str = str(score_value).strip()
            if '-' in score_str:
                max_score = float(score_str.split('-')[1])
            else:
                try:
                    max_score = float(score_str)
                except:
                    max_score = 1.0
        else:
            max_score = 1.0
        
        old_max += max_score
        
        answer = answers.get(q_id, '')
        if answer.startswith('A'):
            old_total += max_score
        elif answer.startswith('B'):
            old_total += max_score * 0.8
    
    old_percentage = (old_total / old_max * 100) if old_max > 0 else 0
    
    print(f"\n旧方法（简化评分）:")
    print(f"  实际得分: {old_total:.2f}分")
    print(f"  满分: {old_max:.2f}分")
    print(f"  百分制得分: {old_percentage:.2f}分")
    
    if new_result:
        print(f"\n差异分析:")
        print(f"  得分差异: {abs(new_result['total_score'] - old_total):.2f}分")
        print(f"  百分制差异: {abs(new_result['percentage'] - old_percentage):.2f}分")
        print(f"  满分差异: {abs(new_result['max_score'] - old_max):.2f}分")


if __name__ == '__main__':
    # 测试评分引擎
    result = test_scoring_engine()
    
    # 对比新旧方法
    if result:
        compare_scoring_methods()
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)