# -*- coding: utf-8 -*-
"""
文件上传处理模块
处理问卷附件的上传、存储和管理
"""
import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

# 允许的文件类型
ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'jpg', 'jpeg', 'png', 'gif', 'bmp',
    'txt', 'csv', 'zip', 'rar', '7z'
}

# 最大文件大小（100MB）
MAX_FILE_SIZE = 100 * 1024 * 1024


class FileUploadHandler:
    """文件上传处理器"""

    def __init__(self, upload_base_dir='storage/questionnaire_uploads'):
        """
        初始化上传处理器
        
        Args:
            upload_base_dir: 上传文件的基础目录
        """
        self.upload_base_dir = upload_base_dir
        self.ensure_upload_dir()

    def ensure_upload_dir(self):
        """确保上传目录存在"""
        os.makedirs(self.upload_base_dir, exist_ok=True)

    def allowed_file(self, filename):
        """检查文件类型是否允许"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def get_file_size(self, file_obj):
        """获取文件大小"""
        try:
            file_obj.seek(0, os.SEEK_END)
            size = file_obj.tell()
            file_obj.seek(0)
            return size
        except Exception as e:
            logger.error(f"获取文件大小失败: {e}")
            return 0

    def validate_file(self, file_obj, filename):
        """
        验证文件
        
        Args:
            file_obj: 文件对象
            filename: 文件名
            
        Returns:
            (是否有效, 错误信息)
        """
        # 检查文件名
        if not filename:
            return False, "文件名不能为空"

        # 检查文件类型
        if not self.allowed_file(filename):
            return False, f"不支持的文件类型: {filename.rsplit('.', 1)[1].upper()}"

        # 检查文件大小
        file_size = self.get_file_size(file_obj)
        if file_size == 0:
            return False, "文件为空"
        if file_size > MAX_FILE_SIZE:
            return False, f"文件过大，最大允许 {MAX_FILE_SIZE / 1024 / 1024:.0f}MB"

        return True, None

    def save_file(self, file_obj, submission_id, question_id, filename=None):
        """
        保存上传的文件
        
        Args:
            file_obj: 文件对象
            submission_id: 问卷提交ID
            question_id: 问题ID
            filename: 文件名（可选，如不提供则使用原文件名）
            
        Returns:
            (是否成功, 文件信息或错误信息)
        """
        try:
            # 获取原始文件名
            original_filename = file_obj.filename or filename
            if not original_filename:
                return False, "无法获取文件名"

            # 验证文件
            is_valid, error_msg = self.validate_file(file_obj, original_filename)
            if not is_valid:
                return False, error_msg

            # 创建提交目录
            submission_dir = os.path.join(self.upload_base_dir, submission_id)
            os.makedirs(submission_dir, exist_ok=True)

            # 生成安全的文件名
            file_ext = original_filename.rsplit('.', 1)[1].lower()
            safe_filename = f"{question_id}_{uuid.uuid4().hex[:8]}.{file_ext}"
            file_path = os.path.join(submission_dir, safe_filename)

            # 保存文件
            file_obj.seek(0)
            file_obj.save(file_path)

            # 获取文件信息
            file_size = os.path.getsize(file_path)
            file_info = {
                'id': str(uuid.uuid4()),
                'submission_id': submission_id,
                'question_id': question_id,
                'original_name': original_filename,
                'saved_name': safe_filename,
                'file_path': file_path,
                'file_size': file_size,
                'file_type': file_ext,
                'upload_time': datetime.now().isoformat(),
                'status': 'uploaded'
            }

            logger.info(f"文件保存成功: {file_path}")
            return True, file_info

        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return False, f"保存文件失败: {str(e)}"

    def delete_file(self, file_path):
        """
        删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"文件已删除: {file_path}")
                return True
            else:
                logger.warning(f"文件不存在: {file_path}")
                return False
        except Exception as e:
            logger.error(f"删除文件失败: {e}")
            return False

    def get_file(self, file_path):
        """
        获取文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容或None
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return f.read()
            else:
                logger.warning(f"文件不存在: {file_path}")
                return None
        except Exception as e:
            logger.error(f"读取文件失败: {e}")
            return None

    def list_submission_files(self, submission_id):
        """
        列出提交的所有文件
        
        Args:
            submission_id: 问卷提交ID
            
        Returns:
            文件列表
        """
        try:
            submission_dir = os.path.join(self.upload_base_dir, submission_id)
            files = []

            if os.path.exists(submission_dir):
                for filename in os.listdir(submission_dir):
                    file_path = os.path.join(submission_dir, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        files.append({
                            'name': filename,
                            'path': file_path,
                            'size': file_size,
                            'modified_time': datetime.fromtimestamp(
                                os.path.getmtime(file_path)
                            ).isoformat()
                        })

            return files
        except Exception as e:
            logger.error(f"列出文件失败: {e}")
            return []

    def cleanup_old_files(self, days=30):
        """
        清理旧文件（超过指定天数）
        
        Args:
            days: 天数
            
        Returns:
            清理的文件数
        """
        try:
            import time
            cutoff_time = time.time() - (days * 24 * 60 * 60)
            cleaned_count = 0

            for submission_id in os.listdir(self.upload_base_dir):
                submission_dir = os.path.join(self.upload_base_dir, submission_id)
                if not os.path.isdir(submission_dir):
                    continue

                for filename in os.listdir(submission_dir):
                    file_path = os.path.join(submission_dir, filename)
                    if os.path.isfile(file_path):
                        if os.path.getmtime(file_path) < cutoff_time:
                            os.remove(file_path)
                            cleaned_count += 1
                            logger.info(f"已删除旧文件: {file_path}")

            return cleaned_count
        except Exception as e:
            logger.error(f"清理旧文件失败: {e}")
            return 0

    def get_submission_storage_info(self, submission_id):
        """
        获取提交的存储信息
        
        Args:
            submission_id: 问卷提交ID
            
        Returns:
            存储信息字典
        """
        try:
            submission_dir = os.path.join(self.upload_base_dir, submission_id)
            files = self.list_submission_files(submission_id)
            
            total_size = sum(f['size'] for f in files)
            
            return {
                'submission_id': submission_id,
                'directory': submission_dir,
                'file_count': len(files),
                'total_size': total_size,
                'total_size_mb': total_size / 1024 / 1024,
                'files': files
            }
        except Exception as e:
            logger.error(f"获取存储信息失败: {e}")
            return None


# 使用示例
if __name__ == '__main__':
    handler = FileUploadHandler()
    
    # 测试文件验证
    print("允许的文件类型:", ALLOWED_EXTENSIONS)
    print("最大文件大小:", MAX_FILE_SIZE / 1024 / 1024, "MB")
    
    # 测试文件列表
    submission_id = "test-submission-001"
    files = handler.list_submission_files(submission_id)
    print(f"提交 {submission_id} 的文件数: {len(files)}")

