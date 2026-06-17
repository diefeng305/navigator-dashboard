# backend/services/card_service.py
"""
卡片服务 - 统一调度各类卡片数据获取
"""
import json
from .weather_service import fetch_weather_data
from .emby_service import fetch_emby_data
from .system_service import fetch_system_data, fetch_stats_data
from .zblog_service import fetch_zblog_data

# 卡片类型注册表
CARD_HANDLERS = {
    'weather': fetch_weather_data,
    'emby': fetch_emby_data,
    'system': fetch_system_data,
    'stats': fetch_stats_data,
    'zblog': fetch_zblog_data,
}


def fetch_card_data(card):
    """
    获取卡片数据，并指定前端渲染组件
    
    参数:
        card: 卡片字典，必须包含 card_type 字段
    
    返回:
        {
            'component': 'card_type',  # 组件名称
            'data': {...}              # 卡片数据
        }
    """
    if not card:
        return {'component': 'error', 'data': {'error': '卡片数据为空'}}
    
    card_type = card.get('card_type')
    if not card_type:
        return {'component': 'error', 'data': {'error': '卡片类型未指定'}}
    
    handler = CARD_HANDLERS.get(card_type)
    if not handler:
        return {
            'component': 'error',
            'data': {'error': f'卡片类型 "{card_type}" 暂未支持'}
        }
    
    try:
        data = handler(card)
        if data is None:
            data = {'error': '获取数据返回空'}
        
        # 返回数据时带上组件名称
        return {
            'component': card_type,
            'data': data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'component': 'error',
            'data': {'error': f'获取数据失败: {str(e)}'}
        }


def register_card_handler(card_type, handler_func):
    """
    动态注册新的卡片处理器
    用于后续扩展，不需要修改现有代码
    """
    if not callable(handler_func):
        raise ValueError('handler_func 必须是可调用对象')
    CARD_HANDLERS[card_type] = handler_func
    print(f'[卡片服务] 已注册卡片类型: {card_type}')