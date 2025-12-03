"""
测试行业对比功能
"""
from industry_analyzer import IndustryAnalyzer
from pdf_report_generator import PDFReportGenerator
import os

def test_industry_analyzer():
    """测试行业分析器"""
    print("\n" + "="*60)
    print("测试行业分析器")
    print("="*60)
    
    analyzer = IndustryAnalyzer()
    
    # 测试1: 获取行业数据
    print("\n[测试1] 获取软件和信息技术服务业数据...")
    industry_data = analyzer.get_industry_data("软件和信息技术服务业")
    print(f"✓ 行业企业总数: {industry_data['total_enterprises']}")
    print(f"✓ 大型企业数: {industry_data['large_enterprises']}")
    print(f"✓ 行业平均分: {industry_data['benchmarks']['average']}%")
    print(f"✓ 行业优秀水平: {industry_data['benchmarks']['excellent']}%")
    print(f"✓ 标杆企业: {', '.join(industry_data['benchmark_companies'])}")
    
    # 测试2: 获取对比数据
    print("\n[测试2] 获取企业对比数据...")
    comparison = analyzer.get_comparison_data(93.1, "软件和信息技术服务业")
    print(f"✓ 企业得分: {comparison['enterprise_score']}%")
    print(f"✓ 行业平均: {comparison['industry_average']}%")
    print(f"✓ 相对位置: {comparison['position']}")
    print(f"✓ 排名: {comparison['ranking']['description']}")
    print(f"✓ 数据来源: {comparison['data_source']}")
    
    # 测试3: 维度对比
    print("\n[测试3] 测试维度对比...")
    test_dimensions = {
        '党建引领': {'score': 19.5, 'max_score': 23.5, 'percentage': 83.0},
        '产权结构': {'score': 25.6, 'max_score': 27.0, 'percentage': 94.8},
        '公司治理结构和机制': {'score': 49.5, 'max_score': 51.5, 'percentage': 96.1}
    }
    
    dim_comparisons = analyzer.get_dimension_comparison(test_dimensions, "软件和信息技术服务业")
    print(f"✓ 对比维度数: {len(dim_comparisons)}")
    for comp in dim_comparisons:
        print(f"  - {comp['dimension']}: {comp['enterprise_score']:.1f}% ({comp['performance']})")
    
    # 测试4: 改进建议
    print("\n[测试4] 生成改进建议...")
    suggestions = analyzer.generate_improvement_suggestions(dim_comparisons)
    print(f"✓ 紧急改进项: {len(suggestions['urgent'])}")
    print(f"✓ 重要改进项: {len(suggestions['important'])}")
    print(f"✓ 保持优势项: {len(suggestions['maintain'])}")
    
    print("\n[OK] 行业分析器测试通过！")
    return True

def test_pdf_generation():
    """测试PDF报告生成（如果有测试数据）"""
    print("\n" + "="*60)
    print("测试PDF报告生成")
    print("="*60)
    
    # 查找最新的问卷提交文件
    submissions_dir = 'storage/submissions'
    if not os.path.exists(submissions_dir):
        print("[SKIP] 没有找到提交数据目录，跳过PDF生成测试")
        return False
    
    # 查找Excel文件
    excel_files = [f for f in os.listdir(submissions_dir) if f.startswith('问卷_') and f.endswith('.xlsx')]
    
    if not excel_files:
        print("[SKIP] 没有找到问卷数据文件，跳过PDF生成测试")
        return False
    
    # 使用最新的文件
    latest_file = sorted(excel_files)[-1]
    questionnaire_file = os.path.join(submissions_dir, latest_file)
    
    print(f"\n[测试] 使用问卷文件: {latest_file}")
    
    try:
        generator = PDFReportGenerator()
        output_path = 'test_industry_comparison_report.pdf'
        
        print("[INFO] 开始生成PDF报告（包含行业对比）...")
        report_path = generator.generate_report(questionnaire_file, output_path)
        
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path) / 1024  # KB
            print(f"✓ PDF报告生成成功: {report_path}")
            print(f"✓ 文件大小: {file_size:.1f} KB")
            print("\n[OK] PDF报告生成测试通过！")
            print(f"\n请查看生成的报告: {report_path}")
            return True
        else:
            print("[ERROR] PDF文件未生成")
            return False
            
    except Exception as e:
        print(f"[ERROR] PDF生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("行业对比功能测试")
    print("="*60)
    
    results = []
    
    # 测试1: 行业分析器
    try:
        result1 = test_industry_analyzer()
        results.append(("行业分析器", result1))
    except Exception as e:
        print(f"\n[ERROR] 行业分析器测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(("行业分析器", False))
    
    # 测试2: PDF生成
    try:
        result2 = test_pdf_generation()
        results.append(("PDF报告生成", result2))
    except Exception as e:
        print(f"\n[ERROR] PDF生成测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        results.append(("PDF报告生成", False))
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！行业对比功能已成功实现！")
    else:
        print("\n⚠️  部分测试失败，请检查错误信息")

if __name__ == '__main__':
    main()