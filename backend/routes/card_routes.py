# backend/routes/card_routes.py
"""
首页卡片管理路由
"""
import json
from flask import request, jsonify
from . import card_bp
from utils.db_utils import get_db, ensure_db
from services.card_service import fetch_card_data


@card_bp.route('/home/cards', methods=['GET'])
def get_home_cards():
    """获取所有卡片配置"""
    ensure_db()
    conn = get_db()
    cards = conn.execute(
        "SELECT * FROM home_cards ORDER BY sort_order ASC"
    ).fetchall()
    conn.close()
    
    result = []
    for card in cards:
        card_dict = dict(card)
        # 解析 display_config
        if card_dict.get('display_config'):
            try:
                card_dict['display_config'] = json.loads(card_dict['display_config'])
            except:
                card_dict['display_config'] = {}
        else:
            card_dict['display_config'] = {}
        result.append(card_dict)
    
    return jsonify(result)


@card_bp.route('/home/cards/data', methods=['GET'])
def get_home_cards_data():
    """获取所有卡片数据（含实时数据）"""
    ensure_db()
    conn = get_db()
    cards = conn.execute(
        "SELECT * FROM home_cards WHERE enabled = 1 ORDER BY sort_order ASC"
    ).fetchall()
    conn.close()
    
    result = []
    for card in cards:
        # 转换为字典
        card_dict = dict(card)
        
        # 解析 display_config
        if card_dict.get('display_config'):
            try:
                card_dict['display_config'] = json.loads(card_dict['display_config'])
            except:
                card_dict['display_config'] = {}
        else:
            card_dict['display_config'] = {}
        
        # 打印调试信息
        print(f"[调试] 处理卡片: {card_dict.get('title')} (类型: {card_dict.get('card_type')})")
        print(f"[调试] api_url: {card_dict.get('api_url')}")
        print(f"[调试] api_key: {card_dict.get('api_key')[:10] if card_dict.get('api_key') else 'None'}...")
        
        # 使用服务层获取数据
        try:
            card_dict['data'] = fetch_card_data(card_dict)
            print(f"[调试] 数据获取成功: {card_dict.get('card_type')}")
        except Exception as e:
            print(f"[调试] 数据获取失败: {e}")
            card_dict['data'] = {'error': f'获取数据失败: {str(e)}'}
        
        result.append(card_dict)
    
    return jsonify(result)


@card_bp.route('/home/cards', methods=['POST'])
def add_home_card():
    """添加新卡片"""
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


@card_bp.route('/home/cards/<int:card_id>', methods=['PUT'])
def update_home_card(card_id):
    """更新卡片"""
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


@card_bp.route('/home/cards/<int:card_id>', methods=['DELETE'])
def delete_home_card(card_id):
    """删除卡片"""
    ensure_db()
    conn = get_db()
    conn.execute("DELETE FROM home_cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@card_bp.route('/home/cards/<int:card_id>/toggle', methods=['POST'])
def toggle_home_card(card_id):
    """切换卡片启用状态"""
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