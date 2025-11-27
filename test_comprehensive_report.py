"""
测试生成综合分析报告
"""
import os
from comprehensive_analysis_generator import ComprehensiveAnalysisGenerator

def test_comprehensive_report():
    """测试生成综合分析报告"""
    print("\n" + "="*60)
    print("综合分析报告生成测试")
    print("="*60)

    # 查找submissions文件夹中的Excel文件
    submissions_folder = 'submissions'

    if not os.path.exists(submissions_folder):
        print(f"\n[ERROR] 未找到submissions文件夹")
        print("请确保有企业已提交问卷")
        return

    # 获取所有Excel文件
    excel_files = [
        os.path.join(submissions_folder, f)
        for f in os.listdir(submissions_folder)
        if f.endswith('.xlsx')
    ]

    if not excel_files:
        print(f"\n[ERROR] submissions文件夹中没有Excel文件")
        print("请先通过在线问卷提交或上传Excel文件")
        return

    if len(excel_files) < 2:
        print(f"\n[WARN] 只有 {len(excel_files)} 个问卷文件")
        print("建议至少有2-3个企业数据才能体现综合分析的价值")
        print("但仍将继续生成报告...")

    print(f"\n找到 {len(excel_files)} 个问卷文件")

    # 生成综合报告
    print("\n开始生成综合分析报告...")
    try:
        generator = ComprehensiveAnalysisGenerator()
        report_path = generator.generate_comprehensive_report(excel_files)

        print("\n" + "="*60)
        print("✅ 综合分析报告生成成功！")
        print("="*60)
        print(f"\n报告位置：{os.path.abspath(report_path)}")
        print(f"\n包含企业数：{len(excel_files)}")
        print(f"\n请用Word打开查看：")
        print(f"  {report_path}")
        print("\n" + "="*60)

        # 自动打开报告（Windows）
        try:
            os.startfile(report_path)
            print("\n已自动打开报告文件")
        except:
            print("\n请手动打开报告文件")

    except Exception as e:
        print(f"\n[ERROR] 生成失败：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_comprehensive_report()
    input("\n按Enter键退出...")
