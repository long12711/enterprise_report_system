-- 指标体系与评分规则
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS evaluation_indicators (
  id VARCHAR(36) PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  level TINYINT NOT NULL, -- 1/2/3
  parent_id VARCHAR(36) NULL,
  `type` ENUM('基础类','拔高类','创新类','责任类','其他类') NULL,
  weight DECIMAL(5,2) NULL,
  sort_order INT DEFAULT 0,
  status ENUM('active','inactive') DEFAULT 'active',
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_parent(parent_id),
  INDEX idx_level(level),
  INDEX idx_type(`type`),
  CONSTRAINT fk_indicator_parent FOREIGN KEY (parent_id) REFERENCES evaluation_indicators(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS scoring_rules (
  id VARCHAR(36) PRIMARY KEY,
  indicator_id VARCHAR(36) NOT NULL,
  level ENUM('初级','中级','高级') NOT NULL,
  score_min INT DEFAULT 0,
  score_max INT DEFAULT 100,
  criteria JSON NULL,  -- 评分标准数组
  remark TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_indicator_level(indicator_id, level),
  INDEX idx_indicator(indicator_id),
  CONSTRAINT fk_rule_indicator FOREIGN KEY (indicator_id) REFERENCES evaluation_indicators(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
