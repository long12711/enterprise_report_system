-- 报告与统一文件存储
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS file_storage (
  id VARCHAR(36) PRIMARY KEY,
  biz_type VARCHAR(50) NULL,         -- 业务类型：report/feedback_attachment/...
  biz_id VARCHAR(36) NULL,
  path VARCHAR(500) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  size BIGINT NULL,
  mime VARCHAR(120) NULL,
  hash_md5 CHAR(32) NULL,
  uploader_id VARCHAR(36) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_biz(biz_type, biz_id),
  INDEX idx_uploader(uploader_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reports (
  id VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NULL,
  filename VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,        -- 如 enterprise_assess/pdf
  file_size BIGINT NULL,
  path VARCHAR(500) NOT NULL,
  md5 CHAR(32) NULL,
  created_time INT NOT NULL,        -- Unix 时间戳，便于兼容现有前端
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_ent(enterprise_id),
  INDEX idx_created(created_time)
  -- 如需外键：CONSTRAINT fk_reports_ent FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

