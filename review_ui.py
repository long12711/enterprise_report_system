"""
审核功能UI界面
使用Tkinter实现审核界面
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from typing import Optional, Callable
from review_service import review_service
from review_models import ReviewStatus, ReportType


class ReviewDetailWindow:
    """审核详情窗口"""
    
    def __init__(self, parent, report_id: str, on_review_callback: Optional[Callable] = None):
        """
        初始化审核详情窗口
        
        Args:
            parent: 父窗口
            report_id: 报告ID
            on_review_callback: 审核完成后的回调函数
        """
        self.parent = parent
        self.report_id = report_id
        self.on_review_callback = on_review_callback
        
        # 获取报告和问卷数据
        self.report = review_service.get_review_report(report_id)
        self.questionnaire = review_service.get_questionnaire_by_report(report_id)
        
        if not self.report:
            messagebox.showerror("错误", "报告不存在")
            return
        
        # 创建窗口
        self.window = tk.Toplevel(parent)
        self.window.title(f"审核详情 - {self.report.enterprise_name}")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # 创建UI
        self._create_ui()
    
    def _create_ui(self):
        """创建UI界面"""
        # 创建主容器
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标签页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 报告标签页
        self._create_report_tab(notebook)
        
        # 原问卷标签页
        self._create_questionnaire_tab(notebook)
        
        # 审核操作标签页
        self._create_review_tab(notebook)
        
        # 晋级操作标签页
        self._create_promotion_tab(notebook)
    
    def _create_report_tab(self, notebook):
        """创建报告标签页"""
        report_frame = ttk.Frame(notebook)
        notebook.add(report_frame, text="查看报告")
        
        # 基本信息
        info_frame = ttk.LabelFrame(report_frame, text="基本信息", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_data = [
            ("企业名称", self.report.enterprise_name),
            ("联系人", self.report.user_name),
            ("当前级别", self.report.current_level),
            ("报告类型", self.report.report_type.value),
            ("创建时间", self.report.created_time.strftime("%Y-%m-%d %H:%M:%S")),
            ("审核状态", self.report.review_status.value),
        ]
        
        for label, value in info_data:
            row_frame = ttk.Frame(info_frame)
            row_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row_frame, text=f"{label}:", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=str(value), font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # 评分信息
        score_frame = ttk.LabelFrame(report_frame, text="评分信息", padding=10)
        score_frame.pack(fill=tk.X, padx=10, pady=10)
        
        score_data = [
            ("合规项得分", f"{self.report.compliance_score:.2f}"),
            ("有效项得分", f"{self.report.effectiveness_score:.2f}"),
            ("调节项得分", f"{self.report.adjustment_score:.2f}" if self.report.adjustment_score else "N/A"),
            ("总分", f"{self.report.total_score:.2f}"),
        ]
        
        for label, value in score_data:
            row_frame = ttk.Frame(score_frame)
            row_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row_frame, text=f"{label}:", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=value, font=("Arial", 10, "bold"), foreground="blue").pack(side=tk.LEFT, padx=10)
        
        # 晋级信息
        if self.report.promotion_eligible or self.report.recommended_level:
            promotion_frame = ttk.LabelFrame(report_frame, text="晋级信息", padding=10)
            promotion_frame.pack(fill=tk.X, padx=10, pady=10)
            
            promotion_data = [
                ("符合晋级条件", "是" if self.report.promotion_eligible else "否"),
                ("推荐晋级级别", self.report.recommended_level or "无"),
                ("晋级原因", self.report.promotion_reason or "无"),
            ]
            
            for label, value in promotion_data:
                row_frame = ttk.Frame(promotion_frame)
                row_frame.pack(fill=tk.X, pady=5)
                ttk.Label(row_frame, text=f"{label}:", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
                ttk.Label(row_frame, text=str(value), font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # 审核意见
        if self.report.review_comment:
            comment_frame = ttk.LabelFrame(report_frame, text="审核意见", padding=10)
            comment_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            comment_text = scrolledtext.ScrolledText(comment_frame, height=6, width=80, wrap=tk.WORD)
            comment_text.pack(fill=tk.BOTH, expand=True)
            comment_text.insert(tk.END, self.report.review_comment)
            comment_text.config(state=tk.DISABLED)
    
    def _create_questionnaire_tab(self, notebook):
        """创建原问卷标签页"""
        questionnaire_frame = ttk.Frame(notebook)
        notebook.add(questionnaire_frame, text="查看原问卷")
        
        if not self.questionnaire:
            ttk.Label(questionnaire_frame, text="问卷数据不存在", font=("Arial", 12)).pack(pady=20)
            return
        
        # 问卷基本信息
        info_frame = ttk.LabelFrame(questionnaire_frame, text="问卷信息", padding=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_data = [
            ("问卷ID", self.questionnaire.questionnaire_id),
            ("用户类型", self.questionnaire.user_type),
            ("用户级别", self.questionnaire.user_level),
            ("提交时间", self.questionnaire.submission_time.strftime("%Y-%m-%d %H:%M:%S")),
            ("总分", f"{self.questionnaire.total_score:.2f}" if self.questionnaire.total_score else "N/A"),
        ]
        
        for label, value in info_data:
            row_frame = ttk.Frame(info_frame)
            row_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row_frame, text=f"{label}:", width=15, font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            ttk.Label(row_frame, text=str(value), font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        # 问卷答案
        answers_frame = ttk.LabelFrame(questionnaire_frame, text="答案详情", padding=10)
        answers_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建树形视图显示答案
        tree = ttk.Treeview(
            answers_frame,
            columns=("question_type", "answer", "score", "comment"),
            height=15,
            show="tree headings"
        )
        
        tree.column("#0", width=300, heading="问题")
        tree.column("question_type", width=100, heading="题目类型")
        tree.column("answer", width=150, heading="答案")
        tree.column("score", width=80, heading="得分")
        tree.column("comment", width=150, heading="备注")
        
        # 添加答案数据
        for i, answer in enumerate(self.questionnaire.answers):
            tree.insert(
                "",
                "end",
                text=answer.question_text,
                values=(
                    answer.question_type,
                    answer.answer,
                    f"{answer.score:.2f}" if answer.score else "N/A",
                    answer.comment or ""
                )
            )
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(answers_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.config(yscrollcommand=scrollbar.set)
    
    def _create_review_tab(self, notebook):
        """创建审核操作标签页"""
        review_frame = ttk.Frame(notebook)
        notebook.add(review_frame, text="审核操作")
        
        # 审核意见输入
        comment_label = ttk.Label(review_frame, text="审核意见:", font=("Arial", 10, "bold"))
        comment_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        comment_text = scrolledtext.ScrolledText(review_frame, height=8, width=80, wrap=tk.WORD)
        comment_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(review_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def approve_review():
            """批准审核"""
            comment = comment_text.get("1.0", tk.END).strip()
            reviewer_id = "reviewer_001"  # 应该从当前用户获取
            reviewer_name = "审核员"  # 应该从当前用户获取
            
            success, message, report = review_service.approve_review(
                self.report_id,
                reviewer_id,
                reviewer_name,
                comment,
                user_type='enterprise'
            )
            
            if success:
                messagebox.showinfo("成功", message)
                if self.on_review_callback:
                    self.on_review_callback()
                self.window.destroy()
            else:
                messagebox.showerror("失败", message)
        
        def reject_review():
            """驳回审核"""
            comment = comment_text.get("1.0", tk.END).strip()
            if not comment:
                messagebox.showwarning("警告", "驳回时必须填写意见")
                return
            
            reviewer_id = "reviewer_001"
            reviewer_name = "审核员"
            
            success, message, report = review_service.reject_review(
                self.report_id,
                reviewer_id,
                reviewer_name,
                comment,
                user_type='enterprise'
            )
            
            if success:
                messagebox.showinfo("成功", message)
                if self.on_review_callback:
                    self.on_review_callback()
                self.window.destroy()
            else:
                messagebox.showerror("失败", message)
        
        ttk.Button(button_frame, text="✓ 批准", command=approve_review).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✗ 驳回", command=reject_review).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _create_promotion_tab(self, notebook):
        """创建晋级操作标签页"""
        promotion_frame = ttk.Frame(notebook)
        notebook.add(promotion_frame, text="手动晋级")
        
        # 晋级资格检查
        eligibility_frame = ttk.LabelFrame(promotion_frame, text="晋级资格", padding=10)
        eligibility_frame.pack(fill=tk.X, padx=10, pady=10)
        
        eligibility_text = f"""
