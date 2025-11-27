"""
批量发送专业报告工具
功能：为所有企业生成专业版报告并通过邮件发送
"""
import os
import sys
from professional_report_generator import ProfessionalReportGenerator
from notification_service import NotificationService
from questionnaire_submission_manager import QuestionnaireSubmissionManager

def batch_send_professional_reports():
    """批量发送专业报告"""
    print("\n" + "="*60)
    print("批量发送专业报告工具")
    print("="*60)

    # 初始化服务
    professional_generator = ProfessionalReportGenerator()
    notification_service = NotificationService()
    submission_manager = QuestionnaireSubmissionManager()

    # 获取所有提交
    submissions = submission_manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无企业提交记录")
        return

    print(f"\n找到 {len(submissions)} 家企业的提交记录\n")

    # 显示企业列表
    for idx, sub in enumerate(submissions, 1):
        print(f"{idx}. {sub['enterprise_name']}")

    print("\n" + "-"*60)
    choice = input("\n是否为所有企业生成专业报告并发送邮件? (y/n): ").strip().lower()

    if choice != 'y':
        print("\n操作已取消")
        return

    # 批量处理
    success_count = 0
    failed_count = 0
    no_email_count = 0

    print("\n开始处理...\n")

    for idx, sub in enumerate(submissions, 1):
        try:
            enterprise_name = sub['enterprise_name']
            print(f"[{idx}/{len(submissions)}] 处理: {enterprise_name}")

            # 获取提交数据
            submission_data = submission_manager.get_submission_by_filename(sub['filename'])
            enterprise_info = submission_data['enterprise_info']

            # 查找Excel文件
            excel_path = os.path.join(
                'submissions',
                sub['filename'].replace('.json', '.xlsx').replace('submission_', '问卷_')
            )

            if not os.path.exists(excel_path):
                print(f"  ❌ Excel文件不存在，跳过")
                failed_count += 1
                continue

            # 生成专业版报告
            print(f"  📄 生成专业版报告...")
            report_path = professional_generator.generate_report(excel_path)
            print(f"  ✅ 报告已生成: {os.path.basename(report_path)}")

            # 获取邮箱
            email = enterprise_info.get('联系人邮箱', '')
            contact_name = enterprise_info.get('联系人姓名', '')

            if not email:
                print(f"  ⚠️  未提供邮箱地址，跳过邮件发送")
                no_email_count += 1
                success_count += 1  # 报告生成成功
                continue

            # 发送邮件
            print(f"  📧 发送邮件到: {email}")
            email_sent = notification_service.send_email(
                to_email=email,
                enterprise_name=enterprise_name,
                contact_name=contact_name,
                report_url='',
                attachment_path=report_path
            )

            if email_sent:
                print(f"  ✅ 邮件发送成功")
                success_count += 1
            else:
                print(f"  ❌ 邮件发送失败")
                failed_count += 1

        except Exception as e:
            print(f"  ❌ 处理失败: {e}")
            failed_count += 1

        print()

    # 汇总统计
    print("=" * 60)
    print("处理完成！")
    print("=" * 60)
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"无邮箱: {no_email_count}")
    print(f"总计: {len(submissions)}")
    print("=" * 60)


def send_single_professional_report():
    """发送单个专业报告"""
    print("\n" + "="*60)
    print("发送单个专业报告")
    print("="*60)

    # 初始化服务
    professional_generator = ProfessionalReportGenerator()
    notification_service = NotificationService()
    submission_manager = QuestionnaireSubmissionManager()

    # 获取所有提交
    submissions = submission_manager.get_all_submissions()

    if not submissions:
        print("\n[ERROR] 暂无企业提交记录")
        return

    print(f"\n找到 {len(submissions)} 家企业的提交记录：\n")

    # 显示列表
    for idx, sub in enumerate(submissions, 1):
        print(f"{idx}. {sub['enterprise_name']}")

    print()
    try:
        choice = int(input("请输入企业序号: ").strip())

        if choice < 1 or choice > len(submissions):
            print("\n[ERROR] 无效的序号")
            return

        selected_sub = submissions[choice - 1]
        enterprise_name = selected_sub['enterprise_name']

        print(f"\n选择的企业: {enterprise_name}")

        # 获取提交数据
        submission_data = submission_manager.get_submission_by_filename(selected_sub['filename'])
        enterprise_info = submission_data['enterprise_info']

        # 查找Excel文件
        excel_path = os.path.join(
            'submissions',
            selected_sub['filename'].replace('.json', '.xlsx').replace('submission_', '问卷_')
        )

        if not os.path.exists(excel_path):
            print(f"\n[ERROR] Excel文件不存在: {excel_path}")
            return

        # 生成专业版报告
        print(f"\n正在生成专业版报告...")
        report_path = professional_generator.generate_report(excel_path)
        print(f"✅ 报告已生成: {report_path}")

        # 获取邮箱
        email = enterprise_info.get('联系人邮箱', '')
        contact_name = enterprise_info.get('联系人姓名', '')

        if not email:
            print(f"\n⚠️  该企业未提供邮箱地址")
            print(f"报告已生成，请手动发送: {report_path}")
            return

        # 确认发送
        confirm = input(f"\n是否发送邮件到 {email}? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\n已取消发送")
            print(f"报告已生成: {report_path}")
            return

        # 发送邮件
        print(f"\n正在发送邮件...")
        email_sent = notification_service.send_email(
            to_email=email,
            enterprise_name=enterprise_name,
            contact_name=contact_name,
            report_url='',
            attachment_path=report_path
        )

        if email_sent:
            print(f"\n✅ 邮件发送成功到 {email}")
        else:
            print(f"\n❌ 邮件发送失败")
            print(f"报告已生成: {report_path}")

    except ValueError:
        print("\n[ERROR] 请输入有效的数字")
    except Exception as e:
        print(f"\n[ERROR] 处理失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主��单"""
    while True:
        print("\n" + "="*60)
        print("专业报告发送工具")
        print("="*60)
        print("1. 批量发送（所有企业）")
        print("2. 发送单个企业")
        print("0. 退出")
        print("="*60)

        choice = input("\n请选择 (0-2): ").strip()

        if choice == '0':
            print("\n退出程序")
            break
        elif choice == '1':
            batch_send_professional_reports()
        elif choice == '2':
            send_single_professional_report()
        else:
            print("\n[ERROR] 无效的选择")

        input("\n按Enter键继续...")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    except Exception as e:
        print(f"\n[ERROR] 系统��误: {e}")
        import traceback
        traceback.print_exc()
