-- ============================================================
-- 工商联用户管理系统 - 数据库初始化脚本
-- ============================================================
-- 创建时间: 2024-11-30
-- 数据库: MySQL 5.7+
-- 字符集: utf8mb4
-- ============================================================

-- 1. 创建工商联用户表
CREATE TABLE IF NOT EXISTS `chamber_users` (
  `id` varchar(36) NOT NULL COMMENT '用户ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `email` varchar(100) NOT NULL COMMENT '邮箱',
  `password` varchar(255) NOT NULL COMMENT '密码(bcrypt加密)',
  `real_name` varchar(50) COMMENT '真实姓名',
  `phone` varchar(20) COMMENT '手机号',
  `level` enum('county','province','national') NOT NULL COMMENT '层级：县市级/省级/全联',
  `region` varchar(100) COMMENT '地区',
  `role` enum('admin','reviewer','operator') NOT NULL DEFAULT 'operator' COMMENT '角色：管理员/审核员/操作员',
  `review_level` enum('beginner','intermediate','advanced') COMMENT '审核权限等级：初级/中级/高级',
  `department` varchar(100) COMMENT '部门',
  `position` varchar(100) COMMENT '职位',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `status` enum('active','inactive','pending') NOT NULL DEFAULT 'pending' COMMENT '状态：激活/停用/待审核',
  `remark` text COMMENT '备注',
  `created_by` varchar(36) COMMENT '创建人ID',
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`),
  KEY `idx_level_region` (`level`, `region`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  KEY `idx_role` (`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联用户表';

-- 2. 创建操作日志表
CREATE TABLE IF NOT EXISTS `chamber_user_logs` (
  `id` varchar(36) NOT NULL COMMENT '日志ID',
  `operator_id` varchar(36) COMMENT '操作人ID',
  `target_user_id` varchar(36) COMMENT '目标用户ID',
  `action` varchar(50) NOT NULL COMMENT '操作类型：create/update/delete/status_change',
  `old_value` json COMMENT '旧值',
  `new_value` json COMMENT '新值',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  
  PRIMARY KEY (`id`),
  KEY `idx_operator_id` (`operator_id`),
  KEY `idx_target_user_id` (`target_user_id`),
  KEY `idx_action` (`action`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联用户操作日志表';

-- 3. 创建用户权限表（可选）
CREATE TABLE IF NOT EXISTS `chamber_user_permissions` (
  `id` varchar(36) NOT NULL COMMENT '权限ID',
  `user_id` varchar(36) NOT NULL COMMENT '用户ID',
  `permission_code` varchar(100) NOT NULL COMMENT '权限代码',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_permission` (`user_id`, `permission_code`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联用户权限表';

-- 4. 创建地区表（用于管理可用的地区）
CREATE TABLE IF NOT EXISTS `chamber_regions` (
  `id` varchar(36) NOT NULL COMMENT '地区ID',
  `name` varchar(100) NOT NULL COMMENT '地区名称',
  `level` enum('county','province','national') NOT NULL COMMENT '地区级别',
  `parent_id` varchar(36) COMMENT '父地区ID',
  `code` varchar(50) COMMENT '地区代码',
  `status` enum('active','inactive') DEFAULT 'active' COMMENT '状态',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name_level` (`name`, `level`),
  KEY `idx_level` (`level`),
  KEY `idx_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='工商联地区表';

-- ============================================================
-- 初始数据插入
-- ============================================================

-- 插入省份数据
INSERT IGNORE INTO `chamber_regions` (`id`, `name`, `level`, `code`, `status`) VALUES
('region_beijing', '北京市', 'province', 'BJ', 'active'),
('region_shanghai', '上海市', 'province', 'SH', 'active'),
('region_guangdong', '广东省', 'province', 'GD', 'active'),
('region_zhejiang', '浙江省', 'province', 'ZJ', 'active'),
('region_jiangsu', '江苏省', 'province', 'JS', 'active');

-- 插入北京市下的县市数据
INSERT IGNORE INTO `chamber_regions` (`id`, `name`, `level`, `parent_id`, `code`, `status`) VALUES
('region_beijing_chaoyang', '北京市朝阳区', 'county', 'region_beijing', 'BJ_CY', 'active'),
('region_beijing_dongcheng', '北京市东城区', 'county', 'region_beijing', 'BJ_DC', 'active'),
('region_beijing_xicheng', '北京市西城区', 'county', 'region_beijing', 'BJ_XC', 'active');

-- 插入上海市下的县市数据
INSERT IGNORE INTO `chamber_regions` (`id`, `name`, `level`, `parent_id`, `code`, `status`) VALUES
('region_shanghai_pudong', '上海市浦东新区', 'county', 'region_shanghai', 'SH_PD', 'active'),
('region_shanghai_huangpu', '上海市黄浦区', 'county', 'region_shanghai', 'SH_HP', 'active');

-- 插入全联数据
INSERT IGNORE INTO `chamber_regions` (`id`, `name`, `level`, `code`, `status`) VALUES
('region_national', '全国', 'national', 'CN', 'active');

-- ============================================================
-- 创建视图（可选）
-- ============================================================

-- 创建用户统计视图
CREATE OR REPLACE VIEW `v_chamber_user_stats` AS
SELECT 
  `level`,
  `region`,
  `role`,
  `status`,
  COUNT(*) as `count`
FROM `chamber_users`
GROUP BY `level`, `region`, `role`, `status`;

-- 创建用户详情视图
CREATE OR REPLACE VIEW `v_chamber_user_detail` AS
SELECT 
  u.`id`,
  u.`username`,
  u.`email`,
  u.`real_name`,
  u.`phone`,
  u.`level`,
  u.`region`,
  u.`role`,
  u.`review_level`,
  u.`department`,
  u.`position`,
  u.`status`,
  u.`created_at`,
  u.`updated_at`,
  u.`remark`,
  (SELECT `real_name` FROM `chamber_users` WHERE `id` = u.`created_by`) as `created_by_name`
FROM `chamber_users` u;

-- ============================================================
-- 创建存储过程（可选）
-- ============================================================

-- 创建获取用户列表的存储过程
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS `sp_get_chamber_users`(
  IN p_level VARCHAR(50),
  IN p_region VARCHAR(100),
  IN p_role VARCHAR(50),
  IN p_status VARCHAR(50),
  IN p_keyword VARCHAR(100),
  IN p_page INT,
  IN p_limit INT,
  OUT p_total INT
)
BEGIN
  DECLARE v_offset INT;
  SET v_offset = (p_page - 1) * p_limit;
  
  -- 获取总数
  SELECT COUNT(*) INTO p_total
  FROM `chamber_users`
  WHERE 
    (p_level IS NULL OR `level` = p_level) AND
    (p_region IS NULL OR `region` = p_region) AND
    (p_role IS NULL OR `role` = p_role) AND
    (p_status IS NULL OR `status` = p_status) AND
    (p_keyword IS NULL OR `username` LIKE CONCAT('%', p_keyword, '%') OR 
     `email` LIKE CONCAT('%', p_keyword, '%') OR 
     `real_name` LIKE CONCAT('%', p_keyword, '%'));
  
  -- 获取分页数据
  SELECT * FROM `chamber_users`
  WHERE 
    (p_level IS NULL OR `level` = p_level) AND
    (p_region IS NULL OR `region` = p_region) AND
    (p_role IS NULL OR `role` = p_role) AND
    (p_status IS NULL OR `status` = p_status) AND
    (p_keyword IS NULL OR `username` LIKE CONCAT('%', p_keyword, '%') OR 
     `email` LIKE CONCAT('%', p_keyword, '%') OR 
     `real_name` LIKE CONCAT('%', p_keyword, '%'))
  ORDER BY `created_at` DESC
  LIMIT v_offset, p_limit;
END //
DELIMITER ;

-- ============================================================
-- 创建索引优化
-- ============================================================

-- 创建复合索引用于常见查询
ALTER TABLE `chamber_users` ADD INDEX `idx_level_region_status` (`level`, `region`, `status`);
ALTER TABLE `chamber_users` ADD INDEX `idx_role_status` (`role`, `status`);
ALTER TABLE `chamber_user_logs` ADD INDEX `idx_operator_action` (`operator_id`, `action`);

-- ============================================================
-- 创建触发器（可选）
-- ============================================================

-- 创建触发器：自动更新updated_at
DELIMITER //
CREATE TRIGGER IF NOT EXISTS `trg_chamber_users_update` 
BEFORE UPDATE ON `chamber_users`
FOR EACH ROW
BEGIN
  SET NEW.`updated_at` = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- ============================================================
-- 权限和用户设置
-- ============================================================

-- 创建数据库用户（如果需要）
-- CREATE USER 'chamber_user'@'localhost' IDENTIFIED BY 'secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `chamber_db`.* TO 'chamber_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ============================================================
-- 数据备份和恢复说明
-- ============================================================

/*
备份命令:
mysqldump -u root -p chamber_db > chamber_backup.sql

恢复命令:
mysql -u root -p chamber_db < chamber_backup.sql

导出用户数据为CSV:
SELECT * FROM chamber_users 
INTO OUTFILE '/var/lib/mysql/chamber_users.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
*/

-- ============================================================
-- 脚本执行完成
-- ============================================================
-- 
-- 已创建的表:
-- 1. chamber_users - 工商联用户表
-- 2. chamber_user_logs - 操作日志表
-- 3. chamber_user_permissions - 用户权限表
-- 4. chamber_regions - 地区表
--
-- 已创建的视图:
-- 1. v_chamber_user_stats - 用户统计视图
-- 2. v_chamber_user_detail - 用户详情视图
--
-- 已创建的存储过程:
-- 1. sp_get_chamber_users - 获取用户列表
--
-- 已创建的触发器:
-- 1. trg_chamber_users_update - 自动更新时间戳
--
-- ============================================================