当前级别: {self.report.current_level}
总分: {self.report.total_score:.2f}
符合晋级条件: {'是' if self.report.promotion_eligible else '否'}
推荐晋级级别: {self.report.recommended_level or '无'}
        """
        
        ttk.Label(eligibility_frame, text=eligibility_text, font=("Arial", 10), justify=tk.LEFT).pack(anchor=tk.W)
        
        # 晋级原因输入
        reason_label = ttk.Label(promotion_frame, text="晋级原因:", font=("Arial", 10, "bold"))
        reason_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        reason_text = scrolledtext.ScrolledText(promotion_frame, height=6, width=80, wrap=tk.WORD)
        reason_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(promotion_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def promote_user():
            """手动晋级用户"""
            reason = reason_text.get("1.0", tk.END).strip()
            if not reason:
                messagebox.showwarning("警告", "请填写晋级原因")
                return
            
            reviewer_id = "reviewer_001"
            reviewer_name = "审核员"
            
            success, message, promotion_record = review_service.promote_user(
                self.report_id,
                reviewer_id,
                reviewer_name,
                reason,
                user_type='enterprise'
            )
            
            if success:
                messagebox.showinfo("成功", message)
                if self.on_review_callback:
                    self.on_review_callback()
                self.window.destroy()
            else:
                messagebox.showerror("失败", message)
        
        ttk.Button(button_frame, text="确认晋级", command=promote_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side=tk.LEFT, padx=5)


class ReviewListWindow:
    """审核列表窗口"""
    
    def __init__(self, parent):
        """初始化审核列表窗口"""
        self.parent = parent
        
        self.window = tk.Toplevel(parent)
        self.window.title("审核管理")
        self.window.geometry("1200x600")
        self.window.resizable(True, True)
        
        self._create_ui()
        self._load_data()
    
    def _create_ui(self):
        """创建UI界面"""
        # 工具栏
        toolbar = ttk.Frame(self.window)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(toolbar, text="筛选状态:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar(value="pending")
        status_combo = ttk.Combobox(
            toolbar,
            textvariable=self.status_var,
            values=["pending", "approved", "rejected", "promoted", "all"],
            state="readonly",
            width=15
        )
        status_combo.pack(side=tk.LEFT, padx=5)
        status_combo.bind("<<ComboboxSelected>>", lambda e: self._load_data())
        
        ttk.Button(toolbar, text="刷新", command=self._load_data).pack(side=tk.LEFT, padx=5)
        
        # 列表框架
        list_frame = ttk.Frame(self.window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建树形视图
        self.tree = ttk.Treeview(
            list_frame,
            columns=("enterprise", "level", "score", "status", "reviewer", "review_time"),
            height=20,
            show="tree headings"
        )
        
        self.tree.column("#0", width=50, heading="ID")
        self.tree.column("enterprise", width=200, heading="企业名称")
        self.tree.column("level", width=100, heading="当前级别")
        self.tree.column("score", width=80, heading="总分")
        self.tree.column("status", width=100, heading="状态")
        self.tree.column("reviewer", width=100, heading="审核员")
        self.tree.column("review_time", width=150, heading="审核时间")
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 绑定双击事件
        self.tree.bind("<Double-1>", self._on_item_double_click)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
    
    def _load_data(self):
        """加载数据"""
        # 清空树形视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 获取数据
        status_filter = self.status_var.get()
        
        if status_filter == "all":
            reports = list(review_service.reports.values())
        else:
            status_enum = ReviewStatus[status_filter.upper()]
            reports = review_service.get_reports_by_status(status_enum)
        
        # 添加数据到树形视图
        for report in reports:
            self.tree.insert(
                "",
                "end",
                text=report.report_id[:8],
                values=(
                    report.enterprise_name,
                    report.current_level,
                    f"{report.total_score:.2f}",
                    report.review_status.value,
                    report.reviewer_name or "未审核",
                    report.review_time.strftime("%Y-%m-%d %H:%M") if report.review_time else "未审核"
                )
            )
    
    def _on_item_double_click(self, event):
        """处理双击事件"""
        item = self.tree.selection()[0]
        report_id = self.tree.item(item, "text")
        
        # 查找完整的report_id
        for rid, report in review_service.reports.items():
            if rid.startswith(report_id):
                ReviewDetailWindow(self.window, rid, self._load_data)
                break


class ReviewDashboard:
    """审核仪表板"""
    
    def __init__(self, parent):
        """初始化审核仪表板"""
        self.parent = parent
        
        self.window = tk.Toplevel(parent)
        self.window.title("审核仪表板")
        self.window.geometry("800x500")
        self.window.resizable(True, True)
        
        self._create_ui()
        self._load_data()
    
    def _create_ui(self):
        """创建UI界面"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 统计信息框架
        stats_frame = ttk.LabelFrame(main_frame, text="审核统计", padding=10)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_labels = {}
        stats_items = [
            ("total_reports", "总报告数"),
            ("pending", "待审核"),
            ("approved", "已批准"),
            ("rejected", "已驳回"),
            ("promoted", "已晋级"),
            ("approval_rate", "批准率"),
            ("promotion_rate", "晋级率"),
        ]
        
        for i, (key, label) in enumerate(stats_items):
            row = i // 3
            col = i % 3
            
            frame = ttk.Frame(stats_frame)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky=tk.W)
            
            ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
            value_label = ttk.Label(frame, text="0", font=("Arial", 14, "bold"), foreground="blue")
            value_label.pack(anchor=tk.W)
            
            self.stats_labels[key] = value_label
        
        # 平均评分框架
        score_frame = ttk.LabelFrame(main_frame, text="平均评分", padding=10)
        score_frame.pack(fill=tk.X, pady=10)
        
        self.score_labels = {}
        score_items = [
            ("avg_compliance_score", "平均合规项得分"),
            ("avg_effectiveness_score", "平均有效项得分"),
            ("avg_total_score", "平均总分"),
        ]
        
        for key, label in score_items:
            frame = ttk.Frame(score_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold"), width=20).pack(side=tk.LEFT)
            value_label = ttk.Label(frame, text="0.00", font=("Arial", 12, "bold"), foreground="green")
            value_label.pack(side=tk.LEFT, padx=10)
            
            self.score_labels[key] = value_label
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="查看审核列表", command=self._open_review_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self._load_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭", command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def _load_data(self):
        """加载数据"""
        # 获取统计信息
        stats = review_service.get_review_statistics()
        for key, value in stats.items():
            if key in self.stats_labels:
                if isinstance(value, float):
                    self.stats_labels[key].config(text=f"{value:.2%}")
                else:
                    self.stats_labels[key].config(text=str(value))
        
        # 获取平均评分
        scores = review_service.get_average_scores()
        for key, value in scores.items():
            if key in self.score_labels:
                self.score_labels[key].config(text=f"{value:.2f}")
    
    def _open_review_list(self):
        """打开审核列表"""
        ReviewListWindow(self.window)


# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    root.title("审核功能演示")
    root.geometry("400x300")
    
    def open_dashboard():
        ReviewDashboard(root)
    
    def open_review_list():
        ReviewListWindow(root)
    
    ttk.Button(root, text="打开审核仪表板", command=open_dashboard).pack(pady=10)
    ttk.Button(root, text="打开审核列表", command=open_review_list).pack(pady=10)
    ttk.Button(root, text="退出", command=root.quit).pack(pady=10)
    
    root.mainloop()

