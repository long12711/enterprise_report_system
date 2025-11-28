import os
import json
from datetime import datetime
from flask import current_app
import pandas as pd


def _list_submission_jsons(limit=200):
    base = current_app.config.get('SUBMISSIONS_FOLDER', 'storage/submissions')
    items = []
    if not os.path.exists(base):
        return []
    for fn in os.listdir(base):
        if fn.endswith('.json'):
            p = os.path.join(base, fn)
            try:
                items.append((os.path.getmtime(p), p))
            except Exception:
                pass
    items.sort(reverse=True)
    return [p for _, p in items[:limit]]


def _compute_score_from_excel(xlsx_path):
    try:
        df = pd.read_excel(xlsx_path, sheet_name='问卷')
        # 兼容列名
        if '答案' not in df.columns and '答案/清单选择' in df.columns:
            df = df.rename(columns={'答案/清单选择': '答案'})
        if '指标类型' not in df.columns and '问题类型' in df.columns:
            df = df.rename(columns={'问题类型': '指标类型'})

        def to_float(v, d=0.0):
            try:
                if pd.isna(v):
                    return d
                return float(v)
            except Exception:
                return d

        # 快速路径：存在计算分数列则直接求和
        if '计算分数' in df.columns:
            total_score = df['计算分数'].apply(lambda x: to_float(x, 0.0)).sum()
        else:
            # 简化打分逻辑
            eff_map = {'很有效': 1.0, '比较有效': 0.8, '一般': 0.6, '不太有效': 0.3, '完全无效': 0.0}
            total_score = 0.0
            for _, r in df.iterrows():
                base = to_float(r.get('分值'), 0.0)
                ans = r.get('答案')
                qtype = str(r.get('指标类型') or '')
                # 尝试JSON
                if isinstance(ans, str) and ans.strip().startswith('{'):
                    try:
                        jr = json.loads(ans)
                        total_score += to_float(jr.get('score'), 0.0)
                        continue
                    except Exception:
                        pass
                ans = str(ans or '').strip()
                if '否决' in qtype or '调节' in qtype:
                    total_score += base if ans == '否' else 0.0
                elif '合规' in qtype:
                    total_score += base if ans == '是' else 0.0
                elif '有效' in qtype:
                    total_score += base * eff_map.get(ans, 0.0)
                else:
                    total_score += base if ans in ['是', '有', '已建立', '已设立', '已制定'] else 0.0

        max_possible = df['分值'].apply(lambda x: to_float(x, 0.0)).apply(lambda x: x if x > 0 else 0).sum()
        pct = (total_score / max_possible * 100.0) if max_possible > 0 else 0.0
        return {'total': float(total_score), 'max': float(max_possible), 'percentage': float(pct)}
    except Exception as e:
        return {'total': 0.0, 'max': 0.0, 'percentage': 0.0, 'error': str(e)}


def _load_submission(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 派生Excel路径：与JSON同目录
        base_dir = os.path.dirname(json_path)
        base_name = os.path.basename(json_path)
        xlsx = os.path.join(base_dir, base_name.replace('submission_', '问卷_').replace('.json', '.xlsx'))
        return data, xlsx
    except Exception:
        return None, None


def get_expert_matches():
    items = []
    for jp in _list_submission_jsons():
        data, xlsx = _load_submission(jp)
        if not data or not os.path.exists(xlsx):
            continue
        sc = _compute_score_from_excel(xlsx)
        pct = sc.get('percentage', 0.0)
        if pct >= 80:
            match_level = 'advanced'; priority = '中'
        elif pct >= 60:
            match_level = 'intermediate'; priority = '中'
        else:
            match_level = 'beginner'; priority = '高'
        items.append({
            'enterprise_name': data.get('enterprise_info', {}).get('企业名称', ''),
            'current_level': data.get('user_level', 'advanced'),
            'score_percentage': pct,
            'match_level': match_level,
            'priority': priority
        })
    return items

