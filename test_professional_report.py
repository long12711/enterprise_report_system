"""
测试生成专业版报告
"""
import os
from professional_report_generator import ProfessionalReportGenerator

def test_professional_report():
    """测试生成专业版报告"""
    print("\n" + "="*60)
    print("专业版报告生成测试")
    print("="*60)

    # 查找submissions文件夹中的Excel文件
    submissions_folder = 'submissions'

    if not os.path.exists(submissions_folder):
        print(f"\n[ERROR] 未找到submissions文件夹")
        print("请确保有企业已提交问卷")
        return

    # 获取所有Excel文件
    excel_files = [f for f in os.listdir(submissions_folder) if f.endswith('.xlsx')]

    if not excel_files:
        print(f"\n[ERROR] submissions文件夹中没有Excel文件")
        print("请先通过在线问卷提交或上传Excel文件")
        return

    print(f"\n找到 {len(excel_files)} 个问卷文件：")
    for idx, file in enumerate(excel_files, 1):
        print(f"  {idx}. {file}")

    # 选择第一个文件作为测试
    test_file = os.path.join(submissions_folder, excel_files[0])
    print(f"\n使用文件：{excel_files[0]}")

    # 生成专业报告
    print("\n开始生成专业版报告...")
    try:
        generator = ProfessionalReportGenerator()
        report_path = generator.generate_report(test_file)

        print("\n" + "="*60)
        print("✅ 报告生成成功！")
        print("="*60)
        print(f"\n报告位置：{os.path.abspath(report_path)}")
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
    test_professional_report()
    input("\n按Enter键退出...")
