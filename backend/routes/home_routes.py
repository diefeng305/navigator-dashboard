# backend/routes/home_routes.py
"""
首页相关路由
"""
from flask import request, jsonify
from . import home_bp
from utils.db_utils import get_db, ensure_db


@home_bp.route('/home/config', methods=['GET'])
def get_home_config():
    """获取首页配置（快捷链接等）"""
    ensure_db()
    conn = get_db()
    quick_links = conn.execute("SELECT * FROM home_quick_links ORDER BY sort_order ASC").fetchall()
    conn.close()
    return jsonify({'quickLinks': [dict(link) for link in quick_links], 'services': []})


@home_bp.route('/system/status', methods=['GET'])
def get_system_status():
    """获取系统运行状态"""
    import time
    try:
        import psutil
        uptime_hours = int(time.time() - psutil.boot_time()) // 3600
        return jsonify({
            'cpu': {'usage': psutil.cpu_percent(interval=1), 'status': 'normal'},
            'memory': {'usage': psutil.virtual_memory().percent, 'status': 'normal'},
            'disk': {'usage': psutil.disk_usage('/').percent, 'status': 'normal'},
            'uptime': uptime_hours,
            'services': [
                {'name': '数据库服务', 'status': 'online', 'type': 'database'},
                {'name': '后端 API', 'status': 'online', 'type': 'api'}
            ]
        })
    except ImportError:
        return jsonify({
            'cpu': {'usage': 25, 'status': 'normal'},
            'memory': {'usage': 45, 'status': 'normal'},
            'disk': {'usage': 60, 'status': 'normal'},
            'uptime': 24,
            'services': [
                {'name': '数据库服务', 'status': 'online', 'type': 'database'},
                {'name': '后端 API', 'status': 'online', 'type': 'api'}
            ]
        })