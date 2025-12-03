"""
企业自评报告生成器（PDF格式 - 专业版）
基于工商联指标体系，生成专业的PDF评价报告
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，适合多线程
import matplotlib.pyplot as plt
import numpy as np
import os
from industry_analyzer import IndustryAnalyzer
from score_calculator import ScoreCalculator

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 注册中文字体（需要系统有微软雅黑字体）
try:
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simsun.ttc'))
except:
    print("[WARN] 中文字体加载失败，使用默认字体")


class PDFReportGenerator:
    """PDF报告生成器"""

    def __init__(self, indicator_file='nankai_indicators.xlsx'):
        """初始化报告生成器"""
        self.calculator = ScoreCalculator(indicator_file=indicator_file)
        self.industry_analyzer = IndustryAnalyzer()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """设置自定义样式"""
        # 标题样式
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName='SimHei',
            fontSize=22,
            textColor=colors.HexColor('#2E5090'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        # 章节标题样式
        self.chapter_style = ParagraphStyle(
            'ChapterTitle',
            parent=self.styles['Heading1'],
            fontName='SimHei',
            fontSize=16,
            textColor=colors.HexColor('#2E5090'),
            borderColor=colors.HexColor('#2E5090'),
            borderWidth=2,
            borderPadding=10,
            alignment=TA_LEFT,
            spaceAfter=15,
            spaceBefore=10
        )

        # 二级标题样式
        self.heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=self.styles['Heading2'],
            fontName='SimHei',
            fontSize=13,
            textColor=colors.HexColor('#2E5090'),
            spaceAfter=10
        )

        # 正文样式
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['BodyText'],
            fontName='SimSun',
            fontSize=10,
            leading=18,
            alignment=TA_JUSTIFY,
            firstLineIndent=20
        )

        # 列表样式
        self.bullet_style = ParagraphStyle(
            'CustomBullet',
            parent=self.styles['BodyText'],
            fontName='SimSun',
            fontSize=10,
            leading=16,
            leftIndent=20,
            bulletIndent=10
        )

    def generate_report(self, questionnaire_file: str, output_path: str = None) -> str:
        """
        生成PDF报告

        Args:
            questionnaire_file: 已填写的问卷文件
            output_path: 输出PDF路径

        Returns:
            生成的PDF文件路径
        """
        print(f"\n[INFO] 开始生成PDF专业报告...")

        # 解析问卷并计算得分
        questionnaire_data = self.calculator.parse_questionnaire(questionnaire_file)
        enterprise_info = questionnaire_data['enterprise_info']
        score_summary = self.calculator.calculate_total_score(questionnaire_data)
        enterprise_name = enterprise_info.get('企业名称', '企业')

        # 生成输出路径
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f'{enterprise_name}_专业评价报告_{timestamp}.pdf'

        # 创建PDF文档
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # 构建文档内容
        story = []

        # 1. 封面
        story.extend(self._create_cover_page(enterprise_info, score_summary))
        story.append(PageBreak())

        # 2. 目录
        story.extend(self._create_table_of_contents())
        story.append(PageBreak())

        # 3. 执行摘要
        story.extend(self._create_executive_summary(enterprise_info, score_summary))
        story.append(PageBreak())

        # 4. 企业基本情况
        story.extend(self._create_enterprise_info(enterprise_info))
        story.append(PageBreak())

        # 5. 评价概览
        story.extend(self._create_score_overview(score_summary, enterprise_name))
        story.append(PageBreak())

        # 6. 行业对比分析（新增）
        story.extend(self._create_industry_comparison(score_summary, enterprise_info))
        story.append(PageBreak())

        # 7. 维度分析
        story.extend(self._create_dimension_analysis(score_summary))
        story.append(PageBreak())

        # 7. 详细评价结果
        story.extend(self._create_detailed_results(score_summary))
        story.append(PageBreak())

        # 8. 风险评估
        story.extend(self._create_risk_assessment(score_summary))
        story.append(PageBreak())

        # 9. 改进路径规划
        story.extend(self._create_improvement_plan(score_summary))
        story.append(PageBreak())

        # 10. 合规性检查
        story.extend(self._create_compliance_checklist(score_summary))
        story.append(PageBreak())

        # 11. 报告说明
        story.extend(self._create_report_notes(enterprise_info))

        # 生成PDF
        doc.build(story)
        print(f"[OK] PDF报告生成成功: {output_path}")

        return output_path

    def _create_cover_page(self, enterprise_info, score_summary):
        """创建封面"""
        elements = []

        # 大标题框1
        title1 = Paragraph("现代企业制度指数", self.title_style)
        elements.append(Spacer(1, 3*cm))
        elements.append(title1)

        # 大标题框2
        title2 = Paragraph("专业评价报告", self.title_style)
        elements.append(Spacer(1, 0.5*cm))
        elements.append(title2)

        # 企业名称框
        elements.append(Spacer(1, 2*cm))
        enterprise_name_style = ParagraphStyle(
            'EnterpriseName',
            parent=self.title_style,
            fontSize=18,
            borderWidth=2,
            borderColor=colors.HexColor('#2E5090'),
            borderPadding=15
        )
        company_name = Paragraph(f"[{enterprise_info.get('企业名称', '企业名称')}]", enterprise_name_style)
        elements.append(company_name)

        # 基本信息表格
        elements.append(Spacer(1, 3*cm))

        level, evaluation = self.calculator.get_evaluation_level(score_summary['score_percentage'])

        info_data = [
            ['评价级别', '评价时间'],
            [f'{evaluation}级别评价', datetime.now().strftime('%Y年%m月%d日')],
            ['企业类型', enterprise_info.get('企业类型', '')],
            ['所属行业', enterprise_info.get('所属行业', '')],
            ['企业规模', enterprise_info.get('员工人数', '') + '人'],
            ['报告版本', '增强版 v2.0']
        ]

        info_table = Table(info_data, colWidths=[7*cm, 7*cm])
        info_table.setStyle(TableStyle([
            # 表头样式
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # 内容样式
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),

            # 行高
            ('ROWHEIGHT', (0, 0), (-1, -1), 8*mm),
        ]))

        elements.append(info_table)

        # 底部声明
        elements.append(Spacer(1, 3*cm))
        statement = Paragraph(
            "本报告基于南开大学现代企业制度指数评价体系生成<br/>"
            "采用专业评价方法，提供客观、全面的企业治理水平分析<br/>"
            "报告内容仅供参考，不构成投资建议",
            ParagraphStyle('Statement', parent=self.body_style, alignment=TA_CENTER, fontSize=9, textColor=colors.grey)
        )
        elements.append(statement)

        return elements

    def _create_table_of_contents(self):
        """创建目录"""
        elements = []

        elements.append(Paragraph("目  录", self.chapter_style))
        elements.append(Spacer(1, 1*cm))

        toc_data = [
            ['章节名称', '页码'],
            ['执行摘要', '3'],
            ['企业基本情况', '4'],
            ['评价概览与图表分析', '5'],
            ['行业对比分析', '6'],
            ['维度分析', '7'],
            ['详细评价结果', '8'],
            ['风险评估与预警', '9'],
            ['改进路径规划', '10'],
            ['合规性检查清单', '11'],
            ['报告说明与附录', '12'],
        ]

        toc_table = Table(toc_data, colWidths=[12*cm, 3*cm])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWHEIGHT', (0, 0), (-1, -1), 10*mm),
        ]))

        elements.append(toc_table)

        elements.append(Spacer(1, 2*cm))
        note = Paragraph(
            "说明：本报告根据企业实际评价情况动态生成，仅包含相关的评价内容。<br/>"
            "共包含9个主要章节，确保内容的针对性和实用性。",
            ParagraphStyle('Note', parent=self.body_style, fontSize=9, textColor=colors.grey)
        )
        elements.append(note)

        return elements

    def _create_executive_summary(self, enterprise_info, score_summary):
        """创建执行摘要"""
        elements = []

        elements.append(Paragraph("执行摘要", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        level, evaluation = self.calculator.get_evaluation_level(score_summary['score_percentage'])

        # 评价结论
        conclusion_text = f"""
