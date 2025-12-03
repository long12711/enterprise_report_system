-- 一键执行脚本（仅 mysql 客户端支持 SOURCE 命令）
-- 使用前：先在 MySQL 中创建并切换到目标数据库，例如：
--   CREATE DATABASE IF NOT EXISTS enterprise_portal DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--   USE enterprise_portal;

SOURCE 000_init.sql;
SOURCE 010_rbac.sql;
SOURCE 015_chamber_users.sql;
SOURCE 020_regions.sql;
SOURCE 030_org.sql;
SOURCE 040_indicators_scoring.sql;
SOURCE 050_surveys.sql;
SOURCE 060_feedback.sql;
SOURCE 070_reports_files.sql;
SOURCE 080_platform_config.sql;
SOURCE 090_audit.sql;
SOURCE 100_seed.sql;
SOURCE 101_chamber_users_seed.sql;

