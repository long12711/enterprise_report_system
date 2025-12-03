# -*- coding: utf-8 -*-
"""
问卷导入测试脚本
用于测试从 Word 文档导入问卷题目的功能
"""
import os
import sys
import json
from docx_questionnaire_importer import DocxQuestionnaireImporter

def test_import():
    """测试导入功能"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 80)
    print("现代企业制度指数评价问卷 - 导入测试")
    print("=" * 80)
    
    # 初始化导入器
    importer = DocxQuestionnaireImporter()
    
    # Word 文档路径
    docx_dir = r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12'
    
    print(f"\n[1] 检查目录: {docx_dir}")
    if not os.path.isdir(docx_dir):
        print(f"    ✗ 目录不存在")
        return False
    
    # 列出目录中的 Word 文件
    docx_files = [f for f in os.listdir(docx_dir) if f.endswith('.docx')]
    print(f"    ✓ 找到 {len(docx_files)} 个 Word 文件:")
    for f in docx_files:
        print(f"      - {f}")
    
    # 导入问卷
    print(f"\n[2] 导入问卷...")
    result = importer.import_all_questionnaires(docx_dir)
    
    print("    导入结果:")
    for level, survey_id in result.items():
        if survey_id:
            print(f"    ✓ {level}级: {survey_id}")
        else:
            print(f"    ✗ {level}级: 导入失败")
    
    # 验证导入结果
    print(f"\n[3] 验证导入结果...")
    surveys = importer.list_surveys()
    print(f"    ✓ 总共有 {len(surveys)} 个问卷")
    
    for survey in surveys:
        print(f"\n    问卷: {survey['name']}")
        print(f"      - ID: {survey['id']}")
        print(f"      - 级别: {survey['level']}")
        print(f"      - 问题数: {survey['total_questions']}")
        print(f"      - 状态: {survey['status']}")
        
        # 获取问题列表
        questions = importer.get_survey_questions(survey['id'])
        if questions:
            print(f"      - 样本问题:")
            for i, q in enumerate(questions[:3]):
                print(f"        {i+1}. {q['question_text'][:50]}...")
                print(f"           类型: {q['question_type']}, 分值: {q['score']}")
                if q.get('requires_file'):
                    print(f"           需要上传文件: 是")
    
    # 显示数据库信息
    print(f"\n[4] 数据库信息...")
    db = importer.load_db()
    print(f"    ✓ 问卷数: {len(db.get('surveys', []))}")
    print(f"    ✓ 问题数: {len(db.get('questions', []))}")
    print(f"    ✓ 提交数: {len(db.get('submissions', []))}")
    
    # 显示数据库文件位置
    print(f"\n[5] 数据库文件位置...")
    print(f"    {importer.db_path}")
    
    print("\n" + "=" * 80)
    print("✓ 测试完成")
    print("=" * 80)
    
    return True


def test_api():
    """测试 API 接口"""
    print("\n" + "=" * 80)
    print("API 接口测试")
    print("=" * 80)
    
    importer = DocxQuestionnaireImporter()
    
    # 获取问卷列表
    print("\n[1] 获取问卷列表...")
    surveys = importer.list_surveys()
    print(f"    ✓ 获取到 {len(surveys)} 个问卷")
    
    if surveys:
        # 获取第一个问卷的详情
        survey_id = surveys[0]['id']
        print(f"\n[2] 获取问卷详情 ({survey_id})...")
        survey = importer.get_survey(survey_id)
        print(f"    ✓ 问卷名称: {survey['name']}")
        print(f"    ✓ 问卷级别: {survey['level']}")
        
        # 获取问卷问题
        print(f"\n[3] 获取问卷问题...")
        questions = importer.get_survey_questions(survey_id)
        print(f"    ✓ 获取到 {len(questions)} 个问题")
        
        if questions:
            q = questions[0]
            print(f"\n    第一个问题:")
            print(f"      - ID: {q['id']}")
            print(f"      - 文本: {q['question_text']}")
            print(f"      - 类型: {q['question_type']}")
            print(f"      - 分值: {q['score']}")
            print(f"      - 一级指标: {q['level1']}")
            print(f"      - 二级指标: {q['level2']}")
            print(f"      - 适用对象: {q['applicable']}")
            print(f"      - 需要文件: {q['requires_file']}")
    
    # 按级别获取问卷
    print(f"\n[4] 按级别获取问卷...")
    for level in ['初级', '中级', '高级']:
        survey = importer.get_survey_by_level(level)
        if survey:
            print(f"    ✓ {level}级: {survey['name']}")
        else:
            print(f"    ✗ {level}级: 未找到")
    
    print("\n" + "=" * 80)
    print("✓ API 测试完成")
    print("=" * 80)


def test_data_structure():
    """测试数据结构"""
    print("\n" + "=" * 80)
    print("数据结构验证")
    print("=" * 80)
    
    importer = DocxQuestionnaireImporter()
    db = importer.load_db()
    
    print("\n[1] 数据库结构...")
    print(f"    ✓ 包含的键: {list(db.keys())}")
    
    print("\n[2] 问卷结构...")
    if db.get('surveys'):
        survey = db['surveys'][0]
        print(f"    ✓ 问卷字段: {list(survey.keys())}")
    
    print("\n[3] 问题结构...")
    if db.get('questions'):
        question = db['questions'][0]
        print(f"    ✓ 问题字段: {list(question.keys())}")
    
    print("\n" + "=" * 80)
    print("✓ 数据结构验证完成")
    print("=" * 80)


def show_sample_data():
    """显示样本数据"""
    print("\n" + "=" * 80)
    print("样本数据")
    print("=" * 80)
    
    importer = DocxQuestionnaireImporter()
    db = importer.load_db()
    
    if db.get('surveys'):
        print("\n[1] 样本问卷:")
        survey = db['surveys'][0]
        print(json.dumps(survey, ensure_ascii=False, indent=2))
    
    if db.get('questions'):
        print("\n[2] 样本问题:")
        question = db['questions'][0]
        print(json.dumps(question, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    try:
        # 运行测试
        test_import()
        test_api()
        test_data_structure()
        show_sample_data()
        
        print("\n✓ 所有测试完成！")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

