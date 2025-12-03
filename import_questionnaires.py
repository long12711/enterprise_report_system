#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""直接导入问卷"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from docx_questionnaire_importer import DocxQuestionnaireImporter

print("=" * 80)
print("开始导入问卷...")
print("=" * 80)

importer = DocxQuestionnaireImporter()

docx_dir = r'D:\xwechat_files\wxid_nfuq3yq5zb4x22_dcf3\msg\file\2025-12'

print(f"\n[1] 导入目录: {docx_dir}")

result = importer.import_all_questionnaires(docx_dir)

print(f"\n[2] 导入结果:")
for level, survey_id in result.items():
    if survey_id:
        print(f"  ✓ {level}级: {survey_id}")
    else:
        print(f"  ✗ {level}级: 导入失败")

print(f"\n[3] 验证导入:")
surveys = importer.list_surveys()
print(f"  总共有 {len(surveys)} 个问卷")

for survey in surveys:
    questions = importer.get_survey_questions(survey['id'])
    print(f"\n  {survey['name']}:")
    print(f"    - 级别: {survey['level']}")
    print(f"    - 问题数: {len(questions)}")
    if questions:
        print(f"    - 第一个问题: {questions[0]['question_text'][:60]}")

print("\n" + "=" * 80)
print("导入完成！")
print("=" * 80)

