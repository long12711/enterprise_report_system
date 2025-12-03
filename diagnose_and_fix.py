#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
诊断和修复应用问题
"""
import os
import sys
import json

print("=" * 60)
print("应用诊断和修复工具")
print("=" * 60)

# 1. 检查存储目录
print("\n[1] 检查存储目录...")
storage_dir = 'storage'
if os.path.exists(storage_dir):
    print(f"✓ {storage_dir} 目录存在")
else:
    print(f"✗ {storage_dir} 目录不存在，正在创建...")
    os.makedirs(storage_dir, exist_ok=True)
    print(f"✓ {storage_dir} 目录已创建")

# 2. 检查数据文件
print("\n[2] 检查数据文件...")
data_files = {
    'storage/experts.json': {'items': []},
    'storage/expert_evaluations.json': {'items': []},
    'storage/enterprises.json': {'items': []},
    'storage/users.json': {'items': []},
    'storage/special_submissions.json': {'items': []}
}

for file_path, default_data in data_files.items():
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = len(data.get('items', []))
            print(f"✓ {file_path} 存在 ({count} 条记录)")
        except Exception as e:
            print(f"✗ {file_path} 读取失败: {e}")
    else:
        print(f"✗ {file_path} 不存在，正在创建...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=2)
        print(f"✓ {file_path} 已创建")

# 3. 检查模板文件
print("\n[3] 检查模板文件...")
template_files = [
    'templates/admin_login.html',
    'templates/portal_chamber.html',
    'templates/index.html',
    'templates/api_test.html'
]

for template in template_files:
    if os.path.exists(template):
        size = os.path.getsize(template)
        print(f"✓ {template} 存在 ({size} 字节)")
    else:
        print(f"✗ {template} 不存在")

# 4. 检查 app.py
print("\n[4] 检查 app.py...")
if os.path.exists('app.py'):
    size = os.path.getsize('app.py')
    print(f"✓ app.py 存在 ({size} 字节)")
    
    # 尝试导入
    try:
        from app import app
        print("✓ app.py 可以成功导入")
        
        # 检查路由
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        print(f"✓ 应用包含 {len(routes)} 个路由")
        
        # 检查关键路由
        key_routes = ['/login', '/logout', '/', '/portal/chamber', '/api/portal/chamber/experts']
        for route in key_routes:
            if any(route in r for r in routes):
                print(f"  ✓ 路由 {route} 存在")
            else:
                print(f"  ✗ 路由 {route} 不存在")
                
    except Exception as e:
        print(f"✗ app.py 导入失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ app.py 不存在")

# 5. 检查依赖
print("\n[5] 检查依赖...")
try:
    import flask
    print(f"✓ Flask {flask.__version__} 已安装")
except ImportError:
    print("✗ Flask 未安装，请运行: pip install flask")

try:
    import pandas
    print(f"✓ Pandas {pandas.__version__} 已安装")
except ImportError:
    print("⚠ Pandas 未安装（可选）")

# 6. 建议
print("\n[6] 建议...")
print("✓ 所有检查完成")
print("\n启动应用的命令:")
print("  python start_server.py")
print("\n或者:")
print("  python app.py")
print("\n访问应用:")
print("  http://localhost:5000/")
print("  http://localhost:5000/login")
print("  http://localhost:5000/portal/chamber")

print("\n" + "=" * 60)
print("诊断完成！")
print("=" * 60)

