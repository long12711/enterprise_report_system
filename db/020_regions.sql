-- 地区字典（省/市县/全国）
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS regions (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  code VARCHAR(32) NOT NULL UNIQUE,
  level ENUM('national','province','county') NOT NULL,
  parent_code VARCHAR(32) NULL,
  status ENUM('active','inactive') DEFAULT 'active',
  sort INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_level(level),
  INDEX idx_parent_code(parent_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

