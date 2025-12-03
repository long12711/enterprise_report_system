-- 初始化（可根据需要修改数据库名）
-- 建议执行顺序：000_init -> 010_rbac -> 020_regions -> 030_org -> 040_indicators_scoring -> 050_surveys -> 060_feedback -> 070_reports_files -> 080_platform_config -> 090_audit -> 100_seed

-- 可选：创建并使用数据库
-- CREATE DATABASE IF NOT EXISTS enterprise_portal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE enterprise_portal;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 1;
