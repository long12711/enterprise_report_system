# -*- coding: utf-8 -*-
"""
JSON → MySQL 迁移脚本
将 storage/questionnaires.json 中的问卷模板与题目迁移到 MySQL 的
questionnaire_templates 和 questionnaire_template_questions 表，便于 Navicat 查看与维护。

使用方法：
  # 先设置数据库环境变量
  # Windows PowerShell 示例：
  #   $env:DB_HOST="127.0.0.1"; $env:DB_USER="root"; $env:DB_PASSWORD="***"; $env:DB_NAME="enterprise_system"
  # 运行迁移：
  #   python migrate_questionnaires_to_mysql.py [可选JSON路径]
"""
import os
import sys
import json
import uuid
from datetime import datetime
import mysql.connector
from mysql.connector import Error

DEFAULT_JSON_PATHS = [
    os.path.join('storage', 'questionnaires.json'),
    os.path.join(os.path.expanduser('~'), 'storage', 'questionnaires.json')
]

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', '123456'),
    'database': os.environ.get('DB_NAME', 'localhost_3306')
}


def get_db_conn():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"[ERROR] 数据库连接失败: {e}")
        return None


def load_json(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] 读取 JSON 失败: {path} - {e}")
        return None


def ensure_tables(conn):
    """确保需要的表存在（与 db/095_questionnaire_submissions.sql 保持一致的核心部分）并做必要的结构升级"""
    ddl = [
        """
        CREATE TABLE IF NOT EXISTS questionnaire_templates (
          id VARCHAR(36) PRIMARY KEY,
          level ENUM('初级','中级','高级') NOT NULL,
          name VARCHAR(100) NOT NULL,
          description TEXT,
          total_questions INT DEFAULT 0,
          status ENUM('active','inactive') DEFAULT 'active',
          source_file VARCHAR(255),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
          INDEX idx_level(level),
          INDEX idx_status(status),
          UNIQUE KEY unique_level(level)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        """
        CREATE TABLE IF NOT EXISTS questionnaire_template_questions (
          id VARCHAR(36) PRIMARY KEY,
          template_id VARCHAR(36) NOT NULL,
          seq_no VARCHAR(50),
          level1 VARCHAR(100),
          level2 VARCHAR(100),
          question_text VARCHAR(1000) NOT NULL,
          question_type VARCHAR(255),
          score DECIMAL(8,2),
          applicable VARCHAR(500),
          remarks LONGTEXT,
          requires_file TINYINT(1) DEFAULT 0,
          sort_order INT DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          INDEX idx_template(template_id),
          INDEX idx_sort(sort_order)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    ]
    cur = conn.cursor()
    for sql in ddl:
        cur.execute(sql)
    # 尝试升级已有表字段，避免长度不足
    for alter in [
        "ALTER TABLE questionnaire_template_questions MODIFY question_type VARCHAR(255) NULL",
        "ALTER TABLE questionnaire_template_questions MODIFY question_text VARCHAR(1000) NOT NULL",
        "ALTER TABLE questionnaire_template_questions MODIFY applicable VARCHAR(500) NULL",
        "ALTER TABLE questionnaire_template_questions MODIFY remarks LONGTEXT NULL"
    ]:
        try:
            cur.execute(alter)
        except Exception:
            pass
    conn.commit()
    cur.close()


def upsert_template(conn, level: str, name: str, description: str, total_questions: int, source_file: str):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id FROM questionnaire_templates WHERE level=%s", (level,))
    row = cur.fetchone()
    if row:
        template_id = row['id']
        cur.execute(
            "UPDATE questionnaire_templates SET name=%s, description=%s, total_questions=%s, source_file=%s, updated_at=NOW() WHERE id=%s",
            (name, description, total_questions, source_file, template_id)
        )
    else:
        template_id = str(uuid.uuid4())
        cur.execute(
            "INSERT INTO questionnaire_templates (id, level, name, description, total_questions, status, source_file) VALUES (%s,%s,%s,%s,%s,'active',%s)",
            (template_id, level, name, description, total_questions, source_file)
        )
    conn.commit()
    cur.close()
    return template_id


def replace_questions(conn, template_id: str, questions: list):
    cur = conn.cursor()
    cur.execute("DELETE FROM questionnaire_template_questions WHERE template_id=%s", (template_id,))
    insert_sql = (
        "INSERT INTO questionnaire_template_questions "
        "(id, template_id, seq_no, level1, level2, question_text, question_type, score, applicable, remarks, requires_file, sort_order) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    data = []
    for idx, q in enumerate(questions, start=1):
        score_val = None
        try:
            score_val = float(q.get('score')) if q.get('score') not in (None, '') else None
        except Exception:
            score_val = None
        data.append((
            str(uuid.uuid4()),
            template_id,
            q.get('seq_no'),
            q.get('level1'),
            q.get('level2'),
            q.get('question_text'),
            q.get('question_type'),
            score_val,
            q.get('applicable'),
            q.get('remarks'),
            1 if q.get('requires_file') else 0,
            idx
        ))
    if data:
        cur.executemany(insert_sql, data)
    conn.commit()
    cur.close()


def main():
    # 解析 JSON 路径
    json_path = None
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
        if not os.path.isfile(json_path):
            print(f"[ERROR] 指定的 JSON 文件不存在: {json_path}")
            return 1
    else:
        for p in DEFAULT_JSON_PATHS:
            if os.path.isfile(p):
                json_path = p
                break
    if not json_path:
        print("[ERROR] 未找到 questionnaires.json，请指定文件路径。")
        return 1

    db = load_json(json_path)
    if not db:
        print("[ERROR] 读取 JSON 失败。")
        return 1

    conn = get_db_conn()
    if not conn:
        return 1

    ensure_tables(conn)

    surveys = db.get('surveys', [])
    questions_all = db.get('questions', [])

    print(f"发现 {len(surveys)} 个问卷，开始迁移...")

    for s in surveys:
        level = s.get('level')
        name = s.get('name')
        desc = s.get('description')
        total_questions = s.get('total_questions', 0)
        source_file = s.get('source_file')
        template_id = upsert_template(conn, level, name, desc, total_questions, source_file)

        qs = [q for q in questions_all if q.get('survey_id') == s.get('id')]
        replace_questions(conn, template_id, qs)
        print(f"  - {level} {name}: 已写入 {len(qs)} 个题目 (template_id={template_id})")

    conn.close()
    print("迁移完成，可在 Navicat 查看 questionnaire_templates / questionnaire_template_questions 表。")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

