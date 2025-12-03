import pandas as pd

# 读取南开大学的指标文件
file_path = 'survey_generator/南开大学-现代企业制度指数评价体系初稿2025.10.22（单独指标）(1).xlsx'

# 读取初级sheet
df = pd.read_excel(file_path, sheet_name='初级')

print('=' * 80)
print('南开大学指标体系 - 初级')
print('=' * 80)
print(f'\n总共 {len(df)} 个指标')
print(f'\n列名: {df.columns.tolist()}')

print('\n' + '=' * 80)
print('前10个指标示例（查看评分标准）')
print('=' * 80)

# 显示前10行的关键列
key_columns = []
for col in ['序号', '一级指标', '二级指标', '三级指标', '指标类型', '分值', '评分准则', '评分标准', '打分标准']:
    if col in df.columns:
        key_columns.append(col)

if key_columns:
    print(df[key_columns].head(10).to_string())
else:
    print(df.head(10).to_string())

# 统计指标类型
print('\n' + '=' * 80)
print('指标类型统计')
print('=' * 80)
if '指标类型' in df.columns:
    print(df['指标类型'].value_counts())
else:
    print('未找到"指标类型"列')

# 查看分值分布
print('\n' + '=' * 80)
print('分值统计')
print('=' * 80)
if '分值' in df.columns:
    print(f'最小分值: {df["分值"].min()}')
    print(f'最大分值: {df["分值"].max()}')
    print(f'总分: {df["分值"].sum()}')
    print(f'\n分值分布:')
    print(df['分值'].value_counts().sort_index())