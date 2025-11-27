#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析指标体系Excel文件
"""

import pandas as pd
import sys

try:
    # 读取Excel文件
    df = pd.read_excel('指标体系_备份.xlsx')
    
    print("=" * 80)
    print("指标体系文件分析")
    print("=" * 80)
    
    print("\n文件读取成功！")
    print(f"\n数据形状: {df.shape[0]} 行, {df.shape[1]} 列")
    
    print("\n列名:")
    for i, col in enumerate(df.columns):
        print(f"  {i+1}. {col}")
    
    print("\n前15行数据:")
    print(df.head(15).to_string())
    
    print("\n" + "=" * 80)
    print("数据类型:")
    print(df.dtypes)
    
    print("\n" + "=" * 80)
    print("非空值统计:")
    print(df.info())
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

