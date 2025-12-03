-- =============================================
-- 专家用户独立认证库（expert_auth）
-- 目标：存储专家端登录账号，支持按账号级别与状态登录控制
-- MySQL 8.0 / InnoDB / utf8mb4
-- =============================================

CREATE DATABASE IF NOT EXISTS expert_auth
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE expert_auth;

-- 专家账号表（与业务库 enterprise_portal.experts 通过 expert_id 逻辑关联；不做跨库外键）
CREATE TABLE IF NOT EXISTS expert_users (
  id            VARCHAR(36) PRIMARY KEY,
  expert_id     VARCHAR(36) NOT NULL COMMENT '对应主库 experts.id，登录时校验存在性',
  username      VARCHAR(64) NOT NULL UNIQUE,
  email         VARCHAR(120) NULL UNIQUE,
  phone         VARCHAR(32)  NULL,
  password      VARCHAR(255) NOT NULL COMMENT 'bcrypt 哈希',
  level         ENUM('县市级','省级','国家级') NOT NULL DEFAULT '县市级' COMMENT '账号级别（与专家等级对应）',
  role          ENUM('expert','lead') NOT NULL DEFAULT 'expert' COMMENT '专家端角色：专家/组长',
  status        ENUM('active','inactive','pending') NOT NULL DEFAULT 'active',
  last_login_at TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_expert (expert_id),
  INDEX idx_username (username),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 示例种子（请替换 password 为你的 bcrypt 哈希；demo 默认禁用）
INSERT IGNORE INTO expert_users
  (id, expert_id, username, email, phone, password, level, role, status)
VALUES
  ('expu_demo', 'expert_id_placeholder', 'exp_user', 'exp_user@example.com', NULL,
   '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH_________________________', '县市级', 'expert', 'inactive');

-- 生成 bcrypt 指引（Python）：
-- import bcrypt; print(bcrypt.hashpw(b'YourPass123!', bcrypt.gensalt()).decode())

