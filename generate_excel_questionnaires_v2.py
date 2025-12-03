"""
使用V2版本生成器生成Excel问卷
与Word格式保持一致：7列表格
"""

import sys
import os
import pandas as pd
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def parse_standard_to_options(standard: str) -> str:
    """将打分标准转换为简化的选项格式"""
    if pd.isna(standard) or not standard:
        return "A. 符合\nB. 部分符合\nC. 不符合"
    
    standard = str(standard).strip()
    
    # 尝试从打分标准中提取选项描述
    import re
    
    # 检查是否包含明确的选项描述
    if 'A.' in standard and 'B.' in standard:
        # 提取A、B、C选项
        options = []
        for letter in ['A', 'B', 'C', 'D']:
            pattern = f'{letter}\\.([^A-D]+?)(?=[A-D]\\.|$)'
            match = re.search(pattern, standard, re.DOTALL)
            if match:
                option_text = match.group(1).strip()
                # 清理选项文本
                option_text = re.sub(r'\s+', ' ', option_text)
                option_text = option_text[:100]  # 限制长度
                options.append(f"{letter}. {option_text}")
        
        if options:
            return '\n'.join(options)
    
    # 默认返回统一格式
    return "A. 符合\nB. 部分符合\nC. 不符合"


def extract_fill_blanks(standard: str) -> str:
    """从打分标准中提取需要填写的数据项"""
    if pd.isna(standard) or not standard:
        return ""
    
    standard = str(standard).strip()
    fill_items = []
    
    # 识别各种数据类型
    if '党员' in standard and '人数' in standard:
        fill_items.append('党员人数：______人（仅 A/B 选项填写）')
    
    if '支部党员大会' in standard or '支委会' in standard or '党小组会' in standard or '党课' in standard:
        parts = []
        if '支部党员大会' in standard:
            parts.append('上一年度支部党员大会召开次数：______次')
        if '支委会' in standard:
            parts.append('支委会：______次')
        if '党小组会' in standard:
            parts.append('党小组会：______次')
        if '党课' in standard:
            parts.append('党课：______次')
        if parts:
            fill_items.append('；'.join(parts))
    
    if '经费' in standard and '场所' in standard:
        fill_items.append('上一年度党组织活动经费金额：元；活动场所面积：㎡（仅 A/B 选项填写）')
    elif '经费' in standard or '金额' in standard:
        fill_items.append('上一年度党组织活动经费金额：______元')
    elif '场所' in standard or '面积' in standard:
        fill_items.append('活动场所面积：______㎡')
    
    if '记录' in standard and '份数' in standard:
        fill_items.append('相关行为记录份数：______份；涉及事项数量：______项')
    
    if '认同度' in standard:
        fill_items.append('参与认同度调查员工人数：______人；认同人数：人；认同度：%')
    
    if '培训' in standard and '法治' in standard:
        fill_items.append('管理层法治培训年度次数：______次；培训时长：______小时')
    
    if '融入' in standard and ('战略' in standard or '生产' in standard or '培训' in standard or '考核' in standard):
        fill_items.append('融入环节：□战略管理 □生产经营 □员工培训 □考核评价；对应环节实施频次：______')
    
    # 通用识别
    if not fill_items:
        if '人数' in standard:
            fill_items.append('人数：______人')
        if '次数' in standard:
            fill_items.append('次数：______次')
        if '金额' in standard or '万元' in standard:
            fill_items.append('金额：______万元')
        if '比例' in standard or '%' in standard:
            fill_items.append('比例：______%')
    
    return '；'.join(fill_items) if fill_items else ''


def generate_excel_questionnaire(excel_path: str, level: str, output_path: str):
    """生成Excel格式问卷"""
    # 读取数据
    df = pd.read_excel(excel_path, sheet_name=level)
    
    # 创建输出DataFrame，7列格式
    output_data = []
    
    for _, row in df.iterrows():
        output_data.append({
            '序号': int(row['序号']) if pd.notna(row['序号']) else '',
            '一级指标': row['一级指标'] if pd.notna(row['一级指标']) else '',
            '二级指标': row['二级指标'] if pd.notna(row['二级指标']) else '',
            '三级指标': row['三级指标'] if pd.notna(row['三级指标']) else '',
            '打分标准': row['打分标准'] if pd.notna(row['打分标准']) else '',
            '选项': parse_standard_to_options(row['打分标准']),
            '补充数据 / 说明': extract_fill_blanks(row['打分标准'])
        })
    
    output_df = pd.DataFrame(output_data)
    
    # 保存Excel
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        output_df.to_excel(writer, sheet_name=f'{level}问卷', index=False)
        
        # 调整列宽
        worksheet = writer.sheets[f'{level}问卷']
        worksheet.column_dimensions['A'].width = 8   # 序号
        worksheet.column_dimensions['B'].width = 15  # 一级指标
        worksheet.column_dimensions['C'].width = 15  # 二级指标
        worksheet.column_dimensions['D'].width = 20  # 三级指标
        worksheet.column_dimensions['E'].width = 50  # 打分标准
        worksheet.column_dimensions['F'].width = 50  # 选项
        worksheet.column_dimensions['G'].width = 40  # 补充数据/说明
    
    print(f"[成功] 生成{level}问卷: {output_path}")
    return output_path


def main():
    """主函数"""
    print("=" * 60)
    print("南开大学Excel问卷生成器 V2")
    print("=" * 60)
    print()
    
    # Excel文件路径
    excel_path = "nankai_indicators.xlsx"
    
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"[错误] 找不到Excel文件: {excel_path}")
        return
    
    print(f"[文件] Excel文件: {excel_path}")
    print()
    
    try:
        # 输出目录
        output_dir = "survey_generator/output/questionnaires"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("[进行中] 正在生成Excel问卷...")
        print()
        
        results = {}
        for level in ['初级', '中级', '高级']:
            output_path = os.path.join(output_dir, f"调查问卷_{level}_{timestamp}.xlsx")
            results[level] = generate_excel_questionnaire(excel_path, level, output_path)
        
        print()
        print("=" * 60)
        print("[成功] Excel问卷生成完成！")
        print("=" * 60)
        print()
        print("生成的文件：")
        for level, path in results.items():
            print(f"  - {level}: {path}")
        print()
        print("Excel问卷特点：")
        print("  * 7列表格：序号、一级指标、二级指标、三级指标、打分标准、选项、补充数据/说明")
        print("  * 与Word格式完全一致")
        print("  * 可直接在Excel中填写")
        print("  * 可导入Web系统")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print("[错误] 生成失败")
        print("=" * 60)
        print(f"错误信息: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()