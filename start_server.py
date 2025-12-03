#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动 Flask 服务器
"""
import os
import sys

# 确保存储目录存在
os.makedirs('storage', exist_ok=True)

try:
    from app import app
    print("=" * 60)
    print("现代企业制度评价系统 - Flask 服务器")
    print("=" * 60)
    print("\n✓ 应用启动成功")
    print("\n访问地址:")
    print("  - 首页: http://localhost:5000/")
    print("  - 工商联门户: http://localhost:5000/portal/chamber")
    print("  - 登录: http://localhost:5000/login")
    print("\n测试用户:")
    print("  - 用户名: admin")
    print("  - 密码: admin")
    print("  - 角色: chamber_of_commerce")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
except Exception as e:
    print(f"✗ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

