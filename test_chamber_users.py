#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工商联用户管理 - 功能测试脚本
"""

import requests
import json
import sys

BASE_URL = 'http://localhost:5000'

# 测试用户
TEST_USERS = {
    'admin_national': {
        'username': 'admin_national',
        'password': '123456',
        'role': 'chamber_of_commerce'
    },
    'admin_beijing': {
        'username': 'admin_beijing',
        'password': '123456',
        'role': 'chamber_of_commerce'
    },
    'admin_chaoyang': {
        'username': 'admin_chaoyang',
        'password': '123456',
        'role': 'chamber_of_commerce'
    }
}

class TestRunner:
    def __init__(self):
        self.session = requests.Session()
        self.passed = 0
        self.failed = 0
        self.current_user = None

    def log(self, message, level='INFO'):
        """打印日志"""
        prefix = f"[{level}]"
        print(f"{prefix} {message}")

    def login(self, username):
        """登录"""
        user_info = TEST_USERS.get(username)
        if not user_info:
            self.log(f"用户 {username} 不存在", 'ERROR')
            return False

        try:
            response = self.session.post(
                f'{BASE_URL}/login',
                json=user_info
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.current_user = username
                    self.log(f"用户 {username} 登录成功")
                    return True
            self.log(f"用户 {username} 登录失败: {response.text}", 'ERROR')
            return False
        except Exception as e:
            self.log(f"登录异常: {e}", 'ERROR')
            return False

    def test_get_users(self, page=1, page_size=10, **filters):
        """测试获取用户列表"""
        try:
            params = {
                'page': page,
                'page_size': page_size,
                **filters
            }
            response = self.session.get(
                f'{BASE_URL}/api/portal/chamber/users',
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    users = data.get('data', {}).get('users', [])
                    total = data.get('data', {}).get('total', 0)
                    self.log(f"获取用户列表成功: {len(users)} 条记录，共 {total} 条")
                    self.passed += 1
                    return True, users
                else:
                    self.log(f"获取用户列表失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False, []
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False, []
        except Exception as e:
            self.log(f"获取用户列表异常: {e}", 'ERROR')
            self.failed += 1
            return False, []

    def test_get_user(self, user_id):
        """测试获取单个用户"""
        try:
            response = self.session.get(
                f'{BASE_URL}/api/portal/chamber/users/{user_id}'
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    user = data.get('data', {})
                    self.log(f"获取用户 {user.get('username')} 成功")
                    self.passed += 1
                    return True, user
                else:
                    self.log(f"获取用户失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False, {}
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False, {}
        except Exception as e:
            self.log(f"获取用户异常: {e}", 'ERROR')
            self.failed += 1
            return False, {}

    def test_create_user(self, user_data):
        """测试创建用户"""
        try:
            response = self.session.post(
                f'{BASE_URL}/api/portal/chamber/users',
                json=user_data
            )
            
            if response.status_code == 201:
                data = response.json()
                if data.get('code') == 201:
                    user_id = data.get('data', {}).get('id')
                    self.log(f"创建用户成功: {user_id}")
                    self.passed += 1
                    return True, user_id
                else:
                    self.log(f"创建用户失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False, None
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False, None
        except Exception as e:
            self.log(f"创建用户异常: {e}", 'ERROR')
            self.failed += 1
            return False, None

    def test_update_user(self, user_id, user_data):
        """测试更新用户"""
        try:
            response = self.session.put(
                f'{BASE_URL}/api/portal/chamber/users/{user_id}',
                json=user_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    self.log(f"更新用户成功: {user_id}")
                    self.passed += 1
                    return True
                else:
                    self.log(f"更新用户失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"更新用户异常: {e}", 'ERROR')
            self.failed += 1
            return False

    def test_delete_user(self, user_id):
        """测试删除用户"""
        try:
            response = self.session.delete(
                f'{BASE_URL}/api/portal/chamber/users/{user_id}'
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    self.log(f"删除用户成功: {user_id}")
                    self.passed += 1
                    return True
                else:
                    self.log(f"删除用户失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False
        except Exception as e:
            self.log(f"删除用户异常: {e}", 'ERROR')
            self.failed += 1
            return False

    def test_get_logs(self):
        """测试获取操作日志"""
        try:
            response = self.session.get(
                f'{BASE_URL}/api/portal/chamber/logs',
                params={'page': 1, 'page_size': 10}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 200:
                    logs = data.get('data', {}).get('logs', [])
                    total = data.get('data', {}).get('total', 0)
                    self.log(f"获取操作日志成功: {len(logs)} 条记录，共 {total} 条")
                    self.passed += 1
                    return True, logs
                else:
                    self.log(f"获取操作日志失败: {data.get('message')}", 'ERROR')
                    self.failed += 1
                    return False, []
            else:
                self.log(f"HTTP 错误: {response.status_code}", 'ERROR')
                self.failed += 1
                return False, []
        except Exception as e:
            self.log(f"获取操作日志异常: {e}", 'ERROR')
            self.failed += 1
            return False, []

    def run_tests(self):
        """运行所有测试"""
        self.log("=" * 60)
        self.log("工商联用户管理系统 - 功能测试")
        self.log("=" * 60)

        # 测试 1: 全联管理员登录
        self.log("\n[测试 1] 全联管理员登录")
        if not self.login('admin_national'):
            self.log("登录失败，停止测试", 'ERROR')
            return

        # 测试 2: 获取所有用户
        self.log("\n[测试 2] 获取所有用户")
        success, users = self.test_get_users()
        if not success or not users:
            self.log("获取用户列表失败", 'ERROR')
            return
        
        first_user_id = users[0]['id']

        # 测试 3: 获取单个用户
        self.log("\n[测试 3] 获取单个用户")
        self.test_get_user(first_user_id)

        # 测试 4: 按层级筛选
        self.log("\n[测试 4] 按层级筛选用户")
        self.test_get_users(level='county')

        # 测试 5: 按角色筛选
        self.log("\n[测试 5] 按角色筛选用户")
        self.test_get_users(role='operator')

        # 测试 6: 按状态筛选
        self.log("\n[测试 6] 按状态筛选用户")
        self.test_get_users(status='active')

        # 测试 7: 搜索用户
        self.log("\n[测试 7] 搜索用户")
        self.test_get_users(keyword='admin')

        # 测试 8: 创建新用户
        self.log("\n[测试 8] 创建新用户")
        new_user_data = {
            'username': 'test_user_' + str(int(__import__('time').time())),
            'email': f'test_{int(__import__("time").time())}@example.com',
            'password': '123456',
            'real_name': '测试用户',
            'phone': '010-12345678',
            'level': 'county',
            'region': '北京朝阳',
            'role': 'operator',
            'status': 'pending'
        }
        success, new_user_id = self.test_create_user(new_user_data)

        # 测试 9: 更新用户
        if success and new_user_id:
            self.log("\n[测试 9] 更新用户")
            self.test_update_user(new_user_id, {
                'status': 'active',
                'phone': '010-87654321'
            })

            # 测试 10: 删除用户
            self.log("\n[测试 10] 删除用户")
            self.test_delete_user(new_user_id)

        # 测试 11: 获取操作日志
        self.log("\n[测试 11] 获取操作日志")
        self.test_get_logs()

        # 测试 12: 省级管理员权限检查
        self.log("\n[测试 12] 省级管理员权限检查")
        self.login('admin_beijing')
        success, users = self.test_get_users()
        if success:
            # 省级管理员应该只能看到本省的用户
            for user in users:
                if user.get('region') and '北京' not in user.get('region', ''):
                    self.log(f"权限检查失败: 看到了非本省用户 {user.get('username')}", 'ERROR')
                    self.failed += 1
                    break
            else:
                self.log("省级管理员权限检查成功")
                self.passed += 1

        # 测试 13: 县市级管理员权限检查
        self.log("\n[测试 13] 县市级管理员权限检查")
        self.login('admin_chaoyang')
        success, users = self.test_get_users()
        if success:
            # 县市级管理员应该只能看到本县市的用户
            for user in users:
                if user.get('region') and '朝阳' not in user.get('region', ''):
                    self.log(f"权限检查失败: 看到了非本县市用户 {user.get('username')}", 'ERROR')
                    self.failed += 1
                    break
            else:
                self.log("县市级管理员权限检查成功")
                self.passed += 1

        # 打印测试结果
        self.log("\n" + "=" * 60)
        self.log("测试结果汇总")
        self.log("=" * 60)
        self.log(f"✅ 通过: {self.passed}")
        self.log(f"❌ 失败: {self.failed}")
        self.log(f"📊 成功率: {self.passed / (self.passed + self.failed) * 100:.1f}%")
        self.log("=" * 60)

        return self.failed == 0

if __name__ == '__main__':
    runner = TestRunner()
    success = runner.run_tests()
    sys.exit(0 if success else 1)

