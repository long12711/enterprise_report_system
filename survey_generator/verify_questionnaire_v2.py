# -*- coding: utf-8 -*-
"""
验证问卷生成器V2的输出
检查选项格式和填空项提取
"""

from docx import Document
import os
import sys

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_questionnaire(docx_path):
    """验证问卷格式"""
    print(f"\n{'='*60}")
    print(f"验证文件: {os.path.basename(docx_path)}")
    print(f"{'='*60}")
    
    doc = Document(docx_path)
    
    # 统计信息
    total_questions = 0
    questions_with_abc = 0
    questions_with_fill_blanks = 0
    
    # 遍历所有表格
    for table in doc.tables:
        # 跳过表头
        for i, row in enumerate(table.rows):
            if i == 0:  # 跳过表头
                continue
            
            cells = row.cells
            if len(cells) >= 6:
                seq_num = cells[0].text.strip()
                if seq_num and seq_num.isdigit():
                    total_questions += 1
                    
                    # 检查选项列（第5列，索引4）
                    options = cells[4].text.strip()
                    if "A. 符合 B. 部分符合 C. 不符合" in options:
                        questions_with_abc += 1
                    
                    # 检查补充数据/说明列（第6列，索引5）
                    supplement = cells[5].text.strip()
                    if supplement and "______" in supplement:
                        questions_with_fill_blanks += 1
                        print(f"  题目 {seq_num}: {supplement}")
    
    print(f"\n统计结果:")
    print(f"  总题目数: {total_questions}")
    print(f"  使用ABC选项的题目: {questions_with_abc} ({questions_with_abc/total_questions*100:.1f}%)")
    print(f"  包含填空项的题目: {questions_with_fill_blanks} ({questions_with_fill_blanks/total_questions*100:.1f}%)")
    
    # 验证结果
    if questions_with_abc == total_questions:
        print(f"\n[OK] 所有题目都使用了统一的ABC选项格式")
    else:
        print(f"\n[ERROR] 有 {total_questions - questions_with_abc} 个题目未使用ABC格式")
    
    if questions_with_fill_blanks > 0:
        print(f"[OK] 成功提取了 {questions_with_fill_blanks} 个填空项")
    else:
        print(f"[WARN] 没有提取到填空项")
    
    return {
        'total': total_questions,
        'abc_format': questions_with_abc,
        'fill_blanks': questions_with_fill_blanks
    }

def main():
    """主函数"""
    output_dir = "output/questionnaires"
    
    # 查找最新生成的问卷
    files = [f for f in os.listdir(output_dir) if f.endswith('.docx') and '20251201_104504' in f]
    
    if not files:
        print("未找到最新生成的问卷文件")
        return
    
    results = {}
    for filename in sorted(files):
        filepath = os.path.join(output_dir, filename)
        level = filename.split('_')[2]  # 提取级别
        results[level] = verify_questionnaire(filepath)
    
    # 总结
    print(f"\n{'='*60}")
    print("总体验证结果")
    print(f"{'='*60}")
    for level, stats in results.items():
        print(f"\n{level}:")
        print(f"  题目数: {stats['total']}")
        print(f"  ABC格式: {stats['abc_format']}/{stats['total']}")
        print(f"  填空项: {stats['fill_blanks']}")

if __name__ == "__main__":
    main()