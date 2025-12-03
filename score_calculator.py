"""
答案解析和评分计算模块
"""
import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class ScoreCalculator:
    """评分计算器"""

    def __init__(self, indicator_file=None):
        """
        初始化评分计算器

        Args:
            indicator_file: 指标体系Excel文件路径
        """
        # 如果未显式传入，则尝试从 config.json / 备份文件 / 默认文件中推断
        if not indicator_file:
            indicator_file = None
            # 1) 尝试从 config.json 读取
            try:
                if os.path.exists("config.json"):
                    with open("config.json", "r", encoding="utf-8") as f:
                        conf = json.load(f)
                    indicator_file = conf.get("indicators", {}).get("nk_excel_path") or None
            except Exception:
                indicator_file = None

            # 2) 若未配置或路径不存在，则尝试本地常用文件名
            if not indicator_file or not os.path.exists(indicator_file):
                if os.path.exists("指标体系_备份.xlsx"):
                    indicator_file = "指标体系_备份.xlsx"
                elif os.path.exists("指标体系.xlsx"):
                    indicator_file = "指标体系.xlsx"
                else:
                    indicator_file = None

        self.indicator_file = indicator_file
        self.indicators_df = None
        self.load_indicators()

    def load_indicators(self):
        """加载指标体系（如缺失则降级为空指标，保证系统可启动）"""
        # 统一列集合，方便后续计算逻辑依赖字段名
        cols = ["序号", "一级指标", "二级指标", "三级指标（问题）", "问题类型", "分值", "适用对象"]
        try:
            if self.indicator_file and os.path.exists(self.indicator_file):
                self.indicators_df = pd.read_excel(self.indicator_file, sheet_name=0)
                print(
                    f"[OK] 加载指标体系: {len(self.indicators_df)} 个问题 -> {self.indicator_file}"
                )
            else:
                # 找不到文件时，给出警告但不抛异常
                self.indicators_df = pd.DataFrame(columns=cols)
                print(
                    "[WARN] 未找到指标体系文件，将使用空指标以保证应用可启动。"
                    "可在 config.json 配置 indicators.nk_excel_path 或放置 指标体系_备份.xlsx / 指标体系.xlsx"
                )
        except Exception as e:
            # 任意异常都降级为空指标，避免阻塞整个系统
            print(f"[ERROR] 加载指标体系失败（已降级为空指标）：{e}")
            self.indicators_df = pd.DataFrame(columns=cols)

    def parse_questionnaire(self, questionnaire_file: str) -> Dict:
        """
        解析已填写的问卷Excel文件

        Args:
            questionnaire_file: 问卷文件路径

        Returns:
            包含企业信息和答案的字典
        """
        try:
            # 读取企业信息
            enterprise_info_df = pd.read_excel(questionnaire_file, sheet_name='企业信息', header=None)
            enterprise_info = {}
            for idx, row in enterprise_info_df.iterrows():
                if idx >= 2 and pd.notna(row[0]) and pd.notna(row[1]):
                    enterprise_info[str(row[0]).strip()] = str(row[1]).strip()

            # 读取问卷答案
            questionnaire_df = pd.read_excel(questionnaire_file, sheet_name='问卷')

            # 兼容列名（答案/清单选择、问题类型、计算分数）
            if '答案' not in questionnaire_df.columns and '答案/清单选择' in questionnaire_df.columns:
                questionnaire_df.rename(columns={'答案/清单选择': '答案'}, inplace=True)
            if '指标类型' not in questionnaire_df.columns and '问题类型' in questionnaire_df.columns:
                questionnaire_df.rename(columns={'问题类型': '指标类型'}, inplace=True)
            # 计算分数列保留为 计算分数

            return {
                'enterprise_info': enterprise_info,
                'answers': questionnaire_df
            }
        except Exception as e:
            print(f"[ERROR] 解析问卷失败: {e}")
            raise

    def calculate_score(self, answer: str, indicator_type: str, base_score: float) -> Tuple[float, str]:
        """
        计算单个问题的得分

        Args:
            answer: 答案
            indicator_type: 指标类型
            base_score: 基础分值

        Returns:
            (得分, 评价说明)
        """
        if pd.isna(answer) or answer == '' or answer == '不适用':
            return 0, '未填写或不适用'

        answer = str(answer).strip()

        # 处理一票否决类
        if '一票否决' in str(indicator_type) or '否决' in str(indicator_type):
            if answer == '否':
                return base_score, '一票否决：扣分'
            elif answer == '是':
                return 0, '符合要求'
            else:
                return 0, '未明确'

        # 处理合规类
        if '合规' in str(indicator_type):
            if answer == '是':
                return base_score, '符合要求'
            elif answer == '否':
                return 0, '不符合'
            else:
                return 0, '未明确'

        # 处理有效性类
        if '有效' in str(indicator_type):
            effectiveness_scores = {
                '很有效': 1.0,
                '比较有效': 0.8,
                '一般': 0.6,
                '不太有效': 0.3,
                '完全无效': 0
            }
            ratio = effectiveness_scores.get(answer, 0)
            return base_score * ratio, f'有效性：{answer}'

        # 默认处理
        if answer in ['是', '有', '已建立', '已设立', '已制定']:
            return base_score, '符合'
        else:
            return 0, '不符合或未填写'

    def calculate_total_score(self, questionnaire_data: Dict) -> Dict:
        """
        计算总得分和各维度得分

        Args:
            questionnaire_data: 问卷数据（包含企业信息和答案）

        Returns:
            得分详情字典
        """
        answers_df = questionnaire_data['answers']
        enterprise_info = questionnaire_data['enterprise_info']
        enterprise_type = enterprise_info.get('企业类型', '所有企业')

        # 初始化得分统计
        score_summary = {
            'total_score': 0,
            'max_possible_score': 0,
            'score_by_level1': {},
            'score_by_level2': {},
            'question_details': [],
            'negative_points': 0,  # 一票否决扣分
            'answered_count': 0,
            'total_questions': 0,
            'applicable_questions': 0
        }

        # 逐题计算
        for idx, row in answers_df.iterrows():
            seq_no = row.get('序号', idx + 1)
            level1 = str(row.get('一级指标', '')) if pd.notna(row.get('一级指标')) else ''
            level2 = str(row.get('二级指标', '')) if pd.notna(row.get('二级指标')) else ''
            question = row.get('三级指标（问题）', '')
            indicator_type = row.get('指标类型', '')
            base_score = row.get('分值', 0)
            applicable = row.get('适用对象', '所有企业')
            answer = row.get('答案', '')
            remark = row.get('备注说明', '')

            # 转换分值
            try:
                base_score = float(base_score) if pd.notna(base_score) else 0
            except:
                base_score = 0

            # 检查是否适用
            is_applicable = self._check_applicability(enterprise_type, applicable)

            if not is_applicable:
                continue

            score_summary['applicable_questions'] += 1
            score_summary['total_questions'] += 1

            # 只计算正分题的最大可能分
            if base_score > 0:
                score_summary['max_possible_score'] += base_score

            # 计算得分
            if pd.notna(answer) and answer != '':
                score_summary['answered_count'] += 1

                # 1) 优先采用“计算分数”列（清单打分）
                actual_score = None
                comment = '自动计分'
                if '计算分数' in answers_df.columns:
                    try:
                        computed = row.get('计算分数')
                        if computed is not None and not pd.isna(computed):
                            actual_score = float(computed)
                    except Exception:
                        actual_score = None

                # 2) 如未取到，尝试解析答案为JSON并取score
                if actual_score is None:
                    try:
                        if isinstance(answer, str) and answer.strip().startswith('{'):
                            import json
                            jr = json.loads(answer)
                            if isinstance(jr, dict) and 'score' in jr:
                                actual_score = float(jr.get('score') or 0)
                                comment = f"清单项{len(jr.get('selected', []))}/{jr.get('total', 0)}，自动计分"
                    except Exception:
                        actual_score = None

                # 3) 仍未取到，则走原有规则
                if actual_score is None:
                    actual_score, comment = self.calculate_score(answer, indicator_type, base_score)

                # 累加得分
                score_summary['total_score'] += actual_score

                # 记录负分
                if actual_score < 0:
                    score_summary['negative_points'] += actual_score

                # 按一级指标统计
                if level1:
                    if level1 not in score_summary['score_by_level1']:
                        score_summary['score_by_level1'][level1] = {
                            'score': 0,
                            'max_score': 0,
                            'count': 0
                        }
                    score_summary['score_by_level1'][level1]['score'] += actual_score
                    if base_score > 0:
                        score_summary['score_by_level1'][level1]['max_score'] += base_score
                    score_summary['score_by_level1'][level1]['count'] += 1

                # 按二级指标统计
                if level2:
                    if level2 not in score_summary['score_by_level2']:
                        score_summary['score_by_level2'][level2] = {
                            'level1': level1,
                            'score': 0,
                            'max_score': 0,
                            'count': 0
                        }
                    score_summary['score_by_level2'][level2]['score'] += actual_score
                    if base_score > 0:
                        score_summary['score_by_level2'][level2]['max_score'] += base_score
                    score_summary['score_by_level2'][level2]['count'] += 1

                # 记录问题详情
                score_summary['question_details'].append({
                    'seq_no': seq_no,
                    'level1': level1,
                    'level2': level2,
                    'question': question,
                    'answer': answer,
                    'base_score': base_score,
                    'actual_score': actual_score,
                    'comment': comment,
                    'remark': remark
                })

        # 计算百分比
        if score_summary['max_possible_score'] > 0:
            score_summary['score_percentage'] = (
                score_summary['total_score'] / score_summary['max_possible_score'] * 100
            )
        else:
            score_summary['score_percentage'] = 0

        # 计算完成率
        if score_summary['applicable_questions'] > 0:
            score_summary['completion_rate'] = (
                score_summary['answered_count'] / score_summary['applicable_questions'] * 100
            )
        else:
            score_summary['completion_rate'] = 0

        # 计算各一级指标的得分率
        for level1, data in score_summary['score_by_level1'].items():
            if data['max_score'] > 0:
                data['percentage'] = (data['score'] / data['max_score']) * 100
            else:
                data['percentage'] = 0

        # 计算各二级指标的得分率
        for level2, data in score_summary['score_by_level2'].items():
            if data['max_score'] > 0:
                data['percentage'] = (data['score'] / data['max_score']) * 100
            else:
                data['percentage'] = 0

        return score_summary

    def _check_applicability(self, enterprise_type: str, applicable: str) -> bool:
        """
        检查问题是否适用于该企业类型

        Args:
            enterprise_type: 企业类型
            applicable: 适用对象

        Returns:
            是否适用
        """
        if pd.isna(applicable) or applicable == '所有企业':
            return True

        applicable = str(applicable).strip()
        enterprise_type = str(enterprise_type).strip()

        # 简单的匹配逻辑
        if '所有企业' in applicable:
            return True

        if enterprise_type in applicable:
            return True

        # 特殊处理
        if '有限责任公司' in enterprise_type and '有限责任公司' in applicable:
            return True
        if '股份有限公司' in enterprise_type and '股份有限公司' in applicable:
            return True
        if '公司制企业' in applicable and ('有限责任公司' in enterprise_type or '股份有限公司' in enterprise_type):
            return True

        return False

    def get_evaluation_level(self, score_percentage: float) -> Tuple[str, str]:
        """
        根据得分百分比确定评价等级

        Args:
            score_percentage: 得分百分比

        Returns:
            (等级, 评价)
        """
        if score_percentage >= 90:
            return 'A', '优秀'
        elif score_percentage >= 80:
            return 'B', '良好'
        elif score_percentage >= 70:
            return 'C', '中等'
        elif score_percentage >= 60:
            return 'D', '及格'
        else:
            return 'E', '需改进'

    def generate_score_summary_text(self, score_summary: Dict) -> str:
        """
        生成得分摘要文本

        Args:
            score_summary: 得分详情

        Returns:
            摘要文本
        """
        level, evaluation = self.get_evaluation_level(score_summary['score_percentage'])

        summary = f"""
==================================================
评分摘要
==================================================

总得分：{score_summary['total_score']:.2f} / {score_summary['max_possible_score']:.2f}
得分率：{score_summary['score_percentage']:.2f}%
评价等级：{level} ({evaluation})

问题统计：
- 适用问题数：{score_summary['applicable_questions']}
- 已回答问题：{score_summary['answered_count']}
- 完成率：{score_summary['completion_rate']:.2f}%

一票否决扣分：{score_summary['negative_points']:.2f}

==================================================
各维度得分
==================================================
"""

        for level1, data in sorted(score_summary['score_by_level1'].items()):
            summary += f"\n{level1}：\n"
            summary += f"  得分：{data['score']:.2f} / {data['max_score']:.2f}\n"
            summary += f"  得分率：{data['percentage']:.2f}%\n"
            summary += f"  问题数：{data['count']}\n"

        return summary


if __name__ == '__main__':
    # 测试评分计算
    calculator = ScoreCalculator()

    # 这里需要一个已填写的问卷文件来测试
    # questionnaire_file = '测试问卷_已填写.xlsx'
    # data = calculator.parse_questionnaire(questionnaire_file)
    # score_summary = calculator.calculate_total_score(data)
    # print(calculator.generate_score_summary_text(score_summary))

    print("\n评分计算器已初始化")
