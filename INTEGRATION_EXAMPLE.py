"""
集成示例 - 展示如何使用独立的问卷生成和报告生成模块

这个文件演示了多种使用场景，可以作为参考进行开发
"""

import os
import sys
import pandas as pd
from datetime import datetime

# ============================================================================
# 场景 1: 基础使用 - 生成单个问卷
# ============================================================================

def scenario_1_basic_questionnaire():
    """场景1: 生成单个问卷"""
    print("\n" + "="*60)
    print("场景 1: 生成单个问卷")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    try:
        # 初始化生成器
        generator = QuestionnaireGenerator()
        
        # 生成问卷
        output_file = generator.generate_questionnaire(
            output_path='示例问卷.xlsx',
            enterprise_name='示例企业有限公司'
        )
        
        print(f"✓ 问卷生成成功: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        return None


# ============================================================================
# 场景 2: 批量生成 - 生成多个企业的问卷
# ============================================================================

def scenario_2_batch_questionnaires():
    """场景2: 批量生成问卷"""
    print("\n" + "="*60)
    print("场景 2: 批量生成问卷")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    try:
        # 准备企业数据
        enterprises_data = {
            '企业名称': [
                '金龙企业有限公司',
                '今麦郎食品有限公司',
                '示例科技有限公司',
                '创新制造有限公司'
            ]
        }
        enterprises_df = pd.DataFrame(enterprises_data)
        
        # 初始化生成器
        generator = QuestionnaireGenerator()
        
        # 批量生成
        output_folder = 'batch_questionnaires'
        files = generator.generate_batch_questionnaires(
            enterprises_df,
            output_folder=output_folder
        )
        
        print(f"✓ 已生成 {len(files)} 份问卷:")
        for file in files:
            print(f"  - {file}")
        
        return files
        
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        return []


# ============================================================================
# 场景 3: 报告生成 - 从问卷生成专业报告
# ============================================================================

def scenario_3_generate_report(questionnaire_file):
    """场景3: 生成专业报告"""
    print("\n" + "="*60)
    print("场景 3: 生成专业报告")
    print("="*60)
    
    try:
        from report_generator import ProfessionalReportGenerator
        from score_calculator import ScoreCalculator
        
        # 检查问卷文件是否存在
        if not os.path.exists(questionnaire_file):
            print(f"✗ 问卷文件不存在: {questionnaire_file}")
            return None
        
        # 初始化计算器和生成器
        calculator = ScoreCalculator()
        report_generator = ProfessionalReportGenerator(
            score_calculator=calculator
        )
        
        # 生成报告
        report_file = report_generator.generate_report(
            questionnaire_file=questionnaire_file
        )
        
        print(f"✓ 报告生成成功: {report_file}")
        return report_file
        
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        print("  提示: 确保 score_calculator.py 在项目根目录")
        return None
    except Exception as e:
        print(f"✗ 生成失败: {e}")
        return None


# ============================================================================
# 场景 4: 完整流程 - 问卷生成 + 报告生成
# ============================================================================

def scenario_4_complete_workflow():
    """场景4: 完整工作流 - 问卷生成 + 报告生成"""
    print("\n" + "="*60)
    print("场景 4: 完整工作流 (问卷 + 报告)")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    try:
        # 第一步: 生成问卷
        print("\n[步骤1] 生成问卷...")
        generator = QuestionnaireGenerator()
        
        questionnaire_file = generator.generate_questionnaire(
            output_path='workflow_questionnaire.xlsx',
            enterprise_name='工作流测试企业'
        )
        print(f"✓ 问卷已生成: {questionnaire_file}")
        
        # 第二步: 生成报告
        print("\n[步骤2] 生成报告...")
        try:
            from report_generator import ProfessionalReportGenerator
            from score_calculator import ScoreCalculator
            
            calculator = ScoreCalculator()
            report_generator = ProfessionalReportGenerator(
                score_calculator=calculator
            )
            
            report_file = report_generator.generate_report(
                questionnaire_file=questionnaire_file
            )
            print(f"✓ 报告已生成: {report_file}")
            
            print("\n✓ 完整工作流执行成功!")
            return questionnaire_file, report_file
            
        except ImportError:
            print("⚠ 报告生成需要 score_calculator.py")
            return questionnaire_file, None
        
    except Exception as e:
        print(f"✗ 工作流执行失败: {e}")
        return None, None


# ============================================================================
# 场景 5: 自定义配置 - 使用自定义指标文件
# ============================================================================

def scenario_5_custom_config():
    """场景5: 自定义配置"""
    print("\n" + "="*60)
    print("场景 5: 自定义配置")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    try:
        # 使用自定义指标文件
        custom_indicator_file = '指标体系.xlsx'
        
        if os.path.exists(custom_indicator_file):
            generator = QuestionnaireGenerator(
                indicator_file=custom_indicator_file
            )
            
            output_file = generator.generate_questionnaire(
                output_path='custom_questionnaire.xlsx',
                enterprise_name='自定义配置企业'
            )
            
            print(f"✓ 使用自定义指标文件生成问卷: {output_file}")
            return output_file
        else:
            print(f"⚠ 自定义指标文件不存在: {custom_indicator_file}")
            print("  使用默认配置...")
            
            generator = QuestionnaireGenerator()
            output_file = generator.generate_questionnaire(
                enterprise_name='默认配置企业'
            )
            print(f"✓ 使用默认配置生成问卷: {output_file}")
            return output_file
            
    except Exception as e:
        print(f"✗ 自定义配置失败: {e}")
        return None


# ============================================================================
# 场景 6: 错误处理 - 演示错误处理机制
# ============================================================================

def scenario_6_error_handling():
    """场景6: 错误处理"""
    print("\n" + "="*60)
    print("场景 6: 错误处理")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    # 测试1: 无效的输出路径
    print("\n[测试1] 无效的输出路径...")
    try:
        generator = QuestionnaireGenerator()
        generator.generate_questionnaire(
            output_path='/invalid/path/questionnaire.xlsx'
        )
    except Exception as e:
        print(f"✓ 捕获到错误: {type(e).__name__}: {e}")
    
    # 测试2: 不存在的问卷文件
    print("\n[测试2] 不存在的问卷文件...")
    try:
        from report_generator import ProfessionalReportGenerator
        from score_calculator import ScoreCalculator
        
        calculator = ScoreCalculator()
        report_gen = ProfessionalReportGenerator(score_calculator=calculator)
        report_gen.generate_report(
            questionnaire_file='nonexistent_questionnaire.xlsx'
        )
    except FileNotFoundError as e:
        print(f"✓ 捕获到文件错误: {e}")
    except Exception as e:
        print(f"✓ 捕获到错误: {type(e).__name__}: {e}")
    
    print("\n✓ 错误处理演示完成")


# ============================================================================
# 场景 7: 数据处理 - 从CSV/Excel读取企业数据并生成问卷
# ============================================================================

def scenario_7_data_processing():
    """场景7: 数据处理"""
    print("\n" + "="*60)
    print("场景 7: 数据处理 (从Excel读取企业数据)")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    
    try:
        # 创建示例企业数据
        sample_data = {
            '企业名称': ['企业A', '企业B', '企业C'],
            '行业': ['制造业', '服务业', '科技业'],
            '规模': ['大型', '中型', '小型']
        }
        
        # 保存为Excel
        sample_file = 'sample_enterprises.xlsx'
        df = pd.DataFrame(sample_data)
        df.to_excel(sample_file, index=False)
        print(f"✓ 创建示例数据文件: {sample_file}")
        
        # 读取数据
        enterprises_df = pd.read_excel(sample_file)
        print(f"✓ 读取企业数据: {len(enterprises_df)} 条记录")
        
        # 生成问卷
        generator = QuestionnaireGenerator()
        files = generator.generate_batch_questionnaires(
            enterprises_df,
            output_folder='data_processing_questionnaires'
        )
        
        print(f"✓ 已生成 {len(files)} 份问卷")
        
        # 清理示例文件
        os.remove(sample_file)
        print(f"✓ 清理临时文件")
        
        return files
        
    except Exception as e:
        print(f"✗ 数据处理失败: {e}")
        return []


# ============================================================================
# 场景 8: 性能测试 - 测试大量生成
# ============================================================================

def scenario_8_performance_test():
    """场景8: 性能测试"""
    print("\n" + "="*60)
    print("场景 8: 性能测试 (生成10份问卷)")
    print("="*60)
    
    from survey_generator import QuestionnaireGenerator
    import time
    
    try:
        # 准备数据
        enterprises = [f'企业{i}' for i in range(1, 11)]
        df = pd.DataFrame({'企业名称': enterprises})
        
        # 测试生成速度
        generator = QuestionnaireGenerator()
        
        start_time = time.time()
        files = generator.generate_batch_questionnaires(
            df,
            output_folder='performance_test_questionnaires'
        )
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        avg_time = elapsed_time / len(files)
        
        print(f"✓ 生成 {len(files)} 份问卷耗时: {elapsed_time:.2f} 秒")
        print(f"  平均每份问卷: {avg_time:.2f} 秒")
        
        return files
        
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return []


# ============================================================================
# 主函数 - 运行所有场景
# ============================================================================

def main():
    """主函数 - 运行所有场景"""
    print("\n" + "="*60)
    print("企业报告系统 - 独立模块集成示例")
    print("="*60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # 运行场景
    scenarios = [
        ("基础使用", scenario_1_basic_questionnaire),
        ("批量生成", scenario_2_batch_questionnaires),
        ("自定义配置", scenario_5_custom_config),
        ("错误处理", scenario_6_error_handling),
        ("数据处理", scenario_7_data_processing),
        ("性能测试", scenario_8_performance_test),
    ]
    
    results = {}
    
    for name, scenario_func in scenarios:
        try:
            result = scenario_func()
            results[name] = "成功" if result else "失败"
        except Exception as e:
            print(f"\n✗ 场景执行失败: {e}")
            results[name] = "异常"
    
    # 打印总结
    print("\n" + "="*60)
    print("执行总结")
    print("="*60)
    
    for name, status in results.items():
        status_symbol = "✓" if status == "成功" else "✗"
        print(f"{status_symbol} {name}: {status}")
    
    print("\n" + "="*60)
    print("示例执行完成")
    print("="*60)


# ============================================================================
# 快速测试函数
# ============================================================================

def quick_test():
    """快速测试 - 仅生成一个问卷"""
    print("\n快速测试: 生成单个问卷\n")
    
    from survey_generator import QuestionnaireGenerator
    
    generator = QuestionnaireGenerator()
    file = generator.generate_questionnaire(
        enterprise_name='快速测试企业'
    )
    
    print(f"问卷已生成: {file}")
    return file


# ============================================================================
# 入口点
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='企业报告系统 - 独立模块集成示例'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='快速测试模式'
    )
    parser.add_argument(
        '--scenario',
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8],
        help='运行指定场景'
    )
    
    args = parser.parse_args()
    
    if args.quick:
        quick_test()
    elif args.scenario:
        scenarios_map = {
            1: scenario_1_basic_questionnaire,
            2: scenario_2_batch_questionnaires,
            3: scenario_3_generate_report,
            4: scenario_4_complete_workflow,
            5: scenario_5_custom_config,
            6: scenario_6_error_handling,
            7: scenario_7_data_processing,
            8: scenario_8_performance_test,
        }
        scenarios_map[args.scenario]()
    else:
        main()