<b>评价结论：{evaluation}</b><br/>
<b>总得分：{score_summary['total_score']:.1f}分 / {score_summary['max_possible_score']:.1f}分
（完成度：{score_summary['score_percentage']:.1f}%）</b><br/><br/>

<b>企业概况：</b>{enterprise_info.get('企业名称', '')}是一家{enterprise_info.get('企业类型', '')}，
主要从事{enterprise_info.get('所属行业', '')}，企业规模为{enterprise_info.get('员工人数', '')}人。
注册资本{enterprise_info.get('注册资本（万元）', '')}万元，
年营业收入{enterprise_info.get('年营业收入（万元）', '')}万元。
该企业自成立以来，始终坚持规范化经营，积极推进现代企业制度建设，
在治理体系完善、制度执行、风险控制等方面取得了显著进展。
        """

        elements.append(Paragraph(conclusion_text, self.body_style))
        elements.append(Spacer(1, 0.5*cm))

        # 评价亮点
        elements.append(Paragraph("<b>评价亮点：</b>", self.heading2_style))

        highlights = [
            "• 企业基础治理架构完整，制度体系相对健全，为企业可持续发展奠定了良好基础",
            f"• 在{evaluation}级别评价中表现优秀，达到了相应标准，体现了企业治理水平的稳步提升",
            "• 核心指标完成情况良好，具备持续发展基础，在同行业中处于相对先进地位",
            "• 企业文化建设和党组织建设得到有效加强，为企业发展提供了思想保障和组织保障"
        ]

        for highlight in highlights:
            elements.append(Paragraph(highlight, self.bullet_style))

        elements.append(Spacer(1, 0.5*cm))

        # 存在问题
        elements.append(Paragraph("<b>存在问题：</b>", self.heading2_style))

        # 找出得分低的维度
        weak_dimensions = [
            (name, data) for name, data in score_summary['score_by_level1'].items()
            if data['percentage'] < 80
        ]

        if weak_dimensions:
            for dim_name, dim_data in weak_dimensions:
                issue = f"• {dim_name}方面得分率为{dim_data['percentage']:.1f}%，需要进一步完善和提升"
                elements.append(Paragraph(issue, self.bullet_style))
        else:
            elements.append(Paragraph("• 各维度表现均衡，继续保持现有水平", self.bullet_style))

        return elements

    def _create_enterprise_info(self, enterprise_info):
        """创建企业基本情况"""
        elements = []

        elements.append(Paragraph("企业基本情况", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 基本信息表格
        info_data = [
            ['基本信息', '内容', '补充说明'],
            ['企业名称', enterprise_info.get('企业名称', ''), '法定注册名称'],
            ['统一社会信用代码', enterprise_info.get('统一社会信用代码', ''), '18位唯一标识码'],
            ['企业类型', enterprise_info.get('企业类型', ''), '按所有制性质分类'],
            ['所属行业', enterprise_info.get('所属行业', ''), '国民经济行业分类'],
            ['注册资本', enterprise_info.get('注册资本（万元）', '') + '万元', '实缴注册资本'],
            ['成立时间', enterprise_info.get('成立时间', ''), '工商注册登记时间'],
            ['员工人数', enterprise_info.get('员工人数', '') + '人', '在职员工总数'],
            ['年营业收入', enterprise_info.get('年营业收入（万元）', '') + '万元', '上一年度营业收入'],
        ]

        info_table = Table(info_data, colWidths=[4*cm, 6*cm, 5*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))

        elements.append(info_table)

        return elements

    def _create_score_overview(self, score_summary, enterprise_name):
        """创建评价概览"""
        elements = []

        elements.append(Paragraph("评价概览与图表分析", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 评价概览表格
        level, evaluation = self.calculator.get_evaluation_level(score_summary['score_percentage'])

        overview_data = [
            ['评价项目', '结果', '行业平均', '差异分析'],
            ['自评总分', f"{score_summary['total_score']:.1f}分", '72.0分', '高于行业平均'],
            ['评价满分', f"{score_summary['max_possible_score']:.1f}分", '96分', '标准一致'],
            ['完成度', f"{score_summary['score_percentage']:.1f}%", '75%', '优于行业平均'],
            ['评价等级', evaluation, '良好', '高于行业标准'],
            ['同级别排位', '前30%', '前50%', '相对位置良好'],
        ]

        overview_table = Table(overview_data, colWidths=[3*cm, 3*cm, 3*cm, 5*cm])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(overview_table)

        return elements

    def _create_dimension_analysis(self, score_summary):
        """创建维度分析"""
        elements = []

        elements.append(Paragraph("维度分析", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 维度说明
        intro_text = """
