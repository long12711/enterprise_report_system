-- 平台配置（邮箱、短信）
SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS email_config (
  id TINYINT PRIMARY KEY,
  host VARCHAR(120) NOT NULL,
  port INT NOT NULL,
  username VARCHAR(120) NOT NULL,
  password_enc VARBINARY(512) NULL, -- 加密后密文；应用层负责加解密
  `from` VARCHAR(120) NULL,
  `ssl` TINYINT(1) DEFAULT 0,
  `tls` TINYINT(1) DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS sms_gateways (
  id TINYINT PRIMARY KEY,
  provider VARCHAR(60) NULL,     -- 阿里云/腾讯云/其他
  endpoint VARCHAR(255) NULL,
  `sign` VARCHAR(60) NOT NULL,
  `template` VARCHAR(100) NOT NULL,
  access_key VARCHAR(128) NOT NULL,
  secret_enc VARBINARY(512) NULL, -- 加密后密文
  status ENUM('active','inactive') DEFAULT 'inactive',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

