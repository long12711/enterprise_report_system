"""
生成示例PDF报告
使用现有的问卷数据生成包含行业对比的PDF报告
"""
from pdf_report_generator import PDFReportGenerator
import os
from datetime import datetime

def generate_sample_report():
    """生成示例报告"""
    print("\n" + "="*60)
    print("生成示例PDF报告（含行业对比）")
    print("="*60)
    
    # 查找最新的问卷文件
    submissions_dir = 'storage/submissions'
    excel_files = [f for f in os.listdir(submissions_dir) 
                   if f.startswith('问卷_') and f.endswith('.xlsx')]
    
    if not excel_files:
        print("[ERROR] 没有找到问卷数据文件")
        return None
    
    # 使用最新的文件
    latest_file = sorted(excel_files)[-1]
    questionnaire_file = os.path.join(submissions_dir, latest_file)
    
    print(f"\n[INFO] 使用问卷文件: {latest_file}")
    
    try:
        # 初始化PDF生成器（指定正确的指标文件路径）
        from score_calculator import ScoreCalculator
        
        # 先创建一个使用正确路径的ScoreCalculator
        calculator = ScoreCalculator(indicator_file='nankai_indicators.xlsx')
        
        # 然后创建PDF生成器
        generator = PDFReportGenerator()
        # 替换生成器中的calculator
        generator.calculator = calculator
        
        # 生成输出文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f'示例报告_含行业对比_{timestamp}.pdf'
        
        print(f"[INFO] 开始生成PDF报告...")
        print(f"[INFO] 输出文件: {output_path}")
        
        # 生成报告
        report_path = generator.generate_report(questionnaire_file, output_path)
        
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path) / 1024  # KB
            print(f"\n{'='*60}")
            print(f"✓ PDF报告生成成功！")
            print(f"{'='*60}")
            print(f"文件路径: {report_path}")
            print(f"文件大小: {file_size:.1f} KB")
            print(f"\n报告包含以下章节:")
            print(f"  1. 封面")
            print(f"  2. 目录")
            print(f"  3. 执行摘要")
            print(f"  4. 企业基本情况")
            print(f"  5. 评价概览与图表分析")
            print(f"  6. 行业对比分析 ⭐ (新增)")
            print(f"  7. 维度分析")
            print(f"  8. 详细评价结果")
            print(f"  9. 风险评估与预警")
            print(f"  10. 改进路径规划")
            print(f"  11. 合规性检查清单")
            print(f"  12. 报告说明与附录")
            print(f"\n请打开PDF文件查看完整报告！")
            print(f"{'='*60}\n")
            
            return report_path
        else:
            print("[ERROR] PDF文件未生成")
            return None
            
    except Exception as e:
        print(f"\n[ERROR] 报告生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    generate_sample_report()