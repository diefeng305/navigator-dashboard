# backend/routes/icon_routes.py
"""
图标管理路由
"""
import os
import uuid
from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import icon_bp
from utils.db_utils import get_db, ensure_db

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../frontend/assets/icons')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'ico'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@icon_bp.route('/icons/upload', methods=['POST'])
def upload_icon():
    """上传图标文件"""
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


@icon_bp.route('/icons', methods=['GET'])
def list_icons():
    """获取所有图标列表"""
    ensure_db()
    conn = get_db()
    icons = conn.execute(
        "SELECT id, filename, original_name, path, file_size, upload_time FROM local_icons ORDER BY upload_time DESC"
    ).fetchall()
    conn.close()
    
    # 扫描文件系统，同步未入库的文件
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


@icon_bp.route('/icons/delete/<int:icon_id>', methods=['DELETE'])
def delete_icon(icon_id):
    """删除图标"""
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