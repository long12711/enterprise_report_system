-- =============================================
-- 企业用户独立认证库（enterprise_auth）
-- 目标：存储企业端登录账号，支持按账号级别（初/中/高）与状态登录控制
-- MySQL 8.0 / InnoDB / utf8mb4
-- =============================================

-- 如需修改库名，可整体替换 enterprise_auth
CREATE DATABASE IF NOT EXISTS enterprise_auth
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE enterprise_auth;

-- 企业账号表（与业务库 enterprise_portal.enterprises 通过 enterprise_id 逻辑关联；不做跨库外键）
CREATE TABLE IF NOT EXISTS enterprise_users (
  id            VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NOT NULL COMMENT '对应主库 enterprises.id，登录时校验存在性',
  username      VARCHAR(64) NOT NULL UNIQUE,
  email         VARCHAR(120) NULL UNIQUE,
  phone         VARCHAR(32)  NULL,
  password      VARCHAR(255) NOT NULL COMMENT 'bcrypt 哈希',
  level         ENUM('初级','中级','高级') NOT NULL DEFAULT '初级' COMMENT '账号级别(用于权限范围/问卷适配)',
  role          ENUM('admin','operator') NOT NULL DEFAULT 'admin' COMMENT '企业端角色（轻量）',
  status        ENUM('active','inactive','pending') NOT NULL DEFAULT 'active',
  last_login_at TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_enterprise (enterprise_id),
  INDEX idx_username (username),
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 可选：企业端角色表（如需更细粒度再启用；当前用轻量 role 字段即可）
-- CREATE TABLE IF NOT EXISTS ent_roles (
--   id VARCHAR(36) PRIMARY KEY,
--   name VARCHAR(64) NOT NULL,
--   `key` VARCHAR(64) NOT NULL UNIQUE,
--   status ENUM('active','inactive') DEFAULT 'active',
--   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- CREATE TABLE IF NOT EXISTS ent_user_roles (
--   id VARCHAR(36) PRIMARY KEY,
--   user_id VARCHAR(36) NOT NULL,
--   role_id VARCHAR(36) NOT NULL,
--   UNIQUE KEY uk_user_role(user_id, role_id),
--   INDEX idx_user(user_id),
--   INDEX idx_role(role_id)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 示例种子（请将 password 替换为你生成的 bcrypt 哈希；demo 为禁用状态，防止误用）
INSERT IGNORE INTO enterprise_users
  (id, enterprise_id, username, email, phone, password, level, role, status)
VALUES
  ('entu_demo_admin', 'enterprise_id_placeholder', 'ent_admin', 'ent_admin@example.com', NULL,
   '$2b$12$REPLACE_WITH_YOUR_BCRYPT_HASH_________________________', '初级', 'admin', 'inactive');

-- 生成 bcrypt 指引（Python）：
-- import bcrypt; print(bcrypt.hashpw(b'YourPass123!', bcrypt.gensalt()).decode())

