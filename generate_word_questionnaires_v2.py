"""
使用V2版本生成器生成Word问卷
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from survey_generator.nankai_questionnaire_generator_v2 import NankaiQuestionnaireGeneratorV2


def main():
    """使用V2生成器生成Word问卷"""
    
    print("=" * 60)
    print("南开大学问卷生成器 V2")
    print("=" * 60)
    print()
    
    # Excel文件路径 - 使用正确的文件名
    excel_path = "nankai_indicators.xlsx"
    
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"[错误] 找不到Excel文件: {excel_path}")
        print("请确保文件存在于当前目录")
        return
    
    print(f"[文件] Excel文件: {excel_path}")
    print()
    
    try:
        # 创建生成器
        print("[进行中] 正在初始化生成器...")
        generator = NankaiQuestionnaireGeneratorV2(excel_path)
        print("[成功] 生成器初始化成功")
        print()
        
        # 输出目录
        output_dir = "survey_generator/output/questionnaires"
        
        # 生成所有级别的问卷
        print("[进行中] 正在生成Word问卷...")
        print()
        results = generator.generate_all_questionnaires(output_dir)
        
        print()
        print("=" * 60)
        print("[成功] 问卷生成完成！")
        print("=" * 60)
        print()
        print("生成的文件：")
        for level, path in results.items():
            print(f"  - {level}: {path}")
        print()
        print("V2版本特点：")
        print("  * 统一选项格式：A. 符合 B. 部分符合 C. 不符合")
        print("  * 自动提取填空项到'补充数据/说明'列")
        print("  * 仿照参考文件格式")
        print("  * 包含企业基本信息部分")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("[错误] 生成失败")
        print("=" * 60)
        print(f"错误信息: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()