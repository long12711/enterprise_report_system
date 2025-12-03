"""
南开问卷评分引擎
根据评分准则精确计算得分
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Any


class NankaiScoringEngine:
    """南开问卷评分引擎"""
    
    def __init__(self, indicator_file: str):
        """
        初始化评分引擎
        
        Args:
            indicator_file: 指标文件路径
        """
        self.indicator_file = indicator_file
        self.indicators_cache = {}
        
    def load_indicators(self, level: str) -> pd.DataFrame:
        """
        加载指标数据
        
        Args:
            level: 级别（初级/中级/高级）
            
        Returns:
            指标DataFrame
        """
        if level not in self.indicators_cache:
            try:
                df = pd.read_excel(self.indicator_file, sheet_name=level)
                self.indicators_cache[level] = df
            except:
                # 如果没有对应级别，尝试读取第一个sheet
                df = pd.read_excel(self.indicator_file, sheet_name=0)
                self.indicators_cache[level] = df
        
        return self.indicators_cache[level]
    
    def parse_score_value(self, score_value: Any) -> tuple:
        """
        解析分值（修复版）
        
        Args:
            score_value: 分值（可能是数字或范围如"0-2"）
            
        Returns:
            (min_score, max_score) 元组
        """
        if pd.isna(score_value):
            return (0.0, 1.0)
        
        score_str = str(score_value).strip()
        
        # 处理范围分值，如"0-2"
        if '-' in score_str:
            parts = score_str.split('-')
            try:
                min_score = float(parts[0])
                max_score = float(parts[1])
                return (min_score, max_score)
            except:
                return (0.0, 1.0)
        
        # 处理单一分值
        try:
            score = float(score_str)
            # 如果是正分，最小分为0；如果是负分，最大分为0
            if score >= 0:
                return (0.0, score)
            else:
                return (score, 0.0)
        except:
            return (0.0, 1.0)
    
    def parse_scoring_rule(self, rule_text: str, score_value: Any) -> Dict:
        """
        解析评分准则（修复版）
        
        Args:
            rule_text: 评分准则文本
            score_value: 分值
            
        Returns:
            评分规则字典
        """
        if pd.isna(rule_text):
            rule_text = ""
        
        rule_text = str(rule_text).strip()
        
        # 解析分值范围（使用修复后的函数）
        min_score, max_score = self.parse_score_value(score_value)
        
        # 分析评分类型
        rule_type = self._identify_rule_type(rule_text, max_score, min_score)
        
        # 提取评分条件
        conditions = self._extract_conditions(rule_text, rule_type, max_score, min_score)
        
        return {
            'type': rule_type,
            'max_score': max_score,
            'min_score': min_score,
            'rule_text': rule_text,
            'conditions': conditions
        }
    
    def _identify_rule_type(self, rule_text: str, max_score: float, min_score: float) -> str:
        """
        识别评分规则类型
        
        Returns:
            规则类型：binary（二元）、multi_item（多项）、all_required（全部必需）、
                     negative（否决）、graded（分级）
        """
        rule_lower = rule_text.lower()
        
        # 否决性指标（负分）
        if min_score < 0 or max_score < 0:
            return 'negative'
        
        # 全部完成型
        if '全部完成' in rule_text or '部分完成不得分' in rule_text:
            return 'all_required'
        
        # 多项累计评分
        if '项' in rule_text and ('得' in rule_text or '分' in rule_text):
            # 检查是否有分段描述，如"1-2项"、"3项"
            if re.search(r'\d+-\d+项', rule_text) or re.search(r'\d+项', rule_text):
                return 'multi_item'
        
        # 分级评分（有明确的等级描述）
        if max_score > min_score and max_score - min_score > 1:
            return 'graded'
        
        # 二元评分（默认）
        return 'binary'
    
    def _extract_conditions(self, rule_text: str, rule_type: str, 
                           max_score: float, min_score: float) -> List[Dict]:
        """
        提取评分条件
        
        Returns:
            条件列表，每个条件包含：description（描述）、score（得分）
        """
        conditions = []
        
        if rule_type == 'binary':
            # 二元评分：满足得分，不满足不得分
            conditions.append({
                'description': '满足条件',
                'score': max_score,
                'keywords': ['是', '有', '已建立', '已设立', '已制定', '完成']
            })
            conditions.append({
                'description': '不满足条件',
                'score': 0,
                'keywords': ['否', '无', '未建立', '未设立', '未制定', '未完成']
            })
        
        elif rule_type == 'all_required':
            # 全部完成型：必须全部完成
            conditions.append({
                'description': '全部完成',
                'score': max_score,
                'keywords': ['全部完成', '全部满足']
            })
            conditions.append({
                'description': '部分完成或未完成',
                'score': 0,
                'keywords': ['部分完成', '未完成']
            })
        
        elif rule_type == 'multi_item':
            # 多项累计：根据完成项数给分
            # 尝试从文本中提取分段规则
            segments = self._parse_multi_item_segments(rule_text, max_score)
            conditions.extend(segments)
        
        elif rule_type == 'negative':
            # 否决性：存在问题扣分
            conditions.append({
                'description': '存在违规',
                'score': min_score,
                'keywords': ['是', '存在', '有']
            })
            conditions.append({
                'description': '不存在违规',
                'score': 0,
                'keywords': ['否', '不存在', '无']
            })
        
        elif rule_type == 'graded':
            # 分级评分：根据完成程度分级
            # 简化处理：平均分配分数
            num_grades = int(max_score - min_score) + 1
            for i in range(num_grades):
                score = min_score + i
                conditions.append({
                    'description': f'等级{i+1}',
                    'score': score
                })
        
        return conditions
    
    def _parse_multi_item_segments(self, rule_text: str, max_score: float) -> List[Dict]:
        """
        解析多项累计的分段规则
        
        例如："实现'1-2项'的得1分，实现'3项'的得2分"
        """
        segments = []
        
        # 查找所有的项数-分数对应关系
        # 模式1: "实现'1-2项'的得1分"
        pattern1 = r'实现[\'"]?(\d+)-(\d+)项[\'"]?.*?得(\d+)分'
        matches1 = re.findall(pattern1, rule_text)
        
        for match in matches1:
            start_items = int(match[0])
            end_items = int(match[1])
            score = float(match[2])
            segments.append({
                'description': f'完成{start_items}-{end_items}项',
                'score': score,
                'min_items': start_items,
                'max_items': end_items
            })
        
        # 模式2: "实现'3项'的得2分"
        pattern2 = r'实现[\'"]?(\d+)项[\'"]?.*?得(\d+)分'
        matches2 = re.findall(pattern2, rule_text)
        
        for match in matches2:
            items = int(match[0])
            score = float(match[1])
            # 避免重复添加
            if not any(s.get('min_items') == items and s.get('max_items') == items 
                      for s in segments):
                segments.append({
                    'description': f'完成{items}项',
                    'score': score,
                    'min_items': items,
                    'max_items': items
                })
        
        # 添加0项的情况
        if segments and not any(s.get('min_items', 1) == 0 for s in segments):
            segments.insert(0, {
                'description': '未完成或完成0项',
                'score': 0,
                'min_items': 0,
                'max_items': 0
            })
        
        # 如果没有解析出分段，使用默认规则
        if not segments:
            segments = [
                {'description': '未完成', 'score': 0},
                {'description': '部分完成', 'score': max_score / 2},
                {'description': '全部完成', 'score': max_score}
            ]
        
        return segments
    
    def calculate_score(self, level: str, answers: Dict[str, str], 
                       partial_details: Dict[str, str] = None) -> Dict:
        """
        计算问卷得分
        
        Args:
            level: 级别
            answers: 答案字典 {question_id: answer}
            partial_details: 部分完成的详细说明
            
        Returns:
            得分结果字典
        """
        if partial_details is None:
            partial_details = {}
        
        # 加载指标
        df = self.load_indicators(level)
        
        total_score = 0
        max_possible_score = 0
        score_details = {}
        
        for idx, row in df.iterrows():
            # 获取题目ID
            q_id = str(int(row['序号'])) if pd.notna(row['序号']) else str(idx + 1)
            
            # 获取分值和评分准则
            score_value = row.get('分值', 1)
            rule_text = row.get('评分准则', '')
            
            # 解析评分规则
            rule = self.parse_scoring_rule(rule_text, score_value)
            
            # 获取用户答案
            answer = answers.get(q_id, '')
            partial_detail = partial_details.get(q_id, '')
            
            # 计算得分
            earned_score = self._calculate_item_score(answer, partial_detail, rule)
            
            total_score += earned_score
            max_possible_score += rule['max_score']
            
            score_details[q_id] = {
                'max_score': rule['max_score'],
                'earned_score': earned_score,
                'answer': answer,
                'rule_type': rule['type']
            }
        
        # 计算百分制得分
        percentage = (total_score / max_possible_score * 100) if max_possible_score > 0 else 0
        
        return {
            'total_score': round(total_score, 2),
            'max_score': round(max_possible_score, 2),
            'percentage': round(percentage, 2),
            'details': score_details
        }
    
    def _calculate_item_score(self, answer: str, partial_detail: str, rule: Dict) -> float:
        """
        计算单个题目的得分（智能评分版）
        
        Args:
            answer: 用户答案
            partial_detail: 部分完成说明（用于B选项的智能评分）
            rule: 评分规则
            
        Returns:
            得分
        """
        answer = str(answer).strip()
        partial_detail = str(partial_detail).strip() if partial_detail else ''
        rule_type = rule['type']
        conditions = rule['conditions']
        max_score = rule['max_score']
        min_score = rule['min_score']
        
        # 提取答案中的关键信息
        answer_lower = answer.lower()
        
        if rule_type == 'binary':
            # 二元评分：A=满分，C=0分
            if answer.startswith('A'):
                return max_score
            else:
                return 0
        
        elif rule_type == 'all_required':
            # 全部完成型：只有A才得分
            if answer.startswith('A'):
                return max_score
            else:
                return 0
        
        elif rule_type == 'multi_item' or rule_type == 'graded':
            # 多项累计或分级评分
            if answer.startswith('A'):
                # 已完成，取最高分
                return max_score
            elif answer.startswith('B'):
                # 部分完成，根据补充说明智能评分
                return self._evaluate_partial_completion(
                    partial_detail, max_score, min_score
                )
            else:
                # 未完成，取最低分
                return min_score
        
        elif rule_type == 'negative':
            # 否决性指标：A=扣分，C=不扣分
            if answer.startswith('A') or '是' in answer or '存在' in answer:
                return min_score  # 扣分（负值）
            else:
                return 0
        
        return 0
    
    def _evaluate_partial_completion(self, partial_detail: str, max_score: float, min_score: float) -> float:
        """
        根据部分完成的补充说明智能评分
        
        Args:
            partial_detail: 用户填写的补充说明
            max_score: 最高分
            min_score: 最低分
            
        Returns:
            智能评分结果
        """
        if not partial_detail:
            # 没有填写补充说明，给予较低分数
            if max_score == 2 and min_score == 0:
                return 0.5  # 0-2分题目，无说明得0.5分
            else:
                return min_score + (max_score - min_score) * 0.3
        
        # 分析补充说明的质量
        detail_length = len(partial_detail)
        detail_lower = partial_detail.lower()
        
        # 评分因子
        score_factor = 0.5  # 基础分（50%）
        
        # 因子1：文字长度（最多+20%）
        if detail_length >= 100:
            score_factor += 0.2
        elif detail_length >= 50:
            score_factor += 0.15
        elif detail_length >= 20:
            score_factor += 0.1
        elif detail_length >= 10:
            score_factor += 0.05
        
        # 因子2：关键词分析（最多+20%）
        positive_keywords = [
            '已', '完成', '建立', '制定', '实施', '执行', '落实', '推进',
            '正在', '计划', '准备', '即将', '部分', '初步', '基本',
            '规范', '完善', '健全', '明确', '具体', '详细'
        ]
        
        negative_keywords = [
            '未', '没有', '缺少', '不足', '待', '需要', '尚未', '暂无'
        ]
        
        positive_count = sum(1 for kw in positive_keywords if kw in partial_detail)
        negative_count = sum(1 for kw in negative_keywords if kw in partial_detail)
        
        if positive_count > negative_count:
            keyword_bonus = min(0.2, positive_count * 0.05)
            score_factor += keyword_bonus
        elif negative_count > positive_count:
            keyword_penalty = min(0.1, negative_count * 0.03)
            score_factor -= keyword_penalty
        
        # 因子3：具体性分析（最多+10%）
        # 检查是否包含具体的数字、时间、名称等
        import re
        has_numbers = bool(re.search(r'\d+', partial_detail))
        has_percentage = bool(re.search(r'\d+%', partial_detail))
        has_date = bool(re.search(r'\d{4}年|\d+月', partial_detail))
        
        specificity_bonus = 0
        if has_numbers:
            specificity_bonus += 0.03
        if has_percentage:
            specificity_bonus += 0.04
        if has_date:
            specificity_bonus += 0.03
        
        score_factor += specificity_bonus
        
        # 确保评分因子在合理范围内（0.3-0.9）
        score_factor = max(0.3, min(0.9, score_factor))
        
        # 计算最终得分
        final_score = min_score + (max_score - min_score) * score_factor
        
        # 对于0-2分的题目，确保得分在0.5-1.8之间
        if max_score == 2 and min_score == 0:
            final_score = max(0.5, min(1.8, final_score))
        
        return round(final_score, 2)


if __name__ == '__main__':
    # 测试代码
    engine = NankaiScoringEngine('survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx')
    
    # 测试解析评分规则
    test_rules = [
        ("按照以下两项对应内容的得1分", "1"),
        ("按照全部完成的得1分，部分完成不得分", "1"),
        ("按照以下三项目标企业已实现的得0分，实现'1-2项'的得1分，实现'3项'的得2分", "0-2"),
    ]
    
    print("评分规则解析测试：")
    print("=" * 80)
    for rule_text, score_value in test_rules:
        rule = engine.parse_scoring_rule(rule_text, score_value)
        print(f"\n规则文本: {rule_text}")
        print(f"分值: {score_value}")
        print(f"规则类型: {rule['type']}")
        print(f"最高分: {rule['max_score']}, 最低分: {rule['min_score']}")
        print(f"条件数: {len(rule['conditions'])}")