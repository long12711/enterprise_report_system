-- =============================================
-- 将“已有一份问卷”的题目克隆成三份等级问卷（初/中/高）
-- 用途：把之前生成/维护的一份问卷题目，一键复制为三套题库
-- 运行环境：MySQL 8.0
-- 使用方法：
--   1) 替换 @SRC_SURVEY_ID 为你的源问卷ID
--   2) 执行本脚本
--   3) 执行完成后会输出新建问卷ID与题目数量
-- =============================================

-- 统一本会话字符集与排序规则，避免不同表/连接的 collation 冲突
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET collation_connection = 'utf8mb4_unicode_ci';

USE enterprise_portal;

-- 1) 配置你的源问卷ID
SET @SRC_SURVEY_ID = 'survey_demo_01';  -- TODO: 替换为你现有问卷ID

-- 2) 生成三个新问卷ID
SET @SURV_BEGIN = UUID();
SET @SURV_INTER = UUID();
SET @SURV_ADV  = UUID();

-- 3) 新建三份问卷（保持启用状态，total_questions 后续回填）
INSERT INTO enterprise_surveys(id,name,level,description,status,total_questions,created_at,updated_at)
VALUES
(@SURV_BEGIN,'（自动生成）基础问卷-初级','初级','由脚本克隆自源问卷','active',0,NOW(),NOW()),
(@SURV_INTER,'（自动生成）基础问卷-中级','中级','由脚本克隆自源问卷','active',0,NOW(),NOW()),
(@SURV_ADV ,'（自动生成）基础问卷-高级','高级','由脚本克隆自源问卷','active',0,NOW(),NOW());

-- 4) 将源问卷题目克隆到三份问卷
INSERT INTO survey_questions(id,survey_id,indicator_id,question_text,question_type,options,required,sort_order,created_at)
SELECT UUID(), @SURV_BEGIN, indicator_id, question_text, question_type, options, required, sort_order, NOW()
FROM survey_questions WHERE BINARY survey_id = BINARY @SRC_SURVEY_ID ORDER BY sort_order;

INSERT INTO survey_questions(id,survey_id,indicator_id,question_text,question_type,options,required,sort_order,created_at)
SELECT UUID(), @SURV_INTER, indicator_id, question_text, question_type, options, required, sort_order, NOW()
FROM survey_questions WHERE BINARY survey_id = BINARY @SRC_SURVEY_ID ORDER BY sort_order;

INSERT INTO survey_questions(id,survey_id,indicator_id,question_text,question_type,options,required,sort_order,created_at)
SELECT UUID(), @SURV_ADV,  indicator_id, question_text, question_type, options, required, sort_order, NOW()
FROM survey_questions WHERE BINARY survey_id = BINARY @SRC_SURVEY_ID ORDER BY sort_order;

-- 5) 回填题目数量
UPDATE enterprise_surveys s
SET total_questions = (SELECT COUNT(*) FROM survey_questions q WHERE q.survey_id=s.id)
WHERE s.id IN (@SURV_BEGIN,@SURV_INTER,@SURV_ADV);

-- 6) 输出结果
SELECT 'BEGIN_ID' AS tag, @SURV_BEGIN AS survey_id
UNION ALL SELECT 'INTER_ID', @SURV_INTER
UNION ALL SELECT 'ADV_ID',   @SURV_ADV;

SELECT s.id,s.name,s.level,s.status,s.total_questions
FROM enterprise_surveys s
WHERE s.id IN (@SURV_BEGIN,@SURV_INTER,@SURV_ADV);

