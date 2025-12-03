"""验证生成的问卷是否包含所有题目"""
from docx import Document

# 读取生成的问卷
doc = Document('output/questionnaires/调查问卷_初级_20251201_103357.docx')

# 统计表格和行数
tables = [t for t in doc.tables]
print(f'文档中的表格数量: {len(tables)}')

total_rows = 0
for i, table in enumerate(tables, 1):
    rows = len(table.rows) - 1  # 减去表头
    total_rows += rows
    print(f'表格{i}: {rows}行（不含表头）')

print(f'\n总问题行数: {total_rows}')
print(f'预期问题数: 64')
print(f'是否匹配: {"✓" if total_rows == 64 else "✗"}')

# 检查序号
print('\n检查序号连续性:')
all_seq_nums = []
for table in tables:
    for row in table.rows[1:]:  # 跳过表头
        seq_text = row.cells[0].text.strip()
        if seq_text and seq_text.isdigit():
            all_seq_nums.append(int(seq_text))

all_seq_nums.sort()
print(f'序号范围: {min(all_seq_nums)} - {max(all_seq_nums)}')
print(f'序号数量: {len(all_seq_nums)}')

# 检查是否有缺失的序号
expected = set(range(1, 65))
actual = set(all_seq_nums)
missing = expected - actual
if missing:
    print(f'缺失的序号: {sorted(missing)}')
else:
    print('✓ 所有序号完整')