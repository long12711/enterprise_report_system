import pandas as pd

df = pd.read_excel('指标体系.xlsx', sheet_name=0)
print('所有列名:')
print(df.columns.tolist())
print('\n前5行示例数据:')
print(df.head(5)[['序号', '一级指标', '三级指标', '指标类型', '分值']].to_string())