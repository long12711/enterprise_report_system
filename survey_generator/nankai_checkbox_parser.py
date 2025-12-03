"""
南开问卷复选框解析器
用于解析补充说明中的复选框选项和补充数据
"""

import re
import pandas as pd


def parse_supplement_data(supplement_text):
    """
    解析补充数据/说明列的内容
    
    Args:
        supplement_text: 补充数据/说明文本，如"党员人数：___人（仅A/B选项填写）"
    
    Returns:
        dict: {
            'conditions': list,      # 条件列表（如果有编号条件）
            'fill_blanks': list,     # 填空项列表
            'other_text': str        # 其他说明文字
        }
    """
    if not supplement_text or pd.isna(supplement_text):
        return {
            'conditions': [],
            'fill_blanks': [],
            'other_text': ''
        }
    
    conditions = []
    fill_blanks = []
    other_text = supplement_text
    
    # 1. 提取编号条件（如：1. xxx 2. xxx）
    numbered_pattern = r'(\d+)[\.、\)）]\s*([^；\n]+?)(?=\s*\d+[\.、\)）]|；|$)'
    matches = re.findall(numbered_pattern, supplement_text, re.DOTALL)
    
    if matches:
        for num, cond in matches:
            cond_text = cond.strip().strip('；;，,')
            if cond_text and len(cond_text) > 3:
                conditions.append(f"{num}. {cond_text}")
        # 移除条件部分
        other_text = re.sub(numbered_pattern, '', other_text)
    
    # 2. 提取填空项（格式：xxx：______xxx 或 xxx：___xxx）
    blank_pattern = r'([^：\n]+)：[_\s]+([^；\n\(（]*)'
    blank_matches = re.findall(blank_pattern, supplement_text)
    
    for match in blank_matches:
        label = match[0].strip()
        unit = match[1].strip() if match[1] else ''
        if label and not any(char.isdigit() and label.startswith(char) for char in '123456789'):
            # 排除编号条件
            fill_blanks.append(f"{label}{('（' + unit + '）') if unit else ''}")
    
    # 3. 清理other_text
    other_text = re.sub(blank_pattern, '', other_text)
    other_text = re.sub(r'[_\s]+', ' ', other_text).strip()
    other_text = re.sub(r'；+', '；', other_text).strip('；')
    
    return {
        'conditions': conditions,
        'fill_blanks': fill_blanks,
        'other_text': other_text
    }

def parse_checkboxes(supplement_text):
    """
    从补充说明文本中解析复选框选项
    
    Args:
        supplement_text: 补充说明文本，如"融入环节：□战略管理 □生产经营 □员工培训 □考核评价"
    
    Returns:
        dict: {
            'has_checkboxes': bool,  # 是否包含复选框
            'checkbox_label': str,    # 复选框标签，如"融入环节"
            'checkbox_options': list, # 复选框选项列表
            'other_fields': str       # 其他非复选框字段
        }
    """
    if not supplement_text or pd.isna(supplement_text):
        return {
            'has_checkboxes': False,
            'checkbox_label': '',
            'checkbox_options': [],
            'other_fields': supplement_text or ''
        }
    
    # 查找复选框模式：标签：□选项1 □选项2 □选项3
    checkbox_pattern = r'([^：]+)：((?:□[^□；]+)+)'
    matches = re.findall(checkbox_pattern, supplement_text)
    
    if not matches:
        return {
            'has_checkboxes': False,
            'checkbox_label': '',
            'checkbox_options': [],
            'other_fields': supplement_text
        }
    
    # 提取第一组复选框（通常一个问题只有一组）
    label, options_text = matches[0]
    
    # 提取所有选项
    options = re.findall(r'□([^□；]+)', options_text)
    options = [opt.strip() for opt in options if opt.strip()]
    
    # 移除复选框部分，保留其他字段
    other_fields = re.sub(checkbox_pattern, '', supplement_text, count=1).strip()
    # 清理多余的分号
    other_fields = re.sub(r'；+', '；', other_fields).strip('；')
    
    return {
        'has_checkboxes': True,
        'checkbox_label': label.strip(),
        'checkbox_options': options,
        'other_fields': other_fields
    }


def parse_conditions_from_standard(scoring_standard):
    """
    从打分标准中解析条件列表（不区分A/B/C选项）
    
    Args:
        scoring_standard: 打分标准文本，如"评分标准：以下全部完成得1分\n1.xxx\n2.xxx"
    
    Returns:
        list: 条件列表，如 ['1. xxx', '2. xxx']
    """
    if not scoring_standard:
        return []
    
    conditions = []
    
    # 匹配编号条件（1. xxx 2. xxx 或 1）xxx 2）xxx）
    # 支持多种编号格式：1. 1） 1、
    # 修改正则：匹配到下一个编号或分号或换行
    numbered_pattern = r'(\d+)[\.、\)）]\s*([^；\n]+?)(?=\s*\d+[\.、\)）]|；|$)'
    matches = re.findall(numbered_pattern, scoring_standard, re.DOTALL)
    
    if matches:
        for num, cond in matches:
            cond_text = cond.strip().strip('；;，,')
            # 过滤掉太短的文本和明显不是条件的文本
            if cond_text and len(cond_text) > 5:
                conditions.append(f"{num}. {cond_text}")
    
    return conditions


def should_show_checkboxes(selected_option, scoring_standard):
    """
    判断选择某个选项后是否应该显示复选框
    
    Args:
        selected_option: 用户选择的选项，如"A"或"B"
        scoring_standard: 打分标准文本
    
    Returns:
        bool: 是否应该显示复选框
    """
    if not selected_option or not scoring_standard:
        return False
    
    # 查找该选项的描述
    option_pattern = rf'{selected_option}[\.、\s]*([^A-D]+?)(?=[A-D][\.\s]|$)'
    match = re.search(option_pattern, scoring_standard)
    
    if not match:
        return False
    
    option_desc = match.group(1)
    
    # 如果选项描述中包含"满足X项"、"完成X项"等关键词，则需要显示复选框
    keywords = ['满足.*项', '完成.*项', '建立.*类', '包含.*项', r'\d+[\.、\)）]']
    for keyword in keywords:
        if re.search(keyword, option_desc):
            return True
    
    return False


# 测试代码
if __name__ == '__main__':
    import pandas as pd
    
    # 测试用例1：有复选框
    text1 = "融入环节：□战略管理 □生产经营 □员工培训 □考核评价；对应环节实施频次：______"
    result1 = parse_checkboxes(text1)
    print("测试1:", result1)
    
    # 测试用例2：有复选框
    text2 = "沟通对象：□员工 □客户 □供应商 □债权人 □社区；沟通次数：______次 / 年"
    result2 = parse_checkboxes(text2)
    print("测试2:", result2)
    
    # 测试用例3：无复选框
    text3 = "党员人数：______人（仅 A/B 选项填写）"
    result3 = parse_checkboxes(text3)
    print("测试3:", result3)
    
    # 测试用例4：判断是否显示复选框
    standard = "A. 满足 4-5 项（有规划 + 融入战略 / 生产 / 培训 / 考核） B. 满足 1-3 项 C. 均未满足"
    print("测试4 - 选A:", should_show_checkboxes('A', standard))
    print("测试4 - 选B:", should_show_checkboxes('B', standard))