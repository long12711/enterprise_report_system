# -*- coding: utf-8 -*-
"""
创建 MySQL 数据库并初始化问卷相关表
使用内置的 SQL 脚本 db/095_questionnaire_submissions.sql
"""
import os
import sys
import mysql.connector
from mysql.connector import Error

HOST = os.environ.get('DB_HOST', 'localhost')
USER = os.environ.get('DB_USER', 'root')
PASSWORD = os.environ.get('DB_PASSWORD', '123456')
DB_NAME = os.environ.get('DB_NAME', 'localhost_3306')

SQL_FILE = os.path.join(os.path.dirname(__file__), 'db', '095_questionnaire_submissions.sql')


def run_sql_file(conn, sql_path):
    with open(sql_path, 'r', encoding='utf-8') as f:
        sql_text = f.read()
    # 简单分割执行（适用于当前脚本）
    statements = [s.strip() for s in sql_text.split(';') if s.strip()]
    cur = conn.cursor()
    for stmt in statements:
        try:
            cur.execute(stmt)
        except Exception as e:
            # 某些 CREATE INDEX 若重复会报错，忽略
            print(f"[WARN] 执行失败（忽略）：{e}\nSQL: {stmt[:120]}...")
    conn.commit()
    cur.close()


def main():
    print(f"连接到 MySQL: {HOST} ...")
    conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    conn.commit()
    cur.close()
    conn.close()
    print(f"数据库已准备: {DB_NAME}")

    print("初始化表结构...")
    conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DB_NAME)
    run_sql_file(conn, SQL_FILE)
    conn.close()
    print("表结构初始化完成。")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

