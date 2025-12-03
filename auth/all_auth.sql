-- =============================================
-- 一键创建企业/专家独立认证库与账号表（可直接在 mysql 客户端中执行）
-- MySQL 8.0 / InnoDB / utf8mb4
-- =============================================

-- ========== 企业认证库 ==========
CREATE DATABASE IF NOT EXISTS enterprise_auth
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE enterprise_auth;

CREATE TABLE IF NOT EXISTS enterprise_users (
  id            VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NOT NULL,
  username      VARCHAR(64) NOT NULL UNIQUE,
  email         VARCHAR(120) NULL UNIQUE,
  phone         VARCHAR(32)  NULL,
  password      VARCHAR(255) NOT NULL,
  level         ENUM('初级','中级','高级') NOT NULL DEFAULT '初级',
  role          ENUM('admin','operator') NOT NULL DEFAULT 'admin',
  status        ENUM('active','inactive','pending') NOT NULL DEFAULT 'active',
  last_login_at TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_enterprise (enterprise_id),
  INDEX idx_username (username),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO enterprise_users
  (id, enterprise_id, username, email, phone, password, level, role, status)
VALUES
  ('entu_demo_admin', 'enterprise_id_placeholder', 'ent_admin', 'ent_admin@example.com', NULL,
   '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH_________________________', '初级', 'admin', 'inactive');

-- ========== 专家认证库 ==========
CREATE DATABASE IF NOT EXISTS expert_auth
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE expert_auth;

CREATE TABLE IF NOT EXISTS expert_users (
  id            VARCHAR(36) PRIMARY KEY,
  expert_id     VARCHAR(36) NOT NULL,
  username      VARCHAR(64) NOT NULL UNIQUE,
  email         VARCHAR(120) NULL UNIQUE,
  phone         VARCHAR(32)  NULL,
  password      VARCHAR(255) NOT NULL,
  level         ENUM('县市级','省级','国家级') NOT NULL DEFAULT '县市级',
  role          ENUM('expert','lead') NOT NULL DEFAULT 'expert',
  status        ENUM('active','inactive','pending') NOT NULL DEFAULT 'active',
  last_login_at TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_expert (expert_id),
  INDEX idx_username (username),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO expert_users
  (id, expert_id, username, email, phone, password, level, role, status)
VALUES
  ('expu_demo', 'expert_id_placeholder', 'exp_user', 'exp_user@example.com', NULL,
   '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH_________________________', '县市级', 'expert', 'inactive');

-- 生成 bcrypt 指南（Python）：
-- import bcrypt; print(bcrypt.hashpw(b'YourPass123!', bcrypt.gensalt()).decode())

