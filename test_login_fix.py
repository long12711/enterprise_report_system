#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试登录修复
"""
import json

print("=" * 70)
print("登录修复验证")
print("=" * 70)

# 检查 admin_login.html 是否已修复
print("\n[1] 检查 admin_login.html...")
try:
    with open('templates/admin_login.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否使用了正确的 API 端点
    if "fetch('/login'" in content:
        print("✓ 使用了正确的 API 端点 /login")
    else:
        print("✗ 未找到正确的 API 端点")
    
    # 检查是否包含 role 参数
    if "role: 'chamber_of_commerce'" in content:
        print("✓ 包含 role 参数")
    else:
        print("✗ 未找到 role 参数")
    
    # 检查是否跳转到正确的页面
    if "/portal/chamber" in content:
        print("✓ 跳转到正确的页面 /portal/chamber")
    else:
        print("✗ 未找到正确的跳转页面")
        
except Exception as e:
    print(f"✗ 检查失败: {e}")

# 检查 app.py 是否有正确的路由
print("\n[2] 检查 app.py...")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查 /login 路由
    if "@app.route('/login'" in content:
        print("✓ 存在 /login 路由")
    else:
        print("✗ 未找到 /login 路由")
    
    # 检查 /portal/chamber 路由
    if "@app.route('/portal/chamber')" in content:
        print("✓ 存在 /portal/chamber 路由")
    else:
        print("✗ 未找到 /portal/chamber 路由")
    
    # 检查认证装饰器
    if "@_role_required('chamber_of_commerce')" in content:
        print("✓ 存在角色检查装饰器")
    else:
        print("✗ 未找到角色检查装饰器")
        
except Exception as e:
    print(f"✗ 检查失败: {e}")

# 测试应用导入
print("\n[3] 测试应用导入...")
try:
    from app import app
    print("✓ 应用导入成功")
    
    # 检查路由
    routes = [str(rule) for rule in app.url_map.iter_rules()]
    
    if any('/login' in r for r in routes):
        print("✓ /login 路由可访问")
    else:
        print("✗ /login 路由不可访问")
    
    if any('/portal/chamber' in r for r in routes):
        print("✓ /portal/chamber 路由可访问")
    else:
        print("✗ /portal/chamber 路由不可访问")
    
    if any('/api/portal/chamber/experts' in r for r in routes):
        print("✓ /api/portal/chamber/experts 路由可访问")
    else:
        print("✗ /api/portal/chamber/experts 路由不可访问")
        
except Exception as e:
    print(f"✗ 应用导入失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("验证完成！")
print("=" * 70)
print("\n现在可以启动应用:")
print("  python run_app.py")
print("\n然后访问:")
print("  http://localhost:5000/login")
print("\n使用以下凭证登录:")
print("  用户名: admin")
print("  密码: admin")