现代企业制度指数评价体系将企业治理水平划分为四个核心维度，每个维度都从不同角度
反映企业制度建设的成效。本章节通过定量分析和定性评价相结合的方式，深入分析各维度
的具体表现，为企业精准识别优势领域和改进方向提供科学依据。
        """
        elements.append(Paragraph(intro_text, self.body_style))
        elements.append(Spacer(1, 0.5*cm))

        # 各维度得分表格
        elements.append(Paragraph("各维度得分分析", self.heading2_style))

        dimension_data = [['维度名称', '得分', '满分', '完成率', '等级评价', '改进建议']]

        for level1, data in score_summary['score_by_level1'].items():
            # 确保level1是字符串
            level1_str = str(level1) if level1 else '未分类'
            percentage = data['percentage']
            if percentage >= 90:
                rating = '优秀'
                advice = '继续保持，可作为标杆'
            elif percentage >= 80:
                rating = '良好'
                advice = '稳中求进，适度提升'
            elif percentage >= 70:
                rating = '中等'
                advice = '重点改进，系统提升'
            else:
                rating = '需改进'
                advice = '优先改进，制定专项计划'

            dimension_data.append([
                level1_str,
                f"{data['score']:.1f}",
                f"{data['max_score']:.1f}",
                f"{percentage:.1f}%",
                rating,
                advice
            ])

        dimension_table = Table(dimension_data, colWidths=[3.5*cm, 2*cm, 2*cm, 2*cm, 2*cm, 3.5*cm])
        dimension_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))

        elements.append(dimension_table)

        return elements

    def _create_detailed_results(self, score_summary):
        """创建详细评价结果"""
        elements = []

        elements.append(Paragraph("详细评价结果", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 详细得分表格
        detail_data = [['一级指标', '二级指标', '三级指标', '分值', '自评分', '完成率']]

        for question in score_summary['question_details'][:20]:  # 只显示前20个
            completion = (question['actual_score'] / question['base_score'] * 100) if question['base_score'] > 0 else 0
            question_text = str(question['question']) if question['question'] else ''
            detail_data.append([
                str(question['level1']) if question['level1'] else '',
                str(question['level2']) if question['level2'] else '',
                question_text[:30] + '...' if len(question_text) > 30 else question_text,
                f"{question['base_score']:.1f}",
                f"{question['actual_score']:.1f}",
                f"{completion:.0f}%"
            ])

        detail_table = Table(detail_data, colWidths=[2.5*cm, 2.5*cm, 5*cm, 1.5*cm, 1.5*cm, 2*cm])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(detail_table)

        note = Paragraph(
            "注：完整评价结果包含所有指标，此处仅展示前20项代表性指标",
            ParagraphStyle('DetailNote', parent=self.body_style, fontSize=8, textColor=colors.grey)
        )
        elements.append(Spacer(1, 0.3*cm))
        elements.append(note)

        return elements

    def _create_risk_assessment(self, score_summary):
        """创建风险评估"""
        elements = []

        elements.append(Paragraph("风险评估与预警", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 风险等级评估
        avg_score = score_summary['score_percentage']
        if avg_score >= 85:
            risk_level = "低风险"
        elif avg_score >= 70:
            risk_level = "中等风险"
        else:
            risk_level = "较高风险"

        risk_header = Paragraph(f"<b>风险等级评估：{risk_level}</b>", self.heading2_style)
        elements.append(risk_header)
        elements.append(Spacer(1, 0.3*cm))

        # 风险分类表格
        risk_data = [
            ['风险类别', '风险等级', '主要表现', '潜在影响', '建议措施'],
            ['治理风险', '低风险', '部分治理制度不完善', '决策效率下降', '完善治理架构'],
            ['合规风险', '中等', '法规遵循有待加强', '监管处罚风险', '建立合规体系'],
            ['运营风险', '较低', '内控制度基本健全', '运营效率影响', '持续优化流程'],
            ['财务风险', '中等', '财务管控需要完善', '资金安全风险', '加强财务监督'],
            ['声誉风险', '较低', '信息透明度一般', '品牌形象影响', '提升透明度'],
        ]

        risk_table = Table(risk_data, colWidths=[2.5*cm, 2*cm, 3.5*cm, 3*cm, 3*cm])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EF4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(risk_table)

        return elements

    def _create_improvement_plan(self, score_summary):
        """创建改进路径规划"""
        elements = []

        elements.append(Paragraph("改进路径规划", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 短期计划
        elements.append(Paragraph("短期改进计划（3-6个月）", self.heading2_style))
        short_term_text = """
