"""
终端命令行工具 - 管理在线提交的问卷并生成报告
功能：
1. 查看所有在线提交的问卷
2. 为指定企业生成报告
3. 批量生成报告并发送邮件
"""
import os
import sys
from datetime import datetime
from questionnaire_submission_manager import QuestionnaireSubmissionManager
from enterprise_report_generator import EnterpriseReportGenerator
from pdf_report_generator import PDFReportGenerator
from notification_service import NotificationService


def print_menu():
    """打印菜单"""
    print("\n" + "="*60)
    print("    在线问卷管理系统 - 终端工具")
    print("="*60)
    print("1. 查看所有在线提交的问卷")
    print("2. 为指定企业生成Word报告")
    print("3. 为指定企业生成PDF报告")
    print("4. 批量生成报告并发送邮件")
    print("5. 查看特定提交的详细信息")
    print("0. 退出")
    print("="*60)


def view_all_submissions(manager):
    """查看所有提交"""
    print("\n[功能] 查看所有在线提交的问卷")

    submissions = manager.get_all_submissions()

    if not submissions:
        print("\n[INFO] 暂无在线提交记录")
        return

    print(f"\n[INFO] 共有 {len(submissions)} 条提交记录:\n")
    print(f"{'序号':<6} {'企业名称':<30} {'提交时间':<20} {'文件名'}")
    print("-" * 80)

    for idx, sub in enumerate(submissions, 1):
        submit_time = datetime.fromtimestamp(sub['submit_time']).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{idx:<6} {sub['enterprise_name']:<30} {submit_time:<20} {sub['filename']}")


def generate_word_report_for_submission(manager):
    """为指定企业生成Word报告"""
    print("\n[功能] 为指定企业生成Word报告")

    submissions = manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无在线提交记录")
        return

    # 显示列表
    print(f"\n共有 {len(submissions)} 条提交记录:")
    for idx, sub in enumerate(submissions, 1):
        print(f"{idx}. {sub['enterprise_name']}")

    try:
        choice = int(input("\n请输入序号（直接回车生成所有）: ").strip() or "0")

        if choice == 0:
            # 生成所有
            print("\n[INFO] 开始批量生成Word报告...")
            report_generator = EnterpriseReportGenerator()

            for idx, sub in enumerate(submissions, 1):
                try:
                    excel_path = sub['filepath'].replace('.json', '.xlsx').replace('submission_', '问卷_')

                    if os.path.exists(excel_path):
                        report_path = report_generator.generate_report(excel_path)
                        print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: {report_path}")
                    else:
                        print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: Excel文件不存在")

                except Exception as e:
                    print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: 生成失败 - {e}")

            print("\n[SUCCESS] 批量生成完成!")

        elif 1 <= choice <= len(submissions):
            # 生成单个
            selected_sub = submissions[choice - 1]
            excel_path = selected_sub['filepath'].replace('.json', '.xlsx').replace('submission_', '问卷_')

            if not os.path.exists(excel_path):
                print(f"\n[ERROR] Excel文件不存在: {excel_path}")
                return

            report_generator = EnterpriseReportGenerator()
            report_path = report_generator.generate_report(excel_path)

            print(f"\n[SUCCESS] Word报告已生成: {report_path}")

        else:
            print("\n[ERROR] 无效的选择")

    except ValueError:
        print("\n[ERROR] 请输入有效的数字")
    except Exception as e:
        print(f"\n[ERROR] 生成报告失败: {e}")
        import traceback
        traceback.print_exc()


def generate_pdf_report_for_submission(manager):
    """为指定企业生成PDF报告"""
    print("\n[功能] 为指定企业生成PDF报告")

    submissions = manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无在线提交记录")
        return

    # 显示列表
    print(f"\n共有 {len(submissions)} 条提交记录:")
    for idx, sub in enumerate(submissions, 1):
        print(f"{idx}. {sub['enterprise_name']}")

    try:
        choice = int(input("\n请输入序号（直接回车生成所有）: ").strip() or "0")

        if choice == 0:
            # 生成所有
            print("\n[INFO] 开始批量生成PDF报告...")
            report_generator = PDFReportGenerator()

            for idx, sub in enumerate(submissions, 1):
                try:
                    excel_path = sub['filepath'].replace('.json', '.xlsx').replace('submission_', '问卷_')

                    if os.path.exists(excel_path):
                        report_path = report_generator.generate_report(excel_path)
                        print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: {report_path}")
                    else:
                        print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: Excel文件不存在")

                except Exception as e:
                    print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: 生成失败 - {e}")

            print("\n[SUCCESS] 批量生成完成!")

        elif 1 <= choice <= len(submissions):
            # 生成单个
            selected_sub = submissions[choice - 1]
            excel_path = selected_sub['filepath'].replace('.json', '.xlsx').replace('submission_', '问卷_')

            if not os.path.exists(excel_path):
                print(f"\n[ERROR] Excel文件不存在: {excel_path}")
                return

            report_generator = PDFReportGenerator()
            report_path = report_generator.generate_report(excel_path)

            print(f"\n[SUCCESS] PDF报告已生成: {report_path}")

        else:
            print("\n[ERROR] 无效的选择")

    except ValueError:
        print("\n[ERROR] 请输入有效的数字")
    except Exception as e:
        print(f"\n[ERROR] 生成报告失败: {e}")
        import traceback
        traceback.print_exc()


