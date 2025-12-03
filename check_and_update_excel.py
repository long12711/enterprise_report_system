"""检查并更新Excel文件的选项格式"""
import pandas as pd
import re

# 读取Excel
excel_path = 'nankai_indicators.xlsx'

print("=" * 60)
print("检查Excel文件的打分标准格式")
print("=" * 60)

for sheet_name in ['初级', '中级', '高级']:
    print(f"\n【{sheet_name}】")
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    
    print(f"总题数: {len(df)}")
    print("\n前3题的打分标准:")
    
    for i in range(min(3, len(df))):
        row = df.iloc[i]
        print(f"\n题{i+1} - {row['三级指标']}")
        standard = str(row['打分标准'])
        print(f"打分标准: {standard[:200]}")
        
        # 检查是否包含"是/否"格式
        if '是' in standard and '否' in standard:
            print("  ⚠️ 发现'是/否'格式，需要更新为'完成/部分完成/未完成'")
        
        # 检查选项格式
        options = re.findall(r'[A-D]\.', standard)
        print(f"  选项数量: {len(options)}")

print("\n" + "=" * 60)
print("建议：")
print("1. 将所有'A. 是 B. 否'格式改为'A. 完成 B. 部分完成 C. 未完成'")
print("2. 在前端添加逻辑：只有选择A或B时才显示填空项")
print("=" * 60)