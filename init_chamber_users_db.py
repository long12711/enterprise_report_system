#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工商联用户管理 - 数据库初始化脚本
用于创建表和插入测试数据
"""

import os
import sys
import logging
from sqlalchemy import create_engine, text

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'enterprise_portal'),
}

def get_connection_string():
    """获取数据库连接字符串"""
    return f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

def read_sql_file(filepath):
    """读取 SQL 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"读取 SQL 文件失败: {filepath}, {e}")
        return None

def execute_sql(engine, sql):
    """执行 SQL 语句"""
    try:
        with engine.connect() as conn:
            # 分割 SQL 语句
            statements = sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    logger.info(f"执行: {statement[:100]}...")
                    conn.execute(text(statement))
            conn.commit()
        return True
    except Exception as e:
        logger.error(f"执行 SQL 失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    logger.info("开始初始化数据库...")
    logger.info(f"数据库配置: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    try:
        # 创建连接
        engine = create_engine(get_connection_string(), echo=False)
        
        # 测试连接
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("数据库连接成功")
        
        # 创建表
        logger.info("创建表...")
        sql_files = [
            'db/015_chamber_users.sql',
        ]
        
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                logger.info(f"执行 {sql_file}...")
                sql = read_sql_file(sql_file)
                if sql:
                    execute_sql(engine, sql)
                    logger.info(f"{sql_file} 执行成功")
            else:
                logger.warning(f"{sql_file} 不存在")
        
        # 插入测试数据
        logger.info("插入测试数据...")
        seed_file = 'db/101_chamber_users_seed.sql'
        if os.path.exists(seed_file):
            logger.info(f"执行 {seed_file}...")
            sql = read_sql_file(seed_file)
            if sql:
                execute_sql(engine, sql)
                logger.info(f"{seed_file} 执行成功")
        else:
            logger.warning(f"{seed_file} 不存在")
        
        logger.info("数据库初始化完成!")
        return True
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)

