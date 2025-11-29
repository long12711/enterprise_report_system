# -*- coding: utf-8 -*-
"""
report_engine.services
集中导出各类报告生成器，采用惰性加载（lazy import），避免在应用启动阶段就引入
matplotlib/reportlab 等重依赖，便于在无这些依赖时完成启动与基础接口冒烟测试。
真正调用生成方法时，再加载真实实现与依赖。
"""
from __future__ import annotations
from typing import Any


class _LazyBase:
    _real: Any | None = None
    _real_cls_path: str = ''  # e.g. 'enterprise_report_generator.EnterpriseReportGenerator'

    def _ensure(self):
        if self._real is None:
            module_path, class_name = self._real_cls_path.rsplit('.', 1)
            mod = __import__(module_path, fromlist=[class_name])
            real_cls = getattr(mod, class_name)
            self._real = real_cls()  # type: ignore


class EnterpriseReportGenerator(_LazyBase):
    _real_cls_path = 'enterprise_report_generator.EnterpriseReportGenerator'

    def generate_report(self, *args, **kwargs):
        self._ensure()
        return self._real.generate_report(*args, **kwargs)  # type: ignore


class PDFReportGenerator(_LazyBase):
    _real_cls_path = 'pdf_report_generator.PDFReportGenerator'

    def generate_report(self, *args, **kwargs):
        self._ensure()
        return self._real.generate_report(*args, **kwargs)  # type: ignore


class ProfessionalReportGenerator(_LazyBase):
    _real_cls_path = 'professional_report_generator.ProfessionalReportGenerator'

    def generate_report(self, *args, **kwargs):
        self._ensure()
        return self._real.generate_report(*args, **kwargs)  # type: ignore


class ComprehensiveAnalysisGenerator(_LazyBase):
    _real_cls_path = 'comprehensive_analysis_generator.ComprehensiveAnalysisGenerator'

    def generate_comprehensive_report(self, *args, **kwargs):
        self._ensure()
        return self._real.generate_comprehensive_report(*args, **kwargs)  # type: ignore


class OverallReportGenerator(_LazyBase):
    _real_cls_path = 'overall_report_generator.OverallReportGenerator'

    def generate_report(self, *args, **kwargs):
        self._ensure()
        return self._real.generate_report(*args, **kwargs)  # type: ignore


__all__ = [
    'EnterpriseReportGenerator',
    'PDFReportGenerator',
    'ProfessionalReportGenerator',
    'ComprehensiveAnalysisGenerator',
    'OverallReportGenerator',
]
