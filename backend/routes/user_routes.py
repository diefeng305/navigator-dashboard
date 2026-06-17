# backend/routes/user_routes.py
"""
用户管理路由
"""
import sqlite3
from flask import request, jsonify
from . import user_bp
from utils.db_utils import get_db, ensure_db


@user_bp.route('/users', methods=['GET'])
def get_users():
    """获取用户列表（排除管理员）"""
    ensure_db()
    conn = get_db()
    users = conn.execute(
        "SELECT id, username, role FROM users WHERE username != 'admin'"
    ).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])


@user_bp.route('/users/add', methods=['POST'])
def add_user():
    """添加新用户"""
    ensure_db()
    data = request.json
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (data['username'], data['password'], data['role'])
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': '用户名已存在'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@user_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """删除用户（不能删除管理员）"""
    ensure_db()
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ? AND username != 'admin'", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@user_bp.route('/users/change-password', methods=['POST'])
def change_password():
    """修改用户密码"""
    ensure_db()
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, old_password)
    ).fetchone()
    
    if user:
        conn.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (new_password, username)
        )
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    conn.close()
    return jsonify({'success': False, 'message': '原密码错误'})