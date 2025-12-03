-- 组织与主体：工商联画像 / 企业 / 专家 / 辅导
SET NAMES utf8mb4;

-- 工商联用户画像（扩展 chamber_users）
CREATE TABLE IF NOT EXISTS chamber_profiles (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  level ENUM('county','province','national') NOT NULL,
  region_code VARCHAR(32),
  review_level ENUM('beginner','intermediate','advanced') NULL,
  remark TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_user(user_id),
  INDEX idx_level_region(level, region_code),
  CONSTRAINT fk_cp_user FOREIGN KEY (user_id) REFERENCES chamber_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 企业
CREATE TABLE IF NOT EXISTS enterprises (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  region_code VARCHAR(32),
  industry_code VARCHAR(64),
  contact VARCHAR(64),
  email VARCHAR(120),
  phone VARCHAR(32),
  level ENUM('beginner','intermediate','advanced') NULL,
  status ENUM('active','inactive') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_name(name),
  INDEX idx_region(region_code),
  INDEX idx_level(level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 专家
CREATE TABLE IF NOT EXISTS experts (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  region_code VARCHAR(32),
  province VARCHAR(64),
  industry VARCHAR(64),
  level ENUM('county','province','national') NULL,
  phone VARCHAR(32),
  email VARCHAR(120),
  org VARCHAR(200),
  skills TEXT,
  status ENUM('active','inactive') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_region(region_code),
  INDEX idx_level(level),
  INDEX idx_name(name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 专家辅导台账
CREATE TABLE IF NOT EXISTS tutoring_ledger (
  id VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NOT NULL,
  expert_id VARCHAR(36) NOT NULL,
  time DATETIME NOT NULL,
  note TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_ent_time(enterprise_id, time),
  INDEX idx_exp_time(expert_id, time),
  CONSTRAINT fk_tl_ent FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE,
  CONSTRAINT fk_tl_exp FOREIGN KEY (expert_id) REFERENCES experts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 专家与企业的辅导消息记录（如需）
CREATE TABLE IF NOT EXISTS tutoring_records (
  id VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NOT NULL,
  expert_id VARCHAR(36) NOT NULL,
  content TEXT NOT NULL,
  time DATETIME NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_ent_time(enterprise_id, time),
  INDEX idx_exp_time(expert_id, time),
  CONSTRAINT fk_tr_ent FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE,
  CONSTRAINT fk_tr_exp FOREIGN KEY (expert_id) REFERENCES experts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

