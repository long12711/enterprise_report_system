"""
用户类型和分级配置 - 版本2
基于南开大学现代企业制度指数评价体系
根据指标难度和类型为不同级别分配题目
"""

import pandas as pd

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
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,  # 最小分值，0表示无限制
            'max_score': 100  # 最大分值，100表示无限制
        },
        'provincial': {
            'description': '省级工商联评估问卷 - 重点评估',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,
            'max_score': 100
        },
        'municipal': {
            'description': '市级工商联评估问卷 - 基础评估',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制', '科学民主管理'],
            'min_score': 0,
            'max_score': 0.5  # 只包含基础题目
        }
    },
    'enterprise': {
        'advanced': {
            'description': '企业高级自评问卷 - 全面自评',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,
            'max_score': 100
        },
        'intermediate': {
            'description': '企业中级自评问卷 - 标准自评',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,
            'max_score': 100
        },
        'beginner': {
            'description': '企业初级自评问卷 - 基础自评',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制', '科学民主管理'],
            'min_score': 0,
            'max_score': 0.5
        }
    },
    'expert': {
        'senior': {
            'description': '高级专家评估问卷 - 深度评估',
            'include_all': True,
            'question_types': ['合规项', '有效项', '调节项'],
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,
            'max_score': 100
        },
        'intermediate': {
            'description': '中级专家评估问卷 - 标准评估',
            'include_all': True,
            'question_types': ['合规项', '有效项'],
            'applicable_enterprises': ['所有企业'],
            'min_score': 0,
            'max_score': 100
        },
        'junior': {
            'description': '初级专家评估问卷 - 基础评估',
            'include_all': False,
            'question_types': ['合规项'],
            'applicable_enterprises': ['所有企业'],
            'focus_areas': ['党建引领', '产权结构', '公司治理结构和机制'],
            'min_score': 0,
            'max_score': 0.5
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

# 根据指标体系文件加载题目并按级别分配
def load_questions_from_excel(excel_path='指标体系_备份.xlsx'):
    """
    从Excel文件加载问卷题目
    返回按级别分配的题目字典
    """
    try:
        df = pd.read_excel(excel_path)
        
        # 初始化分级题目字典
        questions_by_level = {
            'advanced': [],      # 高级：所有题目
            'intermediate': [],  # 中级：合规项和有效项
            'beginner': []       # 初级：仅合规项和核心题目
        }
        
        # 遍历所有题目
        for idx, row in df.iterrows():
            question = {
                'sequence': int(row['序号']) if pd.notna(row['序号']) else idx + 1,
                'level1': str(row['一级指标']) if pd.notna(row['一级指标']) else '',
                'level2': str(row['二级指标']) if pd.notna(row['二级指标']) else '',
                'question': str(row['三级指标']) if pd.notna(row['三级指标']) else '',
                'question_type': str(row['指标类型']) if pd.notna(row['指标类型']) else '',
                'base_score': float(row['分值']) if pd.notna(row['分值']) else 0,
                'applicable_enterprises': str(row['适用对象']) if pd.notna(row['适用对象']) else '所有企业'
            }
            
            # 根据题目类型和分值分配到不同级别
            question_type = question['question_type']
            base_score = question['base_score']
            level1 = question['level1']
            
            # 高级：所有题目
            questions_by_level['advanced'].append(question)
            
            # 中级：合规项和有效项（不包括调节项）
            if question_type in ['合规项', '有效项']:
                questions_by_level['intermediate'].append(question)
            
            # 初级：仅合规项，且在核心领域
            core_areas = ['党建引领', '产权结构', '公司治理结构和机制', '科学民主管理']
            if question_type == '合规项' and level1 in core_areas:
                questions_by_level['beginner'].append(question)
        
        return questions_by_level
    
    except Exception as e:
        print(f"加载Excel文件失败: {e}")
        return None

# 缓存加载的题目
_cached_questions = None

def get_questions_by_level(user_type, level, excel_path='指标体系_备份.xlsx'):
    """
    获取特定用户类型和分级的问卷题目
    """
    global _cached_questions
    
    # 如果缓存为空，加载题目
    if _cached_questions is None:
        _cached_questions = load_questions_from_excel(excel_path)
    
    if _cached_questions is None:
        return []
    
    # 根据用户类型和分级返回对应的题目
    # 工商联用户和企业用户使用相同的分级逻辑
    if user_type in ['chamber_of_commerce', 'enterprise']:
        if level == 'national' or level == 'advanced' or level == 'senior':
            return _cached_questions['advanced']
        elif level == 'provincial' or level == 'intermediate':
            return _cached_questions['intermediate']
        elif level == 'municipal' or level == 'beginner' or level == 'junior':
            return _cached_questions['beginner']
    
    elif user_type == 'expert':
        if level == 'senior':
            return _cached_questions['advanced']
        elif level == 'intermediate':
            return _cached_questions['intermediate']
        elif level == 'junior':
            return _cached_questions['beginner']
    
    return []

