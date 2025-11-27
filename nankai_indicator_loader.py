# -*- coding: utf-8 -*-
"""
南开大学指标体系加载器
支持从包含“初级 / 中级 / 高级”三个工作表的Excel读取题目。
输出统一题目结构，包含可选的“打分标准(criteria)”。
"""
from __future__ import annotations
import pandas as pd
from typing import List, Dict, Optional, Tuple

SHEET_MAP_CN = {
    'beginner': '初级',
    'intermediate': '中级',
    'advanced': '高级',
}

# 兼容的列名映射（可能存在不同的命名）
COLUMN_CANDIDATES = {
    '序号': ['序号', '编号', 'id', 'Index'],
    '一级指标': ['一级指标', '一级', '一级维度'],
    '二级指标': ['二级指标', '二级', '二级维度'],
    '三级指标': ['三级指标', '三级', '问题', '指标内容', '题目'],
    '指标类型': ['指标类型', '题目类型', '类型'],
    '分值': ['分值', '满分', '权重', '得分上限'],
    '适用对象': ['适用对象', '适用企业'],
    '打分标准': ['打分标准', '评分标准', '评分细则', '评价标准', '判断标准']
}


def _resolve_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """尝试在DataFrame中解析出标准列名对应的真实列名。"""
    result = {}
    lower_cols = {str(c).strip().lower(): c for c in df.columns}
    for std, cands in COLUMN_CANDIDATES.items():
        hit = None
        for name in cands:
            key = str(name).strip().lower()
            if key in lower_cols:
                hit = lower_cols[key]
                break
        result[std] = hit
    return result


def _coerce(value, default=""):
    if pd.isna(value):
        return default
    return value


def load_questions_by_level(file_path: str, level_key: str) -> List[Dict]:
    """
    从指定Excel读取指定级别(初级/中级/高级)题目。
    level_key: beginner/intermediate/advanced
    返回：统一结构的题目列表
    """
    sheet_name = SHEET_MAP_CN.get(level_key, level_key)
    # 读取指定工作表
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    except ValueError:
        # 工作表不在，尝试读取所有，优先匹配包含关键字的sheet
        xls = pd.ExcelFile(file_path)
        matched = None
        for sn in xls.sheet_names:
            if str(sheet_name) in str(sn):
                matched = sn
                break
        if matched is None:
            raise
        df = pd.read_excel(file_path, sheet_name=matched)

    cols = _resolve_columns(df)

    seq_col = cols.get('序号')
    l1_col = cols.get('一级指标')
    l2_col = cols.get('二级指标')
    l3_col = cols.get('三级指标')
    type_col = cols.get('指标类型')
    score_col = cols.get('分值')
    target_col = cols.get('适用对象')
    criteria_col = cols.get('打分标准')

    questions: List[Dict] = []
    if l3_col is None:
        # 没有三级指标列无法形成题目
        return questions

    for idx, row in df.iterrows():
        question_text = _coerce(row.get(l3_col, ''), '').strip()
        if not question_text:
            continue
        sequence = row.get(seq_col) if seq_col else None
        level1 = _coerce(row.get(l1_col, ''), '').strip() if l1_col else ''
        level2 = _coerce(row.get(l2_col, ''), '').strip() if l2_col else ''
        qtype = _coerce(row.get(type_col, ''), '').strip() if type_col else ''
        base_score = row.get(score_col) if score_col else None
        try:
            base_score = float(base_score) if base_score is not None and not pd.isna(base_score) else None
        except Exception:
            base_score = None
        applicable = _coerce(row.get(target_col, ''), '所有企业') if target_col else '所有企业'
        criteria = _coerce(row.get(criteria_col, ''), '').strip() if criteria_col else ''

        q = {
            'sequence': int(sequence) if (sequence is not None and not pd.isna(sequence)) else (len(questions) + 1),
            'level1': level1,
            'level2': level2,
            'question': question_text,
            'question_type': qtype or '合规项',
            'base_score': base_score if base_score is not None else 1.0,
            'applicable_enterprises': applicable,
            'criteria': criteria,
            'source_level': sheet_name
        }
        questions.append(q)

    return questions


def map_user_to_level(user_type: str, user_level: str) -> str:
    """将用户类型/级别映射到 beginner/intermediate/advanced。"""
    mapping = {
        'chamber_of_commerce': {
            'national': 'advanced',
            'provincial': 'intermediate',
            'municipal': 'beginner'
        },
        'enterprise': {
            'advanced': 'advanced',
            'intermediate': 'intermediate',
            'beginner': 'beginner'
        },
        'expert': {
            'senior': 'advanced',
            'intermediate': 'intermediate',
            'junior': 'beginner'
        }
    }
    return mapping.get(user_type, {}).get(user_level, 'advanced')