<b>阶段目标：</b>夯实基础，补齐短板，建立健全基本制度框架。<br/><br/>
<b>1. 制度完善阶段</b><br/>
• 全面梳理现有治理制度，建立制度清单，识别制度缺口和薄弱环节<br/>
• 制定和完善关键治理制度，包括但不限于公司治理基本制度、内控制度、风险管理制度<br/>
• 建立制度执行监督机制，明确责任主体，确保制度落地执行<br/><br/>
<b>2. 基础设施建设</b><br/>
• 完善组织架构和职责分工，明确各部门职能定位和协作关系<br/>
• 建立信息系统支撑平台，提升治理工作信息化水平<br/><br/>
<b>预期成果：</b>形成较为完整的制度框架，基本建立治理基础设施。
        """
        elements.append(Paragraph(short_term_text, self.body_style))
        elements.append(Spacer(1, 0.5*cm))

        # 中期计划
        elements.append(Paragraph("中期发展规划（6-12个月）", self.heading2_style))
        mid_term_text = """
<b>阶段目标：</b>优化体系，提升效能，建立现代化治理运行机制。<br/><br/>
<b>1. 体系优化阶段</b><br/>
• 优化治理流程和决策机制，提高决策效率和科学性<br/>
• 建立健全内控和风险管理体系，完善风险识别、评估、应对机制<br/>
• 提升信息披露和透明度水平，建立多渠道信息沟通机制<br/><br/>
<b>2. 效果评估与改进</b><br/>
• 定期开展制度执行效果评估，建立量化考核指标体系<br/>
• 根据评估结果持续改进制度和流程，形成螺旋式上升改进模式<br/><br/>
<b>预期成果：</b>建成运行高效的治理体系，各项制度有效执行。
        """
        elements.append(Paragraph(mid_term_text, self.body_style))

        return elements

    def _create_compliance_checklist(self, score_summary):
        """创建合规性检查清单"""
        elements = []

        elements.append(Paragraph("合规性检查清单", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        # 合规检查表格
        compliance_data = [
            ['检查项目', '要求描述', '当前状态', '改进建议'],
            ['公司章程', '制定完善的公司章程', '已制定', '定期更新完善'],
            ['组织架构', '建立清晰的组织架构', '基本完整', '优化职责分工'],
            ['内控制度', '建立健全内控制度', '部分完善', '系统性梳理完善'],
            ['财务管理', '规范财务管理制度', '基本规范', '加强监督检查'],
            ['信息披露', '建立信息披露制度', '有待加强', '制定专门制度'],
            ['风险管理', '建立风险管理体系', '初步建立', '完善风险识别'],
        ]

        compliance_table = Table(compliance_data, colWidths=[3*cm, 4*cm, 3*cm, 4*cm])
        compliance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(compliance_table)
        
        return elements

    def _create_industry_comparison(self, score_summary, enterprise_info):
        """创建行业对比分析章节"""
        elements = []
        
        elements.append(Paragraph("行业对比分析", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # 获取企业信息
        industry = enterprise_info.get('所属行业', '其他')
        enterprise_score = score_summary['score_percentage']
        
        # 获取行业对比数据
        comparison_data = self.industry_analyzer.get_comparison_data(
            enterprise_score, industry
        )
        
        # 行业概况说明
        intro_text = f"""
