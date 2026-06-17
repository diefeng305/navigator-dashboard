# backend/app.py
"""
导航页主应用
"""
from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os
import uuid
import json
import time
import requests
from models import init_db

# 导入服务
from services.card_service import fetch_card_data

app = Flask(__name__, static_folder='../frontend', static_url_path='')
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/navigator.db')

# 图标上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../frontend/assets/icons')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'ico'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

_db_initialized = False
def ensure_db():
    global _db_initialized
    if not _db_initialized:
        init_db()
        _db_initialized = True

# ========== 用户认证 ==========
@app.route('/api/login', methods=['POST'])
def api_login():
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

# ========== 导航菜单管理 ==========
@app.route('/api/navigation', methods=['GET'])
def get_navigation():
    ensure_db()
    current_role = request.args.get('role', 'visitor')
    role_weights = {'visitor': 0, 'user': 1, 'special': 2, 'admin': 3}
    user_weight = role_weights.get(current_role, 0)
    
    conn = get_db()
    all_items = conn.execute(
        "SELECT * FROM nav_items ORDER BY parent_id, sort_order ASC"
    ).fetchall()
    conn.close()
    
    accessible_items = []
    for item in all_items:
        item_dict = dict(item)
        required_weight = role_weights.get(item_dict.get('min_role_required', 'visitor'), 0)
        if current_role == 'admin' or user_weight >= required_weight:
            accessible_items.append(item_dict)
    return jsonify(accessible_items)

