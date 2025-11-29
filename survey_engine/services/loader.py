# -*- coding: utf-8 -*-
"""
SurveyLoader: 统一管理问卷指标文件路径与题目加载逻辑。
当前为薄封装，内部复用 nankai_indicator_loader，以便后续完全迁移实现。
"""
from __future__ import annotations
import json
import os
from typing import List, Dict

from nankai_indicator_loader import load_questions_by_level, map_user_to_level


class SurveyLoader:
    def __init__(self, config_path: str = 'config.json') -> None:
        self.config_path = config_path
        self._nk_path = None
        self._load_config()

    def _load_config(self) -> None:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                conf = json.load(f)
                self._nk_path = (conf.get('indicators') or {}).get('nk_excel_path')
        except Exception:
            self._nk_path = None

    @property
    def nk_excel_path(self) -> str | None:
        if self._nk_path and os.path.exists(self._nk_path):
            return self._nk_path
        # 回退：仓库内备份文件
        fallback = '指标体系_备份.xlsx'
        if os.path.exists(fallback):
            return fallback
        # 再回退：原项目默认绝对路径（可能不存在）
        return self._nk_path

    def resolve_level_key(self, user_type: str | None, user_level: str | None, excel_level: str | None) -> str:
        if excel_level:
            return excel_level
        if user_type and user_level:
            return map_user_to_level(user_type, user_level)
        return 'advanced'

    def get_questions(self, level_key: str) -> List[Dict]:
        path = self.nk_excel_path
        if not path or not os.path.exists(path):
            raise FileNotFoundError('指标文件不存在，请在config.json配置indicators.nk_excel_path或放置指标体系_备份.xlsx')
        return load_questions_by_level(path, level_key)