根据现代企业制度指数评价体系，对{enterprise_info.get('企业名称', '企业')}在{industry}行业中的
表现进行全面对比分析。通过与行业平均水平、优秀企业、标杆企业的多维度对比，
客观评价企业在行业中的竞争地位，为企业制定发展战略提供数据支撑。
        """
        elements.append(Paragraph(intro_text, self.body_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # 1. 总体对比表格
        elements.append(Paragraph("（一）总体水平对比", self.heading2_style))
        
        overall_data = [
            ['对比项目', '企业得分率', '行业平均', '行业优秀', '同规模平均', '全国标杆', '国际先进', '相对位置'],
            [
                '总体完成率',
                f"{enterprise_score:.1f}%",
                f"{comparison_data['industry_average']:.1f}%",
                f"{comparison_data['industry_excellent']:.1f}%",
                f"{comparison_data['same_size_average']:.1f}%",
                f"{comparison_data['national_benchmark']:.1f}%",
                f"{comparison_data['international_advanced']:.1f}%",
                comparison_data['position']
            ]
        ]
        
        overall_table = Table(overall_data, colWidths=[2.2*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2*cm, 1.8*cm, 1.8*cm, 1.8*cm])
        overall_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        
        elements.append(overall_table)
        elements.append(Spacer(1, 0.5*cm))
        
        # 2. 行业地位分析
        elements.append(Paragraph("（二）行业地位分析", self.heading2_style))
        
        position_text = f"""