@app.route('/api/navigation/add', methods=['POST'])
def add_item():
    ensure_db()
    data = request.json
    conn = get_db()
    conn.execute(
        """INSERT INTO nav_items 
           (title, url, icon, parent_id, sort_order, min_role_required, open_type) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data['title'], data.get('url', ''), data.get('icon', ''), 
         data.get('parent_id', 0), data.get('sort_order', 0), 
         data.get('min_role_required', 'visitor'), data.get('open_type', 'iframe'))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/navigation/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    ensure_db()
    data = request.json
    conn = get_db()
    conn.execute(
        """UPDATE nav_items SET 
           title=?, url=?, icon=?, parent_id=?, sort_order=?, min_role_required=?, open_type=? 
           WHERE id=?""",
        (data['title'], data.get('url', ''), data.get('icon', ''), 
         data.get('parent_id', 0), data.get('sort_order', 0), 
         data.get('min_role_required', 'visitor'), data.get('open_type', 'iframe'), item_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/navigation/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    ensure_db()
    conn = get_db()
    conn.execute("UPDATE nav_items SET parent_id = 0 WHERE parent_id = ?", (item_id,))
    conn.execute("DELETE FROM nav_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ========== 用户管理 ==========
@app.route('/api/users', methods=['GET'])
def get_users():
    ensure_db()
    conn = get_db()
    users = conn.execute(
        "SELECT id, username, role FROM users WHERE username != 'admin'"
    ).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])

@app.route('/api/users/add', methods=['POST'])
def add_user():
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

@app.route('/api/users/delete/<int:u_id>', methods=['POST'])
def delete_user(u_id):
    ensure_db()
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ? AND username != 'admin'", (u_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/users/change-password', methods=['POST'])
def change_password():
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

# ========== 系统配置 ==========
@app.route('/api/config/update', methods=['POST'])
def update_config():
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

@app.route('/api/config')
def get_config():
    ensure_db()
    conn = get_db()
    configs = conn.execute("SELECT * FROM system_config").fetchall()
    conn.close()
    cfg_map = {row['key']: row['value'] for row in configs}
    if 'sidebar_title' not in cfg_map:
        cfg_map['sidebar_title'] = '飞牛私有云'
    if 'sidebar_letter' not in cfg_map:
        cfg_map['sidebar_letter'] = 'O'
    return jsonify(cfg_map)

# ========== 图标上传管理 ==========
@app.route('/api/icons/upload', methods=['POST'])
def upload_icon():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'})
    
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        conn = get_db()
        conn.execute(
            "INSERT INTO local_icons (filename, original_name, path, file_size) VALUES (?, ?, ?, ?)",
            (filename, file.filename, f'/assets/icons/{filename}', os.path.getsize(filepath))
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'path': f'/assets/icons/{filename}',
            'filename': filename
        })
    
    return jsonify({'success': False, 'message': '不支持的文件类型'})

@app.route('/api/icons', methods=['GET'])
def list_icons():
    ensure_db()
    conn = get_db()
    icons = conn.execute(
        "SELECT id, filename, original_name, path, file_size, upload_time FROM local_icons ORDER BY upload_time DESC"
    ).fetchall()
    conn.close()
    
    fs_icons = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename):
                conn_check = get_db()
                existing = conn_check.execute("SELECT id FROM local_icons WHERE filename = ?", (filename,)).fetchone()
                conn_check.close()
                if not existing:
                    fs_icons.append({
                        'id': None,
                        'filename': filename,
                        'original_name': filename,
                        'path': f'/assets/icons/{filename}',
                        'file_size': os.path.getsize(os.path.join(UPLOAD_FOLDER, filename)),
                        'upload_time': None
                    })
    
    result = [dict(icon) for icon in icons] + fs_icons
    return jsonify(result)

@app.route('/api/icons/delete/<int:icon_id>', methods=['DELETE'])
def delete_icon(icon_id):
    ensure_db()
    conn = get_db()
    icon = conn.execute("SELECT * FROM local_icons WHERE id = ?", (icon_id,)).fetchone()
    if icon:
        filepath = os.path.join(UPLOAD_FOLDER, icon['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)
        conn.execute("DELETE FROM local_icons WHERE id = ?", (icon_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    conn.close()
    return jsonify({'success': False, 'message': '图标不存在'})

# ========== 首页卡片管理 API ==========
@app.route('/api/home/cards', methods=['GET'])
def get_home_cards():
    ensure_db()
    conn = get_db()
    cards = conn.execute(
        "SELECT * FROM home_cards ORDER BY sort_order ASC"
    ).fetchall()
    conn.close()
    result = []
    for card in cards:
        card_dict = dict(card)
        if card_dict.get('display_config'):
            try:
                card_dict['display_config'] = json.loads(card_dict['display_config'])
            except:
                card_dict['display_config'] = {}
        else:
            card_dict['display_config'] = {}
        result.append(card_dict)
    return jsonify(result)

@app.route('/api/home/cards', methods=['POST'])
def add_home_card():
    ensure_db()
    data = request.json
    display_config = json.dumps(data.get('display_config', {}))
    conn = get_db()
    cursor = conn.execute(
        """INSERT INTO home_cards 
           (title, card_type, api_url, api_key, sort_order, enabled, refresh_interval, display_config) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (data['title'], data['card_type'], data.get('api_url', ''), data.get('api_key', ''),
         data.get('sort_order', 0), data.get('enabled', 1), data.get('refresh_interval', 60), display_config)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': new_id})

@app.route('/api/home/cards/<int:card_id>', methods=['PUT'])
def update_home_card(card_id):
    ensure_db()
    data = request.json
    display_config = json.dumps(data.get('display_config', {}))
    conn = get_db()
    conn.execute(
        """UPDATE home_cards SET 
           title=?, card_type=?, api_url=?, api_key=?, sort_order=?, enabled=?, refresh_interval=?, display_config=?, updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        (data['title'], data['card_type'], data.get('api_url', ''), data.get('api_key', ''),
         data.get('sort_order', 0), data.get('enabled', 1), data.get('refresh_interval', 60), display_config, card_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/home/cards/<int:card_id>', methods=['DELETE'])
def delete_home_card(card_id):
    ensure_db()
    conn = get_db()
    conn.execute("DELETE FROM home_cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/home/cards/<int:card_id>/toggle', methods=['POST'])
def toggle_home_card(card_id):
    ensure_db()
    data = request.json
    conn = get_db()
    conn.execute(
        "UPDATE home_cards SET enabled = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (data.get('enabled', 1), card_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ========== 单个卡片数据 API ==========
@app.route('/api/home/cards/single/<int:card_id>', methods=['GET'])
def get_single_card_data(card_id):
    """获取单个卡片的最新数据"""
    ensure_db()
    conn = get_db()
    card = conn.execute(
        "SELECT * FROM home_cards WHERE id = ? AND enabled = 1",
        (card_id,)
    ).fetchone()
    conn.close()
    
    if not card:
        return jsonify({'error': '卡片不存在'}), 404
    
    card_dict = dict(card)
    if card_dict.get('display_config'):
        try:
            card_dict['display_config'] = json.loads(card_dict['display_config'])
        except:
            card_dict['display_config'] = {}
    else:
        card_dict['display_config'] = {}
    
    card_dict['data'] = fetch_card_data(card_dict)
    
    return jsonify(card_dict)

# ========== 页面配置 API ==========
@app.route('/api/home/page-config', methods=['GET'])
def get_page_config():
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

@app.route('/api/home/page-config', methods=['POST'])
def update_page_config():
    ensure_db()
    data = request.json
    conn = get_db()
    if 'show_welcome' in data:
        conn.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES ('show_welcome', ?)", ('true' if data['show_welcome'] else 'false',))
    if 'show_datetime' in data:
        conn.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES ('show_datetime', ?)", ('true' if data['show_datetime'] else 'false',))
    if 'custom_welcome' in data:
        conn.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES ('custom_welcome', ?)", (data['custom_welcome'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ========== 首页卡片数据 API ==========
@app.route('/api/home/cards/data', methods=['GET'])
def get_home_cards_data():
    ensure_db()
    conn = get_db()
    cards = conn.execute(
        "SELECT * FROM home_cards WHERE enabled = 1 ORDER BY sort_order ASC"
    ).fetchall()
    conn.close()
    
    result = []
    for card in cards:
        card_dict = dict(card)
        if card_dict.get('display_config'):
            try:
                card_dict['display_config'] = json.loads(card_dict['display_config'])
            except:
                card_dict['display_config'] = {}
        else:
            card_dict['display_config'] = {}
        
        try:
            card_dict['data'] = fetch_card_data(card_dict)
        except Exception as e:
            card_dict['data'] = {'component': 'error', 'data': {'error': str(e)}}
        
        result.append(card_dict)
    return jsonify(result)

# ========== 首页配置 API ==========
@app.route('/api/home/config', methods=['GET'])
def get_home_config():
    ensure_db()
    conn = get_db()
    quick_links = conn.execute("SELECT * FROM home_quick_links ORDER BY sort_order ASC").fetchall()
    conn.close()
    return jsonify({'quickLinks': [dict(link) for link in quick_links], 'services': []})

@app.route('/api/system/status', methods=['GET'])
def get_system_status():
    try:
        import psutil
        uptime_hours = int(time.time() - psutil.boot_time()) // 3600
        return jsonify({
            'cpu': {'usage': psutil.cpu_percent(interval=1), 'status': 'normal'},
            'memory': {'usage': psutil.virtual_memory().percent, 'status': 'normal'},
            'disk': {'usage': psutil.disk_usage('/').percent, 'status': 'normal'},
            'uptime': uptime_hours,
            'services': [{'name': '数据库服务', 'status': 'online', 'type': 'database'}, {'name': '后端 API', 'status': 'online', 'type': 'api'}]
        })
    except ImportError:
        return jsonify({
            'cpu': {'usage': 25, 'status': 'normal'},
            'memory': {'usage': 45, 'status': 'normal'},
            'disk': {'usage': 60, 'status': 'normal'},
            'uptime': 24,
            'services': [{'name': '数据库服务', 'status': 'online', 'type': 'database'}, {'name': '后端 API', 'status': 'online', 'type': 'api'}]
        })

# ========== 静态文件服务 ==========
@app.route('/')
def index():
    ensure_db()
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(app.static_folder, 'pages'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

if __name__ == '__main__':
    ensure_db()
    print("=" * 50)
    print("🚀 导航页服务已启动")
    print("📍 访问地址: http://localhost:5000")
    print("🔐 管理员账号: admin / admin123")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)