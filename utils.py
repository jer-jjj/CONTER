# -*- coding: utf-8 -*-
"""
Utility functions
"""
import os
import sys
from typing import Optional


def get_app_data_dir() -> str:
    """
    Get application data directory
    Returns the directory where the executable is located, or the script directory if running in dev mode
    """
    # 判断是否为打包后的可执行文件
    if getattr(sys, 'frozen', False):
        # 打包后：使用可执行文件所在目录
        app_dir = os.path.dirname(sys.executable)
    else:
        # 开发模式：使用脚本所在目录
        app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 在应用目录下创建 data 子目录
    data_dir = os.path.join(app_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir


def format_datetime(dt) -> str:
    """Format datetime"""
    if dt is None:
        return 'Not picked'
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def validate_excel_file(file_path: str) -> bool:
    """Validate Excel file"""
    if not os.path.exists(file_path):
        return False
    
    ext = os.path.splitext(file_path)[1].lower()
    return ext in ['.xlsx', '.xls']
