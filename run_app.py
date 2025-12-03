#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单的应用启动脚本
"""
import os
import sys

# 确保存储目录存在
os.makedirs('storage', exist_ok=True)
os.makedirs('storage/reports', exist_ok=True)
os.makedirs('storage/submissions', exist_ok=True)
os.makedirs('storage/uploads', exist_ok=True)
os.makedirs('storage/tutoring_logs', exist_ok=True)
os.makedirs('storage/special_submissions', exist_ok=True)

print("=" * 70)
print("现代企业制度评价系统 - Flask 应用启动")
print("=" * 70)

try:
    print("\n[1] 导入 Flask 应用...")
    from app import app
    print("✓ Flask 应用导入成功")
    
    print("\n[2] 启动应用...")
    print("\n" + "=" * 70)
    print("应用已启动！")
    print("=" * 70)
    print("\n访问地址:")
    print("  • 首页: http://localhost:5000/")
    print("  • 登录: http://localhost:5000/login")
    print("  • 工商联门户: http://localhost:5000/portal/chamber")
    print("  • API 测试: http://localhost:5000/test")
    print("\n测试用户:")
    print("  • 用户名: admin")
    print("  • 密码: admin")
    print("  • 角色: 工商联用户")
    print("\n按 Ctrl+C 停止应用")
    print("=" * 70 + "\n")
    
    # 启动应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
    
except ImportError as e:
    print(f"\n✗ 导入失败: {e}")
    print("\n请确保已安装所有依赖:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

