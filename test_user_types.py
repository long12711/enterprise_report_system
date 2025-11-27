"""
测试用户类型和分级功能
"""

import json
from user_types_config import (
    get_all_user_types,
    get_user_levels,
    get_questionnaire_config,
    USER_TYPES
)

def test_user_types():
    """测试用户类型配置"""
    print("=" * 80)
    print("测试用户类型和分级功能")
    print("=" * 80)
    
    # 测试1: 获取所有用户类型
    print("\n[测试1] 获取所有用户类型")
    print("-" * 80)
    user_types = get_all_user_types()
    for user_type in user_types:
        print(f"  用户类型: {user_type['name']} ({user_type['value']})")
        print(f"  描述: {user_type['description']}")
    
    # 测试2: 获取每个用户类型的分级
    print("\n[测试2] 获取每个用户类型的分级")
    print("-" * 80)
    for user_type_key in USER_TYPES.keys():
        print(f"\n  {USER_TYPES[user_type_key]['name']}:")
        levels = get_user_levels(user_type_key)
        for level in levels:
            print(f"    - {level['name']} ({level['value']})")
    
    # 测试3: 获取问卷配置
    print("\n[测试3] 获取问卷配置")
    print("-" * 80)
    
    test_cases = [
        ('chamber_of_commerce', 'national'),
        ('chamber_of_commerce', 'provincial'),
        ('chamber_of_commerce', 'municipal'),
        ('enterprise', 'advanced'),
        ('enterprise', 'intermediate'),
        ('enterprise', 'beginner'),
        ('expert', 'senior'),
        ('expert', 'intermediate'),
        ('expert', 'junior'),
    ]
    
    for user_type, level in test_cases:
        config = get_questionnaire_config(user_type, level)
        if config:
            user_type_name = USER_TYPES[user_type]['name']
            level_name = USER_TYPES[user_type]['levels'][level]['name']
            print(f"\n  {user_type_name} - {level_name}:")
            print(f"    描述: {config['description']}")
            print(f"    包含所有题目: {config['include_all']}")
            print(f"    问题类型: {', '.join(config['question_types'])}")
            print(f"    适用对象: {', '.join(config['applicable_enterprises'])}")
            if 'focus_areas' in config:
                print(f"    重点领域: {', '.join(config['focus_areas'])}")
    
    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)

if __name__ == '__main__':
    test_user_types()

