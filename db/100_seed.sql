-- 基础种子数据（可按需调整）
SET NAMES utf8mb4;

-- 1) 角色
INSERT IGNORE INTO roles (id, name, `key`, description, status)
VALUES
  ('role_admin', '系统管理员', 'admin', '拥有全部功能', 'active'),
  ('role_reviewer', '审核员', 'reviewer', '审核相关功能', 'active'),
  ('role_operator', '操作员', 'operator', '日常操作', 'active');

-- 2) 菜单（示例，按前端模块分目录/菜单）
-- 顶层目录
INSERT IGNORE INTO menus (id, name, `key`, `type`, `sort`, status)
VALUES
  ('menu_dir_enterprise', '企业管理', 'enterprise', 'directory', 10, 'active'),
  ('menu_dir_expert', '专家管理', 'expert', 'directory', 20, 'active'),
  ('menu_dir_chamber', '工商联用户', 'chamber', 'directory', 30, 'active'),
  ('menu_dir_special', '专项反馈', 'special', 'directory', 40, 'active'),
  ('menu_dir_questionnaire', '基础问卷', 'questionnaire', 'directory', 50, 'active'),
  ('menu_dir_platform', '平台配置', 'platform', 'directory', 60, 'active');

-- 二级菜单（示例）
INSERT IGNORE INTO menus (id, name, `key`, parent_key, `type`, `sort`, status)
VALUES
  ('menu_ent_info', '企业信息', 'enterprise-info', 'enterprise', 'menu', 1, 'active'),
  ('menu_ent_upgrade', '评价升级', 'upgrade-center', 'enterprise', 'menu', 2, 'active'),
  ('menu_exp_info', '专家信息', 'experts-info', 'expert', 'menu', 1, 'active'),
  ('menu_exp_rate', '专家评级', 'expert-rate', 'expert', 'menu', 2, 'active'),
  ('menu_ch_user', '用户管理', 'chamber-users', 'chamber', 'menu', 1, 'active'),
  ('menu_sp_list', '反馈列表', 'special-list', 'special', 'menu', 1, 'active'),
  ('menu_sp_analysis', '深度分析', 'special-analysis', 'special', 'menu', 2, 'active'),
  ('menu_indicators', '指标体系', 'indicators', 'questionnaire', 'menu', 1, 'active'),
  ('menu_rules', '评分规则', 'scoring-rules', 'questionnaire', 'menu', 2, 'active'),
  ('menu_ent_surveys', '企业问卷', 'enterprise-surveys', 'questionnaire', 'menu', 3, 'active'),
  ('menu_exp_surveys', '专家问卷', 'expert-surveys', 'questionnaire', 'menu', 4, 'active'),
  ('menu_platform_roles', '角色管理', 'roles', 'platform', 'menu', 1, 'active'),
  ('menu_platform_menus', '菜单管理', 'menus', 'platform', 'menu', 2, 'active'),
  ('menu_platform_perms', '权限管理', 'permissions', 'platform', 'menu', 3, 'active'),
  ('menu_platform_email', '邮箱配置', 'email-config', 'platform', 'menu', 4, 'active'),
  ('menu_platform_sms', '短信网关', 'sms-gateway', 'platform', 'menu', 5, 'active');

-- 3) 管理员角色默认绑定全部菜单
INSERT IGNORE INTO role_menus (id, role_id, menu_id)
SELECT UUID(), 'role_admin', m.id FROM menus m;

-- 4) 地区（示例）
INSERT IGNORE INTO regions (id, name, code, level, parent_code, status, sort)
VALUES
  ('region_cn', '全国', 'CN', 'national', NULL, 'active', 0),
  ('region_beijing', '北京市', 'BJ', 'province', 'CN', 'active', 10),
  ('region_beijing_cy', '北京市朝阳区', 'BJ_CY', 'county', 'BJ', 'active', 1),
  ('region_shanghai', '上海市', 'SH', 'province', 'CN', 'active', 20),
  ('region_shanghai_pd', '上海市浦东新区', 'SH_PD', 'county', 'SH', 'active', 1);

-- 5) 平台配置占位（id 固定 1）
INSERT IGNORE INTO email_config (id, host, port, username, password_enc, `from`, `ssl`, `tls`)
VALUES (1, 'smtp.example.com', 465, 'no-reply@example.com', NULL, '平台通知', 1, 0);

INSERT IGNORE INTO sms_gateways (id, provider, endpoint, sign, template, access_key, secret_enc, status)
VALUES (1, 'aliyun', NULL, '【平台】', 'SMS_000000', 'AKID_PLACEHOLDER', NULL, 'inactive');