def batch_generate_and_send_email(manager):
    """批量生成报告并发送邮件"""
    print("\n[功能] 批量生成报告并发送邮件")

    submissions = manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无在线提交记录")
        return

    print(f"\n[INFO] 共有 {len(submissions)} 条提交记录")

    # 确认操作
    confirm = input("\n是否为所有企业生成报告并发送邮件? (y/n): ").strip().lower()

    if confirm != 'y':
        print("\n[INFO] 操作已取消")
        return

    # 选择报告格式
    print("\n请选择报告格式:")
    print("1. Word格式")
    print("2. PDF格式")
    print("3. Word + PDF（两种格式都生成）")

    format_choice = input("\n请输入选项 (1-3): ").strip()

    # 初始化
    notification_service = NotificationService()
    word_generator = EnterpriseReportGenerator() if format_choice in ['1', '3'] else None
    pdf_generator = PDFReportGenerator() if format_choice in ['2', '3'] else None

    success_count = 0
    failed_count = 0

    print("\n[INFO] 开始处理...\n")

    for idx, sub in enumerate(submissions, 1):
        try:
            # 获取提交数据
            submission_data = manager.get_submission_by_filename(sub['filename'])
            enterprise_info = submission_data['enterprise_info']
            enterprise_name = enterprise_info.get('企业名称', '')
            email = enterprise_info.get('联系人邮箱', '')
            contact_name = enterprise_info.get('联系人姓名', '')

            if not email:
                print(f"  [{idx}/{len(submissions)}] {enterprise_name}: 跳过（无邮箱地址）")
                failed_count += 1
                continue

            # 查找Excel文件
            excel_path = sub['filepath'].replace('.json', '.xlsx').replace('submission_', '问卷_')

            if not os.path.exists(excel_path):
                print(f"  [{idx}/{len(submissions)}] {enterprise_name}: 跳过（Excel文件不存在）")
                failed_count += 1
                continue

            # 生成报告
            report_paths = []

            if word_generator:
                word_path = word_generator.generate_report(excel_path)
                report_paths.append(word_path)

            if pdf_generator:
                pdf_path = pdf_generator.generate_report(excel_path)
                report_paths.append(pdf_path)

            # 发送邮件
            email_sent = notification_service.send_email(
                to_email=email,
                enterprise_name=enterprise_name,
                contact_name=contact_name,
                report_url='',  # 终端生成不需要URL
                attachment_path=report_paths[0] if report_paths else None
            )

            if email_sent:
                print(f"  [{idx}/{len(submissions)}] {enterprise_name}: 成功")
                success_count += 1
            else:
                print(f"  [{idx}/{len(submissions)}] {enterprise_name}: 邮件发送失败")
                failed_count += 1

        except Exception as e:
            print(f"  [{idx}/{len(submissions)}] {sub['enterprise_name']}: 失败 - {e}")
            failed_count += 1

    print("\n" + "="*60)
    print(f"[总结] 处理完成")
    print(f"  成功: {success_count}")
    print(f"  失败: {failed_count}")
    print(f"  总计: {len(submissions)}")
    print("="*60)


def view_submission_details(manager):
    """查看特定提交的详细信息"""
    print("\n[功能] 查看提交详细信息")

    submissions = manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无在线提交记录")
        return

    # 显示列表
    print(f"\n共有 {len(submissions)} 条提交记录:")
    for idx, sub in enumerate(submissions, 1):
        print(f"{idx}. {sub['enterprise_name']}")

    try:
        choice = int(input("\n请输入序号: ").strip())

        if 1 <= choice <= len(submissions):
            selected_sub = submissions[choice - 1]

            # 读取详细数据
            submission_data = manager.get_submission_by_filename(selected_sub['filename'])
            enterprise_info = submission_data['enterprise_info']
            answers = submission_data['answers']

            # 显示企业信息
            print("\n" + "="*60)
            print("企业基本信息:")
            print("="*60)
            for key, value in enterprise_info.items():
                print(f"  {key}: {value}")

            # 显示答题统计
            print("\n" + "="*60)
            print("答题统计:")
            print("="*60)
            print(f"  已回答问题数: {len(answers)}")
            print(f"  答案示例（前5题）:")
            for seq, answer in list(answers.items())[:5]:
                print(f"    第{seq}题: {answer}")

            # 计算得分
            print("\n正在计算得分...")
            score_summary = manager.calculate_score_for_submission(submission_data)

            print("\n" + "="*60)
            print("评价得分:")
            print("="*60)
            print(f"  总得分: {score_summary['total_score']:.1f} / {score_summary['max_possible_score']:.1f}")
            print(f"  完成度: {score_summary['score_percentage']:.1f}%")

            from score_calculator import ScoreCalculator
            calculator = ScoreCalculator()
            level, evaluation = calculator.get_evaluation_level(score_summary['score_percentage'])
            print(f"  评价等级: {evaluation}")

        else:
            print("\n[ERROR] 无效的选择")

    except ValueError:
        print("\n[ERROR] 请输入有效的数字")
    except Exception as e:
        print(f"\n[ERROR] 查看详情失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    # 初始化管理器
    manager = QuestionnaireSubmissionManager()

    while True:
        print_menu()
        choice = input("\n请选择功能 (0-5): ").strip()

        if choice == '0':
            print("\n感谢使用！再见！")
            break
        elif choice == '1':
            view_all_submissions(manager)
        elif choice == '2':
            generate_word_report_for_submission(manager)
        elif choice == '3':
            generate_pdf_report_for_submission(manager)
        elif choice == '4':
            batch_generate_and_send_email(manager)
        elif choice == '5':
            view_submission_details(manager)
        else:
            print("\n[ERROR] 无效的选择，请重新输入")

        input("\n按Enter键继续...")


if __name__ == '__main__':
    print("\n正在初始化在线问卷管理系统...")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n[ERROR] 系统错误: {e}")
        import traceback
        traceback.print_exc()
