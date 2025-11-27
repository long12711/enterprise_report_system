"""
现代企业制度评价系统 - 主控制脚本
功能：
1. 生成问卷
2. 解析问卷并计算得分
3. 生成企业自评报告
4. 生成整体分析报告
"""
import os
import sys
from datetime import datetime
from questionnaire_generator import QuestionnaireGenerator
from score_calculator import ScoreCalculator
from enterprise_report_generator import EnterpriseReportGenerator
from overall_report_generator import OverallAnalysisReportGenerator
from pdf_report_generator import PDFReportGenerator


def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("    现代企业制度指数评价系统")
    print("="*60)
    print("1. 生成单个问卷")
    print("2. 批量生成问卷")
    print("3. 生成企业自评报告 - Word格式")
    print("4. 生成企业自评报告 - PDF格式（专业版）")
    print("5. 生成整体分析报告（需多个已填写问卷）")
    print("6. 测试完整流程（演示）")
    print("0. 退出")
    print("="*60)


def generate_single_questionnaire():
    """生成单个问卷"""
    print("\n[功能] 生成单个问卷")
    generator = QuestionnaireGenerator()

    enterprise_name = input("请输入企业名称（直接回车则使用默认）: ").strip()
    if not enterprise_name:
        enterprise_name = "示例企业"

    output_path = f'问卷_{enterprise_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'

    try:
        file_path = generator.generate_questionnaire(output_path, enterprise_name)
        print(f"\n[SUCCESS] 问卷已生成: {file_path}")
        print(f"[提示] 请使用Excel打开该文件，填写后保存，然后使用功能3生成报告")
    except Exception as e:
        print(f"\n[ERROR] 生成失败: {e}")


def generate_batch_questionnaires():
    """批量生成问卷"""
    print("\n[功能] 批量生成问卷")

    excel_file = input("请输入包含企业名单的Excel文件路径（包含'企业名称'列）: ").strip()

    if not os.path.exists(excel_file):
        print(f"[ERROR] 文件不存在: {excel_file}")
        return

    try:
        import pandas as pd
        df = pd.read_excel(excel_file)

        if '企业名称' not in df.columns:
            print("[ERROR] Excel文件中没有'企业名称'列")
            return

        generator = QuestionnaireGenerator()
        output_folder = f'问卷批量_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

        generated_files = generator.generate_batch_questionnaires(df, output_folder)

        print(f"\n[SUCCESS] 共生成{len(generated_files)}份问卷")
        print(f"[提示] 问卷保存在文件夹: {output_folder}")

    except Exception as e:
        print(f"\n[ERROR] 批量生成失败: {e}")


def generate_enterprise_report():
    """生成企业自评报告（Word）"""
    print("\n[功能] 生成企业自评报告（Word格式）")

    questionnaire_file = input("请输入已填写的问卷Excel文件路径: ").strip()

    if not os.path.exists(questionnaire_file):
        print(f"[ERROR] 文件不存在: {questionnaire_file}")
        return

    try:
        generator = EnterpriseReportGenerator()
        report_path = generator.generate_report(questionnaire_file)

        print(f"\n[SUCCESS] 企业自评报告已生成: {report_path}")
        print(f"[提示] 请使用Word打开查看报告")

    except Exception as e:
        print(f"\n[ERROR] 生成报告失败: {e}")
        import traceback
        traceback.print_exc()


def generate_enterprise_pdf_report():
    """生成企业自评报告（PDF）"""
    print("\n[功能] 生成企业自评报告（PDF专业版）")

    questionnaire_file = input("请输入已填写的问卷Excel文件路径: ").strip()

    if not os.path.exists(questionnaire_file):
        print(f"[ERROR] 文件不存在: {questionnaire_file}")
        return

    try:
        generator = PDFReportGenerator()
        report_path = generator.generate_report(questionnaire_file)

        print(f"\n[SUCCESS] PDF专业报告已生成: {report_path}")
        print(f"[提示] 请使用PDF阅读器打开查看报告")

    except Exception as e:
        print(f"\n[ERROR] 生成PDF报告失败: {e}")
        import traceback
        traceback.print_exc()


def generate_overall_report():
    """生成整体分析报告"""
    print("\n[功能] 生成整体分析报告")

    folder = input("请输入包含已填写问卷的文件夹路径（或输入文件列表，用逗号分隔）: ").strip()

    questionnaire_files = []

    # 判断是文件夹还是文件列表
    if os.path.isdir(folder):
        # 扫描文件夹中的所有Excel文件
        for file in os.listdir(folder):
            if file.endswith('.xlsx') or file.endswith('.xls'):
                questionnaire_files.append(os.path.join(folder, file))
    else:
        # 按逗号分隔的文件列表
        files = [f.strip() for f in folder.split(',')]
        questionnaire_files = [f for f in files if os.path.exists(f)]

    if not questionnaire_files:
        print("[ERROR] 未找到有效的问卷文件")
        return

    print(f"\n[INFO] 找到{len(questionnaire_files)}个问卷文件")

    try:
        generator = OverallAnalysisReportGenerator()
        report_path = generator.generate_report(questionnaire_files)

        print(f"\n[SUCCESS] 整体分析报告已生成: {report_path}")
        print(f"[提示] 请使用Word打开查看报告")

    except Exception as e:
        print(f"\n[ERROR] 生成报告失败: {e}")
        import traceback
        traceback.print_exc()


def test_demo():
    """测试演示完整流程"""
    print("\n[演示] 测试完整流程")
    print("[说明] 这将生成一个测试问卷，您可以填写后测试报告生成功能")

    try:
        # 1. 生成问卷
        print("\n步骤1: 生成测试问卷...")
        generator = QuestionnaireGenerator()
        questionnaire_path = generator.generate_questionnaire(
            output_path='测试问卷_演示.xlsx',
            enterprise_name='演示科技有限公司'
        )
        print(f"[OK] 问卷已生成: {questionnaire_path}")

        print("\n" + "="*60)
        print("[重要提示]")
        print("1. 请使用Excel打开以下文件并填写问卷:")
        print(f"   {questionnaire_path}")
        print("2. 在'企业信息'工作表中填写企业基本信息")
        print("3. 在'问卷'工作表中填写各个问题的答案")
        print("4. 保存文件后，可以使用菜单选项3生成自评报告")
        print("="*60)

        # 提供示例数据说明
        print("\n[填写建议]")
        print("- 合规类问题：选择'是'或'否'")
        print("- 有效性问题：选择'很有效'、'比较有效'等")
        print("- 如果问题不适用，可选择'不适用'")

    except Exception as e:
        print(f"\n[ERROR] 演示失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    while True:
        print_menu()
        choice = input("\n请选择功能 (0-6): ").strip()

        if choice == '0':
            print("\n感谢使用！再见！")
            break
        elif choice == '1':
            generate_single_questionnaire()
        elif choice == '2':
            generate_batch_questionnaires()
        elif choice == '3':
            generate_enterprise_report()
        elif choice == '4':
            generate_enterprise_pdf_report()
        elif choice == '5':
            generate_overall_report()
        elif choice == '6':
            test_demo()
        else:
            print("\n[ERROR] 无效的选择，请重新输入")

        input("\n按Enter键继续...")


if __name__ == '__main__':
    print("\n正在初始化系统...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n[ERROR] 系统错误: {e}")
        import traceback
        traceback.print_exc()
