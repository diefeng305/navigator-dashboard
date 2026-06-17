# backend/routes/auth_routes.py
"""
认证路由 - 登录、登出
"""
from flask import request, jsonify
from . import auth_bp
from utils.db_utils import get_db


@auth_bp.route('/login', methods=['POST'])
def api_login():
    """用户登录"""
    data = request.json or {}
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (data.get('username'), data.get('password'))
    ).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            'success': True,
            'username': user['username'],
            'role': user['role']
        })
    return jsonify({'success': False, 'message': '用户名或密码错误'})


@auth_bp.route('/logout', methods=['POST'])
def api_logout():
    """用户登出（无状态，仅返回成功）"""
    return jsonify({'success': True})