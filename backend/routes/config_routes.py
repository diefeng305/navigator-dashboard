# backend/routes/config_routes.py
"""
系统配置路由
"""
from flask import request, jsonify
from . import config_bp
from utils.db_utils import get_db, ensure_db


@config_bp.route('/config/update', methods=['POST'])
def update_config():
    """更新系统配置"""
    ensure_db()
    data = request.json
    conn = get_db()
    
    if 'sidebar_title' in data:
        conn.execute(
            "INSERT OR REPLACE INTO system_config (key, value) VALUES ('sidebar_title', ?)",
            (data['sidebar_title'],)
        )
    if 'sidebar_letter' in data:
        conn.execute(
            "INSERT OR REPLACE INTO system_config (key, value) VALUES ('sidebar_letter', ?)",
            (data['sidebar_letter'],)
        )
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@config_bp.route('/config', methods=['GET'])
def get_config():
    """获取系统配置"""
    ensure_db()
    conn = get_db()
    configs = conn.execute("SELECT * FROM system_config").fetchall()
    conn.close()
    
    cfg_map = {row['key']: row['value'] for row in configs}
    
    # 设置默认值
    if 'sidebar_title' not in cfg_map:
        cfg_map['sidebar_title'] = '飞牛私有云'
    if 'sidebar_letter' not in cfg_map:
        cfg_map['sidebar_letter'] = 'O'
    
    return jsonify(cfg_map)


@config_bp.route('/home/page-config', methods=['GET'])
def get_page_config():
    """获取首页页面配置"""
    ensure_db()
    conn = get_db()
    show_welcome = conn.execute("SELECT value FROM system_config WHERE key = 'show_welcome'").fetchone()
    show_datetime = conn.execute("SELECT value FROM system_config WHERE key = 'show_datetime'").fetchone()
    custom_welcome = conn.execute("SELECT value FROM system_config WHERE key = 'custom_welcome'").fetchone()
    conn.close()
    
    return jsonify({
        'show_welcome': show_welcome['value'] == 'true' if show_welcome else True,
        'show_datetime': show_datetime['value'] == 'true' if show_datetime else True,
        'custom_welcome': custom_welcome['value'] if custom_welcome else ''
    })


@config_bp.route('/home/page-config', methods=['POST'])
def update_page_config():
    """更新首页页面配置"""
    ensure_db()
    data = request.json
    conn = get_db()
    
    if 'show_welcome' in data:
        conn.execute(
            "INSERT OR REPLACE INTO system_config (key, value) VALUES ('show_welcome', ?)",
            ('true' if data['show_welcome'] else 'false',)
        )
    if 'show_datetime' in data:
        conn.execute(
            "INSERT OR REPLACE INTO system_config (key, value) VALUES ('show_datetime', ?)",
            ('true' if data['show_datetime'] else 'false',)
        )
    if 'custom_welcome' in data:
        conn.execute(
            "INSERT OR REPLACE INTO system_config (key, value) VALUES ('custom_welcome', ?)",
            (data['custom_welcome'],)
        )
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})