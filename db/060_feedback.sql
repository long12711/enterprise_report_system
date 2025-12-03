-- 专项反馈与附件/标签/关联/统计
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS special_feedbacks (
  id VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NULL,
  enterprise_name VARCHAR(100) NULL,
  category ENUM('typical_case','issue_feedback','chamber_feedback','expert_feedback','material') NOT NULL,
  subcategory VARCHAR(50) NULL,
  title VARCHAR(200) NOT NULL,
  content MEDIUMTEXT NULL,
  status ENUM('draft','submitted','reviewing','approved','rejected') DEFAULT 'draft',
  rating INT NULL,
  priority ENUM('low','medium','high','urgent') DEFAULT 'medium',
  submitted_at TIMESTAMP NULL,
  reviewed_at TIMESTAMP NULL,
  reviewer_id VARCHAR(36) NULL,
  review_comment TEXT NULL,
  tags JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_cat_stat_time(category, status, submitted_at),
  INDEX idx_ent(enterprise_id)
  -- 外键：enterprise_id -> enterprises.id（如存在企业表）可在确认后添加
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS feedback_attachments (
  id VARCHAR(36) PRIMARY KEY,
  feedback_id VARCHAR(36) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  path VARCHAR(500) NOT NULL,
  mime VARCHAR(120) NULL,
  size BIGINT NULL,
  uploader_id VARCHAR(36) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_fb(feedback_id),
  CONSTRAINT fk_fa_fb FOREIGN KEY (feedback_id) REFERENCES special_feedbacks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS feedback_tags (
  id VARCHAR(36) PRIMARY KEY,
  tag_name VARCHAR(50) NOT NULL UNIQUE,
  tag_category VARCHAR(50) NULL,
  usage_count INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 反馈-标签 映射（避免在主表 large JSON 过大）
CREATE TABLE IF NOT EXISTS feedback_tag_map (
  id VARCHAR(36) PRIMARY KEY,
  feedback_id VARCHAR(36) NOT NULL,
  tag_id VARCHAR(36) NOT NULL,
  UNIQUE KEY uk_fb_tag(feedback_id, tag_id),
  INDEX idx_fb(feedback_id),
  INDEX idx_tag(tag_id),
  CONSTRAINT fk_ftm_fb FOREIGN KEY (feedback_id) REFERENCES special_feedbacks(id) ON DELETE CASCADE,
  CONSTRAINT fk_ftm_tag FOREIGN KEY (tag_id) REFERENCES feedback_tags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 反馈关联关系
CREATE TABLE IF NOT EXISTS feedback_relations (
  id VARCHAR(36) PRIMARY KEY,
  source_feedback_id VARCHAR(36) NOT NULL,
  related_feedback_id VARCHAR(36) NOT NULL,
  relation_type VARCHAR(50) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_source(source_feedback_id),
  INDEX idx_related(related_feedback_id),
  CONSTRAINT fk_fr_src FOREIGN KEY (source_feedback_id) REFERENCES special_feedbacks(id) ON DELETE CASCADE,
  CONSTRAINT fk_fr_rel FOREIGN KEY (related_feedback_id) REFERENCES special_feedbacks(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 可选：统计/分析快照（用于离线报表）
CREATE TABLE IF NOT EXISTS feedback_statistics (
  id VARCHAR(36) PRIMARY KEY,
  stat_date DATE NOT NULL,
  stat_type VARCHAR(50) NOT NULL,
  total_count INT DEFAULT 0,
  category_breakdown JSON NULL,
  status_breakdown JSON NULL,
  rating_distribution JSON NULL,
  trend_data JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_stat(stat_date, stat_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

