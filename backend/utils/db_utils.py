# backend/utils/db_utils.py
"""
数据库工具函数
"""
import sqlite3
import os
import threading

DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/navigator.db')
_db_initialized = False
_db_lock = threading.Lock()


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def ensure_db():
    """确保数据库已初始化"""
    global _db_initialized
    if not _db_initialized:
        with _db_lock:
            if not _db_initialized:
                from models import init_db
                init_db()
                _db_initialized = True


def init_db_if_needed():
    """别名，兼容性"""
    return ensure_db()


def execute_query(sql, params=None, fetch_one=False, fetch_all=False):
    """执行查询并返回结果"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
            conn.commit()
        
        return result
    finally:
        conn.close()


def execute_many(sql, params_list):
    """批量执行"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.executemany(sql, params_list)
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()