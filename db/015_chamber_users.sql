-- 工商联用户管理表
-- MySQL 8.0, InnoDB, utf8mb4

SET NAMES utf8mb4;

-- 工商联用户表
CREATE TABLE IF NOT EXISTS chamber_users (
  id VARCHAR(36) PRIMARY KEY COMMENT '用户ID',
  username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
  email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
  password VARCHAR(255) NOT NULL COMMENT '密码(bcrypt加密)',
  real_name VARCHAR(50) COMMENT '真实姓名',
  phone VARCHAR(20) COMMENT '手机号',
  level ENUM('county', 'province', 'national') NOT NULL COMMENT '层级：县市/省级/全联',
  region VARCHAR(100) COMMENT '地区',
  role ENUM('admin', 'reviewer', 'operator') DEFAULT 'operator' COMMENT '角色',
  review_level ENUM('beginner', 'intermediate', 'advanced') COMMENT '审核权限等级',
  department VARCHAR(100) COMMENT '部门',
  position VARCHAR(100) COMMENT '职位',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  status ENUM('active', 'inactive', 'pending') DEFAULT 'pending' COMMENT '状态',
  remark TEXT COMMENT '备注',
  created_by VARCHAR(36) COMMENT '创建人ID',
  
  INDEX idx_level_region (level, region),
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联用户表';

-- 工商联用户操作日志表
CREATE TABLE IF NOT EXISTS chamber_user_logs (
  id VARCHAR(36) PRIMARY KEY COMMENT '日志ID',
  operator_id VARCHAR(36) COMMENT '操作人ID',
  target_user_id VARCHAR(36) COMMENT '目标用户ID',
  action VARCHAR(50) COMMENT '操作类型: create/update/delete/status_change',
  old_value JSON COMMENT '旧值',
  new_value JSON COMMENT '新值',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  
  INDEX idx_operator_id (operator_id),
  INDEX idx_target_user_id (target_user_id),
  INDEX idx_created_at (created_at),
  CONSTRAINT fk_cul_operator FOREIGN KEY (operator_id) REFERENCES chamber_users(id) ON DELETE SET NULL,
  CONSTRAINT fk_cul_target FOREIGN KEY (target_user_id) REFERENCES chamber_users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联用户操作日志表';