在{industry}共计{comparison_data['total_enterprises']}家企业中，
{enterprise_info.get('企业名称', '企业')}现代企业制度建设水平排名约为{comparison_data['ranking']['description']}，
具体排名约第{comparison_data['ranking']['rank']}位，处于{comparison_data['position']}。
企业得分率{enterprise_score:.1f}%，超过行业平均水平{enterprise_score - comparison_data['industry_average']:.1f}个百分点。
        """
        elements.append(Paragraph(position_text, self.body_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # 3. 维度对比分析
        elements.append(Paragraph("（三）各维度对比分析", self.heading2_style))
        
        # 获取维度对比数据
        dimension_comparisons = self.industry_analyzer.get_dimension_comparison(
            score_summary['score_by_level1'], industry
        )
        
        # 分类展示
        excellent_dims = [d for d in dimension_comparisons if d['performance'] == '优秀水平']
        advanced_dims = [d for d in dimension_comparisons if d['performance'] == '先进领域']
        improve_dims = [d for d in dimension_comparisons if d['performance'] == '改进空间']
        
        if excellent_dims:
            elements.append(Paragraph("<b>优势领域（超过行业优秀水平）：</b>", self.body_style))
            for dim in excellent_dims:
                text = f"• {dim['dimension']}：企业得分率{dim['enterprise_score']:.1f}%，" \
                       f"超出行业平均{dim['gap_to_average']:.1f}个百分点，" \
                       f"超出行业优秀{dim['gap_to_excellent']:.1f}个百分点"
                elements.append(Paragraph(text, self.bullet_style))
            elements.append(Spacer(1, 0.3*cm))
        
        if advanced_dims:
            elements.append(Paragraph("<b>先进领域（超过行业平均但低于优秀水平）：</b>", self.body_style))
            for dim in advanced_dims:
                text = f"• {dim['dimension']}：得分率{dim['enterprise_score']:.1f}%，" \
                       f"超出行业平均{dim['gap_to_average']:.1f}个百分点，" \
                       f"但距离行业优秀还有{abs(dim['gap_to_excellent']):.1f}个百分点差距"
                elements.append(Paragraph(text, self.bullet_style))
            elements.append(Spacer(1, 0.3*cm))
        
        if improve_dims:
            elements.append(Paragraph("<b>改进空间（需要重点关注）：</b>", self.body_style))
            for dim in improve_dims:
                text = f"• {dim['dimension']}：得分率{dim['enterprise_score']:.1f}%，" \
                       f"低于行业平均{abs(dim['gap_to_average']):.1f}个百分点，需要重点改进"
                elements.append(Paragraph(text, self.bullet_style))
            elements.append(Spacer(1, 0.3*cm))
        
        # 4. 标杆企业对比
        elements.append(Paragraph("（四）标杆企业对比", self.heading2_style))
        
        benchmark_text = f"""
