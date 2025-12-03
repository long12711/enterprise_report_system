-- RBAC 基础表（依赖：chamber_users 已存在）
-- MySQL 8.0, InnoDB, utf8mb4

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  `key` VARCHAR(64) NOT NULL UNIQUE,
  description VARCHAR(255),
  status ENUM('active','inactive') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS menus (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  `key` VARCHAR(64) NOT NULL UNIQUE,
  path VARCHAR(255),
  parent_key VARCHAR(64),
  `type` ENUM('directory','menu','button') DEFAULT 'menu',
  `sort` INT DEFAULT 0,
  status ENUM('active','inactive') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_parent_key(parent_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS role_menus (
  id VARCHAR(36) PRIMARY KEY,
  role_id VARCHAR(36) NOT NULL,
  menu_id VARCHAR(36) NOT NULL,
  UNIQUE KEY uk_role_menu(role_id, menu_id),
  INDEX idx_role_id(role_id),
  INDEX idx_menu_id(menu_id),
  CONSTRAINT fk_rm_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  CONSTRAINT fk_rm_menu FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户-角色映射（用户来自 chamber_users）
CREATE TABLE IF NOT EXISTS user_roles (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  role_id VARCHAR(36) NOT NULL,
  UNIQUE KEY uk_user_role(user_id, role_id),
  INDEX idx_user_id(user_id),
  INDEX idx_role_id(role_id),
  CONSTRAINT fk_ur_role FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  CONSTRAINT fk_ur_user FOREIGN KEY (user_id) REFERENCES chamber_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

