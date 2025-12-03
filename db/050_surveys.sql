-- 问卷（企业/专家）与作答结构
SET NAMES utf8mb4;

-- 企业问卷元数据
CREATE TABLE IF NOT EXISTS enterprise_surveys (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  level ENUM('初级','中级','高级') NOT NULL,
  description TEXT,
  status ENUM('active','inactive') DEFAULT 'active',
  usage_scope JSON NULL,          -- 使用范围（可与 level 不同的复用范围）
  total_questions INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_level(level),
  INDEX idx_status(status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 企业问卷题目
CREATE TABLE IF NOT EXISTS survey_questions (
  id VARCHAR(36) PRIMARY KEY,
  survey_id VARCHAR(36) NOT NULL,
  indicator_id VARCHAR(36) NULL,
  question_text VARCHAR(500) NOT NULL,
  question_type ENUM('single_choice','multiple_choice','text','number','rating') NOT NULL,
  options JSON NULL,              -- 选项与评分映射可存于 JSON
  required TINYINT(1) DEFAULT 1,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_survey_id(survey_id),
  INDEX idx_indicator_id(indicator_id),
  CONSTRAINT fk_sq_survey FOREIGN KEY (survey_id) REFERENCES enterprise_surveys(id) ON DELETE CASCADE,
  CONSTRAINT fk_sq_indicator FOREIGN KEY (indicator_id) REFERENCES evaluation_indicators(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 专家问卷元数据
CREATE TABLE IF NOT EXISTS expert_surveys (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  expert_type VARCHAR(50) NOT NULL, -- 如：技术专家/管理专家
  description TEXT,
  status ENUM('active','inactive') DEFAULT 'active',
  usage_scope JSON NULL,
  total_questions INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_type(expert_type),
  INDEX idx_status(status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 专家问卷题目
CREATE TABLE IF NOT EXISTS expert_survey_questions (
  id VARCHAR(36) PRIMARY KEY,
  survey_id VARCHAR(36) NOT NULL,
  indicator_id VARCHAR(36) NULL,
  question_text VARCHAR(500) NOT NULL,
  question_type ENUM('rating','single_choice','multiple_choice','text','number') NOT NULL,
  rating_scale INT NULL,          -- 评分量表（如 5/10）
  options JSON NULL,
  required TINYINT(1) DEFAULT 1,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_survey_id(survey_id),
  INDEX idx_indicator_id(indicator_id),
  CONSTRAINT fk_xq_survey FOREIGN KEY (survey_id) REFERENCES expert_surveys(id) ON DELETE CASCADE,
  CONSTRAINT fk_xq_indicator FOREIGN KEY (indicator_id) REFERENCES evaluation_indicators(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 填写实例（企业或专家）
CREATE TABLE IF NOT EXISTS survey_instances (
  id VARCHAR(36) PRIMARY KEY,
  survey_type ENUM('enterprise','expert') NOT NULL,
  survey_id VARCHAR(36) NOT NULL,
  subject_type ENUM('enterprise','expert') NOT NULL,
  subject_id VARCHAR(36) NOT NULL, -- 无条件外键，配合 subject_type 使用
  status ENUM('draft','submitted','scored') DEFAULT 'draft',
  total_score DECIMAL(8,2) NULL,
  submitted_at TIMESTAMP NULL,
  scored_at TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_survey(survey_type, survey_id),
  INDEX idx_subject(subject_type, subject_id),
  INDEX idx_status_time(status, submitted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 答案明细
CREATE TABLE IF NOT EXISTS survey_answers (
  id VARCHAR(36) PRIMARY KEY,
  instance_id VARCHAR(36) NOT NULL,
  question_id VARCHAR(36) NOT NULL,
  value_text TEXT NULL,
  value_number DECIMAL(18,4) NULL,
  value_json JSON NULL,
  score DECIMAL(8,2) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_instance(instance_id),
  INDEX idx_question(question_id),
  CONSTRAINT fk_ans_instance FOREIGN KEY (instance_id) REFERENCES survey_instances(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

