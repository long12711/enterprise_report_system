"""
指标体系管理数据模型
"""

from datetime import datetime
import json
import os
from typing import List, Dict, Optional

class IndicatorModel:
    """指标模型"""
    
    def __init__(self, data_file='indicator_management/data/indicators.json'):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """确保数据文件存在"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> List[Dict]:
        """加载数据"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: List[Dict]):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self, level: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """获取所有指标"""
        data = self._load_data()
        
        # 筛选
        if level:
            data = [item for item in data if level in item.get('applicable_levels', [])]
        if status:
            data = [item for item in data if item.get('status') == status]
        
        return data
    
    def get_by_id(self, indicator_id: str) -> Optional[Dict]:
        """根据ID获取指标"""
        data = self._load_data()
        for item in data:
            if item['id'] == indicator_id:
                return item
        return None
    
    def create(self, indicator: Dict) -> Dict:
        """创建指标"""
        data = self._load_data()
        
        # 生成ID
        if 'id' not in indicator:
            indicator['id'] = f"indicator_{len(data) + 1:03d}"
        
        # 添加时间戳
        indicator['created_at'] = datetime.now().isoformat()
        indicator['updated_at'] = datetime.now().isoformat()
        
        # 默认状态
        if 'status' not in indicator:
            indicator['status'] = 'active'
        
        data.append(indicator)
        self._save_data(data)
        
        return indicator
    
    def update(self, indicator_id: str, updates: Dict) -> Optional[Dict]:
        """更新指标"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item['id'] == indicator_id:
                item.update(updates)
                item['updated_at'] = datetime.now().isoformat()
                data[i] = item
                self._save_data(data)
                return item
        
        return None
    
    def delete(self, indicator_id: str) -> bool:
        """删除指标"""
        data = self._load_data()
        original_len = len(data)
        
        data = [item for item in data if item['id'] != indicator_id]
        
        if len(data) < original_len:
            self._save_data(data)
            return True
        
        return False


class ScoringRuleModel:
    """评分规则模型"""
    
    def __init__(self, data_file='indicator_management/data/scoring_rules.json'):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """确保数据文件存在"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> List[Dict]:
        """加载数据"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: List[Dict]):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_by_level(self, level: str) -> List[Dict]:
        """按级别获取评分规则"""
        data = self._load_data()
        return [item for item in data if item.get('level') == level]
    
    def get_by_indicator(self, indicator_id: str) -> List[Dict]:
        """按指标ID获取评分规则"""
        data = self._load_data()
        return [item for item in data if item.get('indicator_id') == indicator_id]
    
    def create(self, rule: Dict) -> Dict:
        """创建评分规则"""
        data = self._load_data()
        
        # 生成ID
        if 'id' not in rule:
            rule['id'] = f"rule_{len(data) + 1:03d}"
        
        # 添加时间戳
        rule['created_at'] = datetime.now().isoformat()
        rule['updated_at'] = datetime.now().isoformat()
        
        # 默认状态
        if 'status' not in rule:
            rule['status'] = 'active'
        
        data.append(rule)
        self._save_data(data)
        
        return rule
    
    def update(self, rule_id: str, updates: Dict) -> Optional[Dict]:
        """更新评分规则"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item['id'] == rule_id:
                item.update(updates)
                item['updated_at'] = datetime.now().isoformat()
                data[i] = item
                self._save_data(data)
                return item
        
        return None
    
    def delete(self, rule_id: str) -> bool:
        """删除评分规则"""
        data = self._load_data()
        original_len = len(data)
        
        data = [item for item in data if item['id'] != rule_id]
        
        if len(data) < original_len:
            self._save_data(data)
            return True
        
        return False


class QuestionnaireVersionModel:
    """问卷版本模型"""
    
    def __init__(self, data_file='indicator_management/data/questionnaire_versions.json'):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """确保数据文件存在"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self) -> List[Dict]:
        """加载数据"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: List[Dict]):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_all(self, level: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """获取所有问卷版本"""
        data = self._load_data()
        
        # 筛选
        if level:
            data = [item for item in data if item.get('level') == level]
        if status:
            data = [item for item in data if item.get('status') == status]
        
        # 按创建时间倒序排序
        data.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return data
    
    def get_by_id(self, version_id: str) -> Optional[Dict]:
        """根据ID获取问卷版本"""
        data = self._load_data()
        for item in data:
            if item['id'] == version_id:
                return item
        return None
    
    def get_versions(self, questionnaire_id: str) -> List[Dict]:
        """获取问卷的所有版本"""
        data = self._load_data()
        versions = [item for item in data if item.get('questionnaire_id') == questionnaire_id]
        versions.sort(key=lambda x: x.get('version', ''), reverse=True)
        return versions
    
    def create(self, questionnaire: Dict) -> Dict:
        """创建问卷版本"""
        data = self._load_data()
        
        # 生成ID
        if 'id' not in questionnaire:
            questionnaire['id'] = f"questionnaire_v{len(data) + 1}"
        
        # 添加时间戳
        questionnaire['created_at'] = datetime.now().isoformat()
        questionnaire['updated_at'] = datetime.now().isoformat()
        
        # 默认状态
        if 'status' not in questionnaire:
            questionnaire['status'] = 'draft'
        
        data.append(questionnaire)
        self._save_data(data)
        
        return questionnaire
    
    def update(self, version_id: str, updates: Dict) -> Optional[Dict]:
        """更新问卷版本"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item['id'] == version_id:
                item.update(updates)
                item['updated_at'] = datetime.now().isoformat()
                data[i] = item
                self._save_data(data)
                return item
        
        return None
    
    def publish(self, version_id: str) -> Optional[Dict]:
        """发布问卷版本"""
        data = self._load_data()
        
        for i, item in enumerate(data):
            if item['id'] == version_id:
                # 将同级别的其他active版本设为archived
                level = item.get('level')
                for j, other in enumerate(data):
                    if other.get('level') == level and other.get('status') == 'active':
                        data[j]['status'] = 'archived'
                        data[j]['archived_at'] = datetime.now().isoformat()
                
                # 发布当前版本
                item['status'] = 'active'
                item['published_at'] = datetime.now().isoformat()
                item['updated_at'] = datetime.now().isoformat()
                data[i] = item
                self._save_data(data)
                return item
        
        return None
    
    def clone(self, version_id: str, new_version: str) -> Optional[Dict]:
        """克隆问卷版本"""
        data = self._load_data()
        
        # 找到原版本
        original = None
        for item in data:
            if item['id'] == version_id:
                original = item.copy()
                break
        
        if not original:
            return None
        
        # 创建新版本
        new_questionnaire = original.copy()
        new_questionnaire['id'] = f"questionnaire_v{len(data) + 1}"
        new_questionnaire['version'] = new_version
        new_questionnaire['status'] = 'draft'
        new_questionnaire['parent_version'] = version_id
        new_questionnaire['created_at'] = datetime.now().isoformat()
        new_questionnaire['updated_at'] = datetime.now().isoformat()
        new_questionnaire.pop('published_at', None)
        new_questionnaire.pop('archived_at', None)
        
        data.append(new_questionnaire)
        self._save_data(data)
        
        return new_questionnaire