-- 审计与登录日志
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS audit_logs (
  id VARCHAR(36) PRIMARY KEY,
  operator_id VARCHAR(36) NULL,         -- 操作人（chamber_users.id 或其它用户表）
  action VARCHAR(64) NOT NULL,          -- 如: create/update/delete/assign_permissions
  target_type VARCHAR(64) NOT NULL,     -- 如: role/menu/indicator/scoring_rule/...
  target_id VARCHAR(64) NULL,
  old_value JSON NULL,
  new_value JSON NULL,
  ip VARCHAR(64) NULL,
  ua VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_operator(operator_id),
  INDEX idx_action_time(action, created_at),
  INDEX idx_target(target_type, target_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS login_logs (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NULL,
  ip VARCHAR(64) NULL,
  ua VARCHAR(255) NULL,
  success TINYINT(1) DEFAULT 1,
  message VARCHAR(255) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_time(user_id, created_at),
  INDEX idx_success(success)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
