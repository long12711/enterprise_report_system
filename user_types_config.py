"""
用户类型和分级配置
定义三类用户及其分级体系
"""

# 用户类型定义
USER_TYPES = {
    'chamber_of_commerce': {
        'name': '工商联用户',
        'description': '工商联及其下属机构',
        'levels': {
            'national': {'name': '国家级', 'value': 1},
            'provincial': {'name': '省级', 'value': 2},
            'municipal': {'name': '市级', 'value': 3}
        }
    },
    'enterprise': {
        'name': '企业用户',
        'description': '企业自评',
        'levels': {
            'advanced': {'name': '高级', 'value': 1},
            'intermediate': {'name': '中级', 'value': 2},
            'beginner': {'name': '初级', 'value': 3}
        }
    },
    'expert': {
        'name': '专家用户',
        'description': '专业评估机构/专家',
        'levels': {
            'senior': {'name': '高级专家', 'value': 1},
            'intermediate': {'name': '中级专家', 'value': 2},
            'junior': {'name': '初级专家', 'value': 3}
        }
    }
}

# 用户类型对应的问卷题目映射
# 根据指标体系，不同用户类型和分级对应不同的题目
USER_TYPE_QUESTION_MAPPING = {
    'chamber_of_commerce': {
        'national': {
            'description': '国家级工商联评估问卷 - 全面评估',
            'include_all': True,  # 包含所有题目
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业']
        },
        'provincial': {
            'description': '省级工商联评估问卷 - 重点评估',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业']
        },
        'municipal': {
            'description': '市级工商联评估问卷 - 基础评估',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制']
        }
    },
    'enterprise': {
        'advanced': {
            'description': '企业高级自评问卷 - 全面自评',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业']
        },
        'intermediate': {
            'description': '企业中级自评问卷 - 标准自评',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业']
        },
        'beginner': {
            'description': '企业初级自评问卷 - 基础自评',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制', '科学民主管理']
        }
    },
    'expert': {
        'senior': {
            'description': '高级专家评估问卷 - 深度评估',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业']
        },
        'intermediate': {
            'description': '中级专家评估问卷 - 标准评估',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业']
        },
        'junior': {
            'description': '初级专家评估问卷 - 基础评估',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制']
        }
    }
}

# 获取用户类型的所有信息
def get_user_type_info(user_type):
    """获取用户类型的完整信息"""
    return USER_TYPES.get(user_type, None)

# 获取用户分级的所有信息
def get_user_level_info(user_type, level):
    """获取用户分级的完整信息"""
    user_info = USER_TYPES.get(user_type)
    if user_info:
        return user_info['levels'].get(level, None)
    return None

# 获取问卷配置
def get_questionnaire_config(user_type, level):
    """获取特定用户类型和分级的问卷配置"""
    return USER_TYPE_QUESTION_MAPPING.get(user_type, {}).get(level, None)

# 获取所有用户类型列表
def get_all_user_types():
    """获取所有用户类型列表"""
    return [
        {
            'value': key,
            'name': value['name'],
            'description': value['description']
        }
        for key, value in USER_TYPES.items()
    ]

# 获取特定用户类型的所有分级
def get_user_levels(user_type):
    """获取特定用户类型的所有分级"""
    user_info = USER_TYPES.get(user_type)
    if user_info:
        return [
            {
                'value': key,
                'name': value['name']
            }
            for key, value in user_info['levels'].items()
        ]
    return []

