-- 工商联用户管理 - 测试数据
SET NAMES utf8mb4;

-- 插入测试用户数据
-- 密码都是 123456 (bcrypt 加密)
-- 使用 Python 生成: bcrypt.hashpw(b'123456', bcrypt.gensalt()).decode('utf-8')
-- 结果: $2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6

INSERT INTO chamber_users (
  id, username, email, password, real_name, phone, level, region, role, 
  review_level, department, position, status, remark, created_by
) VALUES
-- 全联管理员
('user-001', 'admin_national', 'admin@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6', 
 '全联管理员', '010-12345678', 'national', '全国', 'admin', 'advanced', 
 '办公室', '主任', 'active', '全联系统管理员', NULL),

-- 省级管理员（北京）
('user-002', 'admin_beijing', 'admin.beijing@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '北京省级管理员', '010-87654321', 'province', '北京', 'admin', 'advanced',
 '北京办公室', '主任', 'active', '北京省级管理员', 'user-001'),

-- 省级审核员（北京）
('user-003', 'reviewer_beijing', 'reviewer.beijing@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '北京审核员', '010-11111111', 'province', '北京', 'reviewer', 'advanced',
 '北京办公室', '审核员', 'active', '北京省级审核员', 'user-002'),

-- 县市级管理员（北京朝阳）
('user-004', 'admin_chaoyang', 'admin.chaoyang@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '朝阳区管理员', '010-22222222', 'county', '北京朝阳', 'admin', 'intermediate',
 '朝阳办公室', '主任', 'active', '朝阳区管理员', 'user-002'),

-- 县市级操作员（北京朝阳）
('user-005', 'operator_chaoyang_1', 'operator1.chaoyang@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '朝阳操作员1', '010-33333333', 'county', '北京朝阳', 'operator', 'beginner',
 '朝阳办公室', '操作员', 'active', '朝阳区操作员', 'user-004'),

-- 县市级操作员（北京朝阳）
('user-006', 'operator_chaoyang_2', 'operator2.chaoyang@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '朝阳操作员2', '010-44444444', 'county', '北京朝阳', 'operator', 'beginner',
 '朝阳办公室', '操作员', 'pending', '待审核的操作员', 'user-004'),

-- 县市级管理员（北京海淀）
('user-007', 'admin_haidian', 'admin.haidian@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '海淀区管理员', '010-55555555', 'county', '北京海淀', 'admin', 'intermediate',
 '海淀办公室', '主任', 'active', '海淀区管理员', 'user-002'),

-- 县市级操作员（北京海淀）
('user-008', 'operator_haidian', 'operator.haidian@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '海淀操作员', '010-66666666', 'county', '北京海淀', 'operator', 'beginner',
 '海淀办公室', '操作员', 'active', '海淀区操作员', 'user-007'),

-- 省级管理员（上海）
('user-009', 'admin_shanghai', 'admin.shanghai@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '上海省级管理员', '021-12345678', 'province', '上海', 'admin', 'advanced',
 '上海办公室', '主任', 'active', '上海省级管理员', 'user-001'),

-- 县市级管理员（上海浦东）
('user-010', 'admin_pudong', 'admin.pudong@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '浦东新区管理员', '021-87654321', 'county', '上海浦东', 'admin', 'intermediate',
 '浦东办公室', '主任', 'active', '浦东新区管理员', 'user-009'),

-- 县市级操作员（上海浦东）
('user-011', 'operator_pudong', 'operator.pudong@chamber.org', '$2b$12$R9h7cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jKMm6',
 '浦东操作员', '021-11111111', 'county', '上海浦东', 'operator', 'beginner',
 '浦东办公室', '操作员', 'inactive', '已禁用的操作员', 'user-010');

-- 插入操作日志示例
INSERT INTO chamber_user_logs (
  id, operator_id, target_user_id, action, old_value, new_value
) VALUES
('log-001', 'user-001', 'user-002', 'create', NULL, 
 '{"username":"admin_beijing","real_name":"北京省级管理员","level":"province","role":"admin"}'),

('log-002', 'user-002', 'user-004', 'create', NULL,
 '{"username":"admin_chaoyang","real_name":"朝阳区管理员","level":"county","role":"admin"}'),

('log-003', 'user-004', 'user-005', 'create', NULL,
 '{"username":"operator_chaoyang_1","real_name":"朝阳操作员1","level":"county","role":"operator"}'),

('log-004', 'user-004', 'user-006', 'status_change', 
 '{"status":"pending"}', '{"status":"active"}'),

('log-005', 'user-002', 'user-011', 'update',
 '{"status":"active","position":"操作员"}', '{"status":"inactive","position":"操作员"}');

