import os, json, pandas as pd, time
from datetime import datetime

BASE = 'storage/submissions'
os.makedirs(BASE, exist_ok=True)


def make_excel(path: str, pct: float):
    """创建简单的问卷Excel：10题，总分100，按给定百分比分配得分。"""
    rows = []
    # 10题，每题分值10
    per = pct / 10.0
    level1s = ['治理方向性','治理规范性','治理科学性','治理安全性','治理社会性']
    for i in range(10):
        rows.append({
            '序号': i + 1,
            '一级指标': level1s[i % len(level1s)],
            '问题类型': '合规项',
            '分值': 10,
            # 答案使用JSON，兼容现有解析（score字段）
            '答案': json.dumps({'score': per}),
        })
    df = pd.DataFrame(rows)
    with pd.ExcelWriter(path, engine='openpyxl') as w:
        df.to_excel(w, index=False, sheet_name='问卷')


CASES = [
    ('衡水制造', '河北省', '衡水市', '桃城区', 'beginner', 45),
    ('石家庄食品', '河北省', '石家庄市', '长安区', 'intermediate', 62),
    ('保定电气', '河北省', '保定市', '竞秀区', 'advanced', 77),
    ('太原钢铁', '山西省', '太原市', '迎泽区', 'intermediate', 83),
    ('北京数科', '北京市', '海淀区', '中关村', 'advanced', 91),
    ('天津船舶', '天津市', '滨海新区', '塘沽', 'beginner', 68),
    ('上海新材', '上海市', '浦东新区', '张江', 'advanced', 54),
    ('深圳创科', '广东省', '深圳市', '南山区', 'advanced', 88),
    ('广州医药', '广东省', '广州市', '天河区', 'intermediate', 72),
    ('成都文旅', '四川省', '成都市', '锦江区', 'intermediate', 61),
    ('武汉光电', '湖北省', '武汉市', '洪山区', 'beginner', 36),
    ('杭州互联网', '浙江省', '杭州市', '余杭区', 'advanced', 95),
]


def main():
    count = 0
    for idx, (name, prov, city, dist, level, pct) in enumerate(CASES, start=1):
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_name = f'submission_{name}_{ts}.json'
        xlsx_name = f'问卷_{name}_{ts}.xlsx'
        json_path = os.path.join(BASE, json_name)
        xlsx_path = os.path.join(BASE, xlsx_name)

        make_excel(xlsx_path, pct)

        data = {
            'enterprise_info': {
                '企业名称': name,
                '企业类型': '有限责任公司',
                '所属行业': '综合',
                '联系人姓名': '联系人',
                '联系人邮箱': 'test@example.com',
                '联系人电话': '13800000000',
                '省/直辖市': prov,
                '市/州': city,
                '区县': dist,
            },
            'answers': {},
            'user_type': 'enterprise',
            'user_level': level,
            'username': f'demo_{idx}'
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        count += 1
        time.sleep(0.2)
    print(f'OK, generated {count} demo submissions into {BASE}')


if __name__ == '__main__':
    main()




