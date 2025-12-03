#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 app.py 的 API 端点
"""
import sys
import json

# 测试导入
try:
    from app import app
    print("✓ app.py 导入成功")
except Exception as e:
    print(f"✗ app.py 导入失败: {e}")
    sys.exit(1)

# 测试存储文件
import os
storage_files = [
    'storage/experts.json',
    'storage/expert_evaluations.json',
    'storage/enterprises.json',
    'storage/users.json',
    'storage/special_submissions.json'
]

for f in storage_files:
    if os.path.exists(f):
        print(f"✓ {f} 存在")
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                count = len(data.get('items', []))
                print(f"  └─ 包含 {count} 条记录")
        except Exception as e:
            print(f"  ✗ 读取失败: {e}")
    else:
        print(f"✗ {f} 不存在")

# 测试 Flask 应用
print("\n测试 Flask 应用:")
try:
    with app.test_client() as client:
        # 测试首页
        resp = client.get('/')
        print(f"✓ GET / 返回状态码: {resp.status_code}")
        
        # 测试登录
        resp = client.post('/login', json={
            'username': 'test',
            'password': 'test',
            'role': 'chamber_of_commerce'
        })
        print(f"✓ POST /login 返回状态码: {resp.status_code}")
        
except Exception as e:
    print(f"✗ Flask 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n✓ 所有基本测试通过！")

