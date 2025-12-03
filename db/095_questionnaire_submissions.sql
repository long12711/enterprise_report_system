-- 问卷提交管理表
SET NAMES utf8mb4;

-- 问卷提交记录表
CREATE TABLE IF NOT EXISTS questionnaire_submissions (
  id VARCHAR(36) PRIMARY KEY,
  enterprise_id VARCHAR(36) NOT NULL,
  survey_id VARCHAR(36) NOT NULL,
  survey_level ENUM('初级','中级','高级') NOT NULL,
  status ENUM('draft','submitted','reviewed') DEFAULT 'draft',
  total_score DECIMAL(8,2) NULL,
  submitted_at TIMESTAMP NULL,
  reviewed_at TIMESTAMP NULL,
  reviewer_id VARCHAR(36) NULL,
  reviewer_comments TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_enterprise(enterprise_id),
  INDEX idx_survey(survey_id),
  INDEX idx_status(status),
  INDEX idx_level(survey_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 问卷答案表
CREATE TABLE IF NOT EXISTS questionnaire_answers (
  id VARCHAR(36) PRIMARY KEY,
  submission_id VARCHAR(36) NOT NULL,
  question_id VARCHAR(36) NOT NULL,
  question_text VARCHAR(500) NOT NULL,
  answer_value TEXT NULL,
  answer_type ENUM('text','number','choice','file') DEFAULT 'text',
  score DECIMAL(8,2) NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_submission(submission_id),
  INDEX idx_question(question_id),
  CONSTRAINT fk_qa_submission FOREIGN KEY (submission_id) REFERENCES questionnaire_submissions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 问卷附件表（用于"补充数据/说明"列的文件上传）
CREATE TABLE IF NOT EXISTS questionnaire_attachments (
  id VARCHAR(36) PRIMARY KEY,
  submission_id VARCHAR(36) NOT NULL,
  question_id VARCHAR(36) NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  file_size INT NOT NULL,
  file_type VARCHAR(50),
  upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_submission(submission_id),
  INDEX idx_question(question_id),
  CONSTRAINT fk_attach_submission FOREIGN KEY (submission_id) REFERENCES questionnaire_submissions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 问卷模板表（存储导入的问卷题目）
CREATE TABLE IF NOT EXISTS questionnaire_templates (
  id VARCHAR(36) PRIMARY KEY,
  level ENUM('初级','中级','高级') NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  total_questions INT DEFAULT 0,
  status ENUM('active','inactive') DEFAULT 'active',
  source_file VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_level(level),
  INDEX idx_status(status),
  UNIQUE KEY unique_level(level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 问卷模板题目表
CREATE TABLE IF NOT EXISTS questionnaire_template_questions (
  id VARCHAR(36) PRIMARY KEY,
  template_id VARCHAR(36) NOT NULL,
  seq_no VARCHAR(50),
  level1 VARCHAR(100),
  level2 VARCHAR(100),
  question_text VARCHAR(500) NOT NULL,
  question_type VARCHAR(50),
  score DECIMAL(8,2),
  applicable VARCHAR(100),
  remarks TEXT,
  requires_file TINYINT(1) DEFAULT 0,
  sort_order INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_template(template_id),
  INDEX idx_sort(sort_order),
  CONSTRAINT fk_qtq_template FOREIGN KEY (template_id) REFERENCES questionnaire_templates(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 创建索引以提高查询性能
CREATE INDEX idx_submissions_enterprise_level ON questionnaire_submissions(enterprise_id, survey_level);
CREATE INDEX idx_submissions_status_time ON questionnaire_submissions(status, submitted_at);
CREATE INDEX idx_answers_submission_question ON questionnaire_answers(submission_id, question_id);
CREATE INDEX idx_attachments_submission_question ON questionnaire_attachments(submission_id, question_id);