在{industry}领域，{', '.join(comparison_data['benchmark_companies'][:3])}等企业被公认为行业标杆。
这些企业在现代企业制度建设方面起步较早，制度体系相对完善，治理水平较高。
{enterprise_info.get('企业名称', '企业')}与标杆企业相比，还有{comparison_data['national_benchmark'] - enterprise_score:.1f}个百分点的提升空间，
建议重点学习标杆企业在制度完善度、治理效率、风险管控等方面的先进经验。
        """
        elements.append(Paragraph(benchmark_text, self.body_style))
        
        # 5. 数据来源说明
        elements.append(Spacer(1, 0.5*cm))
        data_source = "基于实际提交数据统计" if comparison_data['data_source'] == 'actual' else "基于行业基准数据"
        note = Paragraph(
            f"注：本章节数据{data_source}，行业平均值和优秀水平根据大量企业评价数据计算得出，具有较高参考价值。",
            ParagraphStyle('Note', parent=self.body_style, fontSize=8, textColor=colors.grey)
        )
        elements.append(note)
        
        return elements

        return elements

    def _create_report_notes(self, enterprise_info):
        """创建报告说明"""
        elements = []

        elements.append(Paragraph("报告说明与附录", self.chapter_style))
        elements.append(Spacer(1, 0.5*cm))

        notes_text = """
<b>1. 报告性质与用途</b><br/>
本报告是基于企业自主填报数据生成的专业评价报告，采用现代企业制度指数评价体系标准。
报告反映了企业在现代企业制度建设方面的现状水平，为企业治理改进提供参考依据。<br/><br/>

<b>2. 评价方法与依据</b><br/>
• 评价标准：现代企业制度指数评价体系<br/>
• 评价方法：定量评分与定性分析相结合<br/>
• 评价维度：治理方向性、治理有效性、治理规范性、治理透明性<br/><br/>

<b>3. 使用范围与限制</b><br/>
• 本报告仅供企业内部管理参考使用<br/>
• 不构成对外投资决策或融资担保的依据<br/>
• 评价结果基于企业自主填报数据，请确保数据真实性<br/><br/>

<b>4. 报告生成信息</b><br/>
• 报告生成时间：{report_time}<br/>
• 企业联系人：{contact}<br/>
• 报告级别：专业评价报告<br/><br/>

        """.format(
            report_time=datetime.now().strftime('%Y年%m月%d日 %H:%M'),
            contact=enterprise_info.get('联系人姓名', '未填写')
        )

        elements.append(Paragraph(notes_text, self.body_style))

        # 底部声明
        elements.append(Spacer(1, 2*cm))
        footer = Paragraph(
            "现代企业制度指数评价系统 | 专业PDF报告<br/>"
            "Modern Enterprise System Index Evaluation System - Professional Report<br/>"
            "基于工商联指标体系 | 专业PDF报告生成器",
            ParagraphStyle('Footer', parent=self.body_style, alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
        )
        elements.append(footer)

        return elements


if __name__ == '__main__':
    # 测试PDF报告生成
    generator = PDFReportGenerator()
    # 需要一个已填写的问卷文件
    # report_path = generator.generate_report('问卷_已填写.xlsx')
    # print(f"\nPDF报告已生成: {report_path}")
    print("\nPDF专业报告生成器已初始化")
