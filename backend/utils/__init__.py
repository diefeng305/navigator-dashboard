# backend/utils/__init__.py
"""
工具函数模块
"""
from .db_utils import get_db, ensure_db, init_db_if_needed

__all__ = [
    'get_db',
    'ensure_db', 
    'init_db_if_needed'
]