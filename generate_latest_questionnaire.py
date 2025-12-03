"""
生成最新的南开问卷Word版本
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from survey_generator.nankai_questionnaire_generator import NankaiQuestionnaireGenerator
from datetime import datetime

def main():
    print("=" * 80)
    print("南开大学现代企业制度指数评价问卷生成器")
    print("=" * 80)
    print()
    
    # Excel文件路径
    excel_path = "survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx"
    
    if not os.path.exists(excel_path):
        print(f"[ERROR] 找不到指标文件: {excel_path}")
        return
    
    print(f"[INFO] 使用指标文件: {excel_path}")
    print()
    
    try:
        # 创建生成器
        print("[INFO] 初始化问卷生成器...")
        generator = NankaiQuestionnaireGenerator(excel_path)
        print("[OK] 生成器初始化成功")
        print()
        
        # 创建输出目录
        output_dir = "问卷输出"
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成三个级别的问卷
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("开始生成问卷...")
        print("-" * 80)
        
        results = {}
        for level in ['初级', '中级', '高级']:
            print(f"\n[INFO] 正在生成{level}问卷...")
            output_path = os.path.join(output_dir, f"南开大学现代企业制度指数评价问卷_{level}_{timestamp}.docx")
            result_path = generator.generate_questionnaire(level, output_path)
            results[level] = result_path
            print(f"[OK] {level}问卷生成成功")
        
        print()
        print("=" * 80)
        print("[SUCCESS] 所有问卷生成完成！")
        print("=" * 80)
        print()
        print("生成的文件：")
        for level, path in results.items():
            file_size = os.path.getsize(path) / 1024  # KB
            print(f"  {level}: {path} ({file_size:.1f} KB)")
        print()
        print(f"输出目录: {os.path.abspath(output_dir)}")
        print()
        
    except Exception as e:
        print(f"[ERROR] 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()