"""
行业对比分析模块
用于分析企业在行业中的位置，提供行业基准对比数据
"""
import json
import os
from typing import Dict, List, Tuple
from datetime import datetime
import statistics


class IndustryAnalyzer:
    """行业对比分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.submissions_dir = 'storage/submissions/'
        self.benchmarks_file = 'storage/industry_benchmarks.json'
        self._load_benchmarks()
    
    def _load_benchmarks(self):
        """加载行业基准数据"""
        if os.path.exists(self.benchmarks_file):
            with open(self.benchmarks_file, 'r', encoding='utf-8') as f:
                self.benchmarks = json.load(f)
        else:
            # 使用默认基准数据
            self.benchmarks = self._get_default_benchmarks()
            self._save_benchmarks()
    
    def _save_benchmarks(self):
        """保存行业基准数据"""
        os.makedirs(os.path.dirname(self.benchmarks_file), exist_ok=True)
        with open(self.benchmarks_file, 'w', encoding='utf-8') as f:
            json.dump(self.benchmarks, f, ensure_ascii=False, indent=2)
    
    def _get_default_benchmarks(self) -> Dict:
        """获取默认行业基准数据"""
        return {
            "last_update": datetime.now().strftime('%Y-%m-%d'),
            "industries": {
                "软件和信息技术服务业": {
                    "total_enterprises": 15420,
                    "large_enterprises": 1205,
                    "benchmarks": {
                        "average": 81.0,
                        "excellent": 95.0,
                        "same_size_avg": 88.0,
                        "benchmark": 97.0,
                        "international": 99.0
                    },
                    "dimensions": {
                        "治理方向性": {"average": 85.0, "excellent": 97.0},
                        "治理有效性": {"average": 80.0, "excellent": 94.0},
                        "治理规范性": {"average": 82.0, "excellent": 96.0},
                        "治理透明性": {"average": 75.0, "excellent": 92.0},
                        "财务管理": {"average": 84.0, "excellent": 97.0},
                        "风险管控": {"average": 78.0, "excellent": 91.0},
                        "合规管理": {"average": 76.0, "excellent": 93.0},
                        "创新能力": {"average": 83.0, "excellent": 95.0},
                        "可持续发展": {"average": 73.5, "excellent": 90.0}
                    },
                    "benchmark_companies": ["腾讯控股", "阿里巴巴集团", "华为技术有限公司"]
                },
                "制造业": {
                    "total_enterprises": 28500,
                    "large_enterprises": 2150,
                    "benchmarks": {
                        "average": 78.0,
                        "excellent": 92.0,
                        "same_size_avg": 85.0,
                        "benchmark": 95.0,
                        "international": 98.0
                    },
                    "dimensions": {
                        "治理方向性": {"average": 82.0, "excellent": 94.0},
                        "治理有效性": {"average": 77.0, "excellent": 91.0},
                        "治理规范性": {"average": 79.0, "excellent": 93.0},
                        "治理透明性": {"average": 72.0, "excellent": 89.0},
                        "财务管理": {"average": 81.0, "excellent": 94.0},
                        "风险管控": {"average": 75.0, "excellent": 88.0},
                        "合规管理": {"average": 73.0, "excellent": 90.0},
                        "创新能力": {"average": 80.0, "excellent": 92.0},
                        "可持续发展": {"average": 70.0, "excellent": 87.0}
                    },
                    "benchmark_companies": ["华为制造", "比亚迪", "格力电器"]
                },
                "其他": {
                    "total_enterprises": 50000,
                    "large_enterprises": 3000,
                    "benchmarks": {
                        "average": 76.0,
                        "excellent": 91.0,
                        "same_size_avg": 83.0,
                        "benchmark": 95.0,
                        "international": 98.0
                    },
                    "dimensions": {
                        "治理方向性": {"average": 80.0, "excellent": 93.0},
                        "治理有效性": {"average": 75.0, "excellent": 89.0},
                        "治理规范性": {"average": 77.0, "excellent": 91.0},
                        "治理透明性": {"average": 71.0, "excellent": 87.0},
                        "财务管理": {"average": 79.0, "excellent": 92.0},
                        "风险管控": {"average": 73.0, "excellent": 86.0},
                        "合规管理": {"average": 71.0, "excellent": 88.0},
                        "创新能力": {"average": 78.0, "excellent": 90.0},
                        "可持续发展": {"average": 68.0, "excellent": 85.0}
                    },
                    "benchmark_companies": ["行业领先企业"]
                }
            }
        }
    
    def get_industry_data(self, industry: str) -> Dict:
        """获取行业数据"""
        if industry not in self.benchmarks['industries']:
            industry = "其他"
        return self.benchmarks['industries'][industry]
    
    def get_comparison_data(self, enterprise_score: float, industry: str, 
                           enterprise_size: str = "大型") -> Dict:
        """获取企业与行业的对比数据"""
        industry_data = self.get_industry_data(industry)
        benchmarks = industry_data['benchmarks']
        
        position = self._calculate_position(enterprise_score, benchmarks)
        ranking = self._calculate_ranking(enterprise_score, benchmarks, 
                                         industry_data['total_enterprises'])
        
        return {
            'enterprise_score': enterprise_score,
            'industry_average': benchmarks['average'],
            'industry_excellent': benchmarks['excellent'],
            'same_size_average': benchmarks['same_size_avg'],
            'national_benchmark': benchmarks['benchmark'],
            'international_advanced': benchmarks['international'],
            'position': position,
            'ranking': ranking,
            'total_enterprises': industry_data['total_enterprises'],
            'large_enterprises': industry_data['large_enterprises'],
            'benchmark_companies': industry_data['benchmark_companies'],
            'data_source': 'benchmark'
        }
    
    def _calculate_position(self, score: float, benchmarks: Dict) -> str:
        """计算企业在行业中的相对位置"""
        if score >= benchmarks['benchmark']:
            return "行业标杆"
        elif score >= benchmarks['excellent']:
            return "行业领先"
        elif score >= benchmarks['same_size_avg']:
            return "优秀水平"
        elif score >= benchmarks['average']:
            return "超过平均"
        else:
            return "需要提升"
    
    def _calculate_ranking(self, score: float, benchmarks: Dict, 
                          total_enterprises: int) -> Dict:
        """计算企业排名"""
        if score >= benchmarks['benchmark']:
            percentile = 95
        elif score >= benchmarks['excellent']:
            percentile = 90
        elif score >= benchmarks['same_size_avg']:
            percentile = 75
        elif score >= benchmarks['average']:
            percentile = 50
        else:
            percentile = max(10, int((score / benchmarks['average']) * 50))
        
        rank = int(total_enterprises * (100 - percentile) / 100)
        
        return {
            'percentile': percentile,
            'rank': rank,
            'description': f"前{100-percentile}%"
        }
    
    def get_dimension_comparison(self, enterprise_dimensions: Dict, 
                                industry: str) -> List[Dict]:
        """获取各维度的行业对比"""
        industry_data = self.get_industry_data(industry)
        dimension_benchmarks = industry_data['dimensions']
        
        comparisons = []
        
        dimension_mapping = {
            '党建引领': '治理方向性',
            '产权结构': '治理规范性',
            '公司治理结构和机制': '治理有效性',
            '战略管理': '治理有效性',
            '内控、风险与合规管理': '风险管控',
            '科学民主管理': '治理有效性',
            '科技创新': '创新能力',
            '社会责任与企业文化': '可持续发展',
            '家族企业治理': '治理规范性'
        }
        
        for dim_name, dim_data in enterprise_dimensions.items():
            standard_dim = dimension_mapping.get(dim_name, '治理有效性')
            
            if standard_dim in dimension_benchmarks:
                benchmark = dimension_benchmarks[standard_dim]
                enterprise_percentage = dim_data.get('percentage', 0)
                
                gap_to_average = enterprise_percentage - benchmark['average']
                gap_to_excellent = enterprise_percentage - benchmark['excellent']
                
                if enterprise_percentage >= benchmark['excellent']:
                    performance = "优秀水平"
                    level = "超过行业优秀"
                elif enterprise_percentage >= benchmark['average']:
                    performance = "先进领域"
                    level = "超过行业平均"
                else:
                    performance = "改进空间"
                    level = "低于行业平均"
                
                comparisons.append({
                    'dimension': dim_name,
                    'standard_dimension': standard_dim,
                    'enterprise_score': enterprise_percentage,
                    'industry_average': benchmark['average'],
                    'industry_excellent': benchmark['excellent'],
                    'gap_to_average': gap_to_average,
                    'gap_to_excellent': gap_to_excellent,
                    'performance': performance,
                    'level': level
                })
        
        return comparisons
    
    def generate_improvement_suggestions(self, comparisons: List[Dict]) -> Dict:
        """基于对比结果生成改进建议"""
        suggestions = {
            'urgent': [],
            'important': [],
            'maintain': []
        }
        
        for comp in comparisons:
            if comp['enterprise_score'] < comp['industry_average']:
                suggestions['urgent'].append({
                    'dimension': comp['dimension'],
                    'current': comp['enterprise_score'],
                    'target': comp['industry_average'],
                    'gap': abs(comp['gap_to_average']),
                    'priority': '高',
                    'suggestion': f"该维度得分率{comp['enterprise_score']:.1f}%，低于行业平均{comp['industry_average']:.1f}%，建议优先改进"
                })
            elif comp['enterprise_score'] < comp['industry_excellent']:
                suggestions['important'].append({
                    'dimension': comp['dimension'],
                    'current': comp['enterprise_score'],
                    'target': comp['industry_excellent'],
                    'gap': abs(comp['gap_to_excellent']),
                    'priority': '中',
                    'suggestion': f"该维度得分率{comp['enterprise_score']:.1f}%，超过行业平均但低于优秀水平，建议持续优化"
                })
            else:
                suggestions['maintain'].append({
                    'dimension': comp['dimension'],
                    'current': comp['enterprise_score'],
                    'priority': '低',
                    'suggestion': f"该维度得分率{comp['enterprise_score']:.1f}%，已达到行业优秀水平，建议保持优势"
                })
        
        return suggestions


if __name__ == '__main__':
    print("[OK] 行业分析模块已加载")