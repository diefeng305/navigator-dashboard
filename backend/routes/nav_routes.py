# backend/routes/nav_routes.py
"""
导航菜单路由
"""
from flask import request, jsonify
from . import nav_bp
from utils.db_utils import get_db, ensure_db

# 角色权重
ROLE_WEIGHTS = {'visitor': 0, 'user': 1, 'special': 2, 'admin': 3}


@nav_bp.route('/navigation', methods=['GET'])
def get_navigation():
    """获取导航菜单（根据用户角色过滤）"""
    ensure_db()
    current_role = request.args.get('role', 'visitor')
    user_weight = ROLE_WEIGHTS.get(current_role, 0)
    
    conn = get_db()
    all_items = conn.execute(
        "SELECT * FROM nav_items ORDER BY parent_id, sort_order ASC"
    ).fetchall()
    conn.close()
    
    accessible_items = []
    for item in all_items:
        item_dict = dict(item)
        required_weight = ROLE_WEIGHTS.get(item_dict.get('min_role_required', 'visitor'), 0)
        if current_role == 'admin' or user_weight >= required_weight:
            accessible_items.append(item_dict)
    
    return jsonify(accessible_items)


@nav_bp.route('/navigation/add', methods=['POST'])
def add_nav_item():
    """添加导航条目"""
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


@nav_bp.route('/navigation/update/<int:item_id>', methods=['POST'])
def update_nav_item(item_id):
    """更新导航条目"""
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


@nav_bp.route('/navigation/delete/<int:item_id>', methods=['POST'])
def delete_nav_item(item_id):
    """删除导航条目（子条目移至根级）"""
    ensure_db()
    conn = get_db()
    conn.execute("UPDATE nav_items SET parent_id = 0 WHERE parent_id = ?", (item_id,))
    conn.execute("DELETE FROM nav_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})