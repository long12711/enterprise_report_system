"""
南开大学问卷生成器 - Excel版本
用于在python-docx未安装时测试功能
"""

import pandas as pd
import os
from datetime import datetime


class NankaiExcelGenerator:
    """Excel格式问卷生成器"""
    
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.data = {}
        self._load_data()
    
    def _load_data(self):
        """加载Excel数据"""
        try:
            self.data['初级'] = pd.read_excel(self.excel_path, sheet_name='初级')
            self.data['中级'] = pd.read_excel(self.excel_path, sheet_name='中级')
            self.data['高级'] = pd.read_excel(self.excel_path, sheet_name='高级')
            print(f"[OK] 成功加载指标数据：")
            print(f"  初级: {len(self.data['初级'])} 条")
            print(f"  中级: {len(self.data['中级'])} 条")
            print(f"  高级: {len(self.data['高级'])} 条")
        except Exception as e:
            raise Exception(f"加载Excel文件失败: {str(e)}")
    
    def _parse_scoring_standard(self, standard: str) -> str:
        """解析打分标准，提取选项（用换行符分隔）"""
        if pd.isna(standard) or not standard:
            return "A. 是\nB. 否"
        
        standard = str(standard).strip()
        
        # 使用正则表达式提取所有选项（A. xxx B. xxx C. xxx D. xxx）
        import re
        # 匹配模式：A. 或 B. 或 C. 或 D. 开头的内容
        options = re.findall(r'([A-D]\.[\s\S]*?)(?=[A-D]\.|$)', standard)
        
        if options:
            # 清理每个选项，去除多余空格
            cleaned_options = [opt.strip() for opt in options if opt.strip()]
            # 用换行符连接
            return '\n'.join(cleaned_options)
        else:
            # 如果没有匹配到标准格式，返回默认选项
            return "A. 是\nB. 否"
    
    def generate_questionnaire(self, level: str, output_path: str = None) -> str:
        """生成Excel格式问卷"""
        if level not in self.data:
            raise ValueError(f"无效的级别: {level}")
        
        df = self.data[level].copy()
        
        # 添加选项列
        df['选项'] = df['打分标准'].apply(self._parse_scoring_standard)
        
        # 添加补充说明列
        df['补充数据/说明'] = df['佐证材料'].fillna('')
        
        # 选择需要的列（添加评分准则列）
        columns_to_include = ['序号', '一级指标', '二级指标', '三级指标']
        
        # 检查是否有评分准则列
        if '评分准则' in df.columns:
            columns_to_include.append('评分准则')
        elif '评分标准' in df.columns:
            columns_to_include.append('评分标准')
        
        columns_to_include.extend(['打分标准', '选项', '补充数据/说明', '佐证材料'])
        
        # 只选择存在的列
        output_df = df[[col for col in columns_to_include if col in df.columns]]
        
        # 生成输出路径
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"调查问卷_{level}_{timestamp}.xlsx"
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 保存Excel
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            output_df.to_excel(writer, sheet_name=f'{level}问卷', index=False)
        
        print(f"[OK] 成功生成{level}问卷: {output_path}")
        return output_path
    
    def generate_all_questionnaires(self, output_dir: str = "output/questionnaires"):
        """生成所有级别问卷"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {}
        
        for level in ['初级', '中级', '高级']:
            output_path = os.path.join(output_dir, f"调查问卷_{level}_{timestamp}.xlsx")
            results[level] = self.generate_questionnaire(level, output_path)
        
        return results


def main():
    """测试函数"""
    print("=" * 60)
    print("南开大学问卷生成器 - Excel版本测试")
    print("=" * 60)
    print()
    
    # Excel文件路径
    excel_path = "../report_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx"
    
    if not os.path.exists(excel_path):
        print(f"[ERROR] 错误：找不到Excel文件")
        print(f"   路径: {excel_path}")
        return
    
    try:
        # 创建生成器
        generator = NankaiExcelGenerator(excel_path)
        print()
        
        # 生成所有问卷
        print("开始生成问卷...")
        print()
        results = generator.generate_all_questionnaires()
        
        print()
        print("=" * 60)
        print("[OK] 问卷生成完成！")
        print("=" * 60)
        for level, path in results.items():
            print(f"  {level}: {path}")
        print()
        
    except Exception as e:
        print(f"[ERROR] 错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()