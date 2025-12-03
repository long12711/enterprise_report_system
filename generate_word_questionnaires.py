"""
生成南开问卷Word版本
使用当前的nankai_indicators.xlsx文件
"""

import sys
import os

# 添加survey_generator到路径
sys.path.insert(0, 'survey_generator')

from nankai_questionnaire_generator import NankaiQuestionnaireGenerator

def main():
    """生成所有级别的Word问卷"""
    
    # 使用当前的Excel文件
    excel_path = "nankai_indicators.xlsx"
    
    if not os.path.exists(excel_path):
        print(f"错误：找不到文件 {excel_path}")
        return
    
    print("=" * 60)
    print("南开问卷Word版本生成器")
    print("=" * 60)
    print(f"Excel文件：{excel_path}")
    print()
    
    try:
        # 创建生成器
        print("正在加载Excel数据...")
        generator = NankaiQuestionnaireGenerator(excel_path)
        print()
        
        # 生成所有级别的问卷
        print("正在生成Word问卷...")
        output_dir = "survey_generator/output/questionnaires"
        results = generator.generate_all_questionnaires(output_dir)
        
        print()
        print("=" * 60)
        print("✅ 问卷生成完成！")
        print("=" * 60)
        
        for level, path in results.items():
            file_size = os.path.getsize(path) / 1024  # KB
            print(f"📄 {level}问卷：{path} ({file_size:.1f} KB)")
        
        print()
        print("说明：")
        print("- 每个问卷包含完整的题目、评分准则、选项和佐证材料要求")
        print("- 问卷采用表格形式，便于打印和填写")
        print("- 可以直接用于线下调查或作为参考文档")
        
    except Exception as e:
        print(f"❌ 生成失败：{str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()