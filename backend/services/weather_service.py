# backend/services/weather_service.py
"""
天气服务模块 - 支持 API 模式和 iframe 嵌入模式
"""
import requests
import json
import re


def fetch_weather_data(card):
    """
    获取天气数据
    支持两种模式:
    1. api 模式: 使用 OpenWeatherMap API
    2. iframe 模式: 从 iframe URL 提取城市信息，使用 OpenWeatherMap API 展示
    """
    api_url = card.get('api_url', '')
    api_key = card.get('api_key', '')
    display_config = card.get('display_config', {})
    
    if isinstance(display_config, str):
        try:
            display_config = json.loads(display_config)
        except:
            display_config = {}
    
    mode = display_config.get('mode', 'iframe')
    
    # iframe 模式 - 从 URL 提取城市，使用 OpenWeatherMap API
    if mode == 'iframe':
        return handle_iframe_mode(api_url, display_config)
    
    # API 模式
    return handle_api_mode(api_url, api_key, display_config)


# backend/services/weather_service.py

def handle_iframe_mode(api_url, display_config):
    """
    处理 iframe 模式：直接返回用户提供的 iframe 代码，不做任何解析
    """
    # 直接返回 iframe 模式数据，保留原始代码
    return {
        'mode': 'iframe',
        'raw_code': api_url,  # 这里保存用户粘贴的完整 iframe HTML 代码
        'iframe_src': '',     # 不再提取 src
        'height': display_config.get('height', 150),
        'width': display_config.get('width', '100%')
    }

def extract_city_from_url(url):
    """
    从 iframe URL 中提取城市名称
    支持的格式:
    - https://i.tianqi.com?c=code&id=48&py=ningbo
    - https://i.tianqi.com?c=code&id=48&py=beijing
    - 其他天气网站的 URL
    """
    if not url:
        return None
    
    # 尝试从 URL 中提取 py=xxx 参数（天气网格式）
    match = re.search(r'[?&]py=([^&]+)', url)
    if match:
        city = match.group(1)
        # 转换拼音为中文（简化映射）
        city_map = {
            'beijing': '北京', 'shanghai': '上海', 'guangzhou': '广州', 
            'shenzhen': '深圳', 'ningbo': '宁波', 'hangzhou': '杭州',
            'chengdu': '成都', 'wuhan': '武汉', 'nanjing': '南京',
            'chongqing': '重庆', 'xian': '西安', 'tianjin': '天津',
            'suzhou': '苏州', 'dalian': '大连', 'qingdao': '青岛',
            'changsha': '长沙', 'zhengzhou': '郑州', 'shenyang': '沈阳'
        }
        return city_map.get(city.lower(), city.capitalize())
    
    # 尝试从 URL 中提取其他格式的城市名
    match = re.search(r'[?&]city=([^&]+)', url)
    if match:
        return match.group(1)
    
    return None


def fetch_weather_from_api(city, api_key):
    """
    从 OpenWeatherMap API 获取天气数据
    """
    if not city:
        return {'error': '无法从 iframe URL 中识别城市，请检查配置'}
    
    if not api_key:
        return {'error': '请配置 OpenWeatherMap API Key'}
    
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'zh_cn'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'mode': 'api',
                'city': data.get('name', city),
                'temperature': data.get('main', {}).get('temp'),
                'humidity': data.get('main', {}).get('humidity'),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'icon': data.get('weather', [{}])[0].get('icon', '')
            }
        else:
            return {'error': f'获取天气数据失败: HTTP {response.status_code}'}
            
    except Exception as e:
        return {'error': f'获取天气数据失败: {str(e)}'}


def handle_api_mode(api_url, api_key, display_config):
    """处理 OpenWeatherMap API 模式"""
    if not api_key:
        return {'error': '请配置 OpenWeatherMap API Key'}
    
    city = display_config.get('city', 'Beijing')
    
    if not api_url:
        api_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'zh_cn'
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'mode': 'api',
                'city': data.get('name', city),
                'temperature': data.get('main', {}).get('temp'),
                'humidity': data.get('main', {}).get('humidity'),
                'description': data.get('weather', [{}])[0].get('description', ''),
                'icon': data.get('weather', [{}])[0].get('icon', '')
            }
        else:
            return {'error': f'天气 API 请求失败: HTTP {response.status_code}'}
            
    except requests.exceptions.ConnectionError:
        return {'error': '无法连接到天气服务器'}
    except requests.exceptions.Timeout:
        return {'error': '请求天气数据超时'}
    except Exception as e:
        return {'error': f'获取天气数据失败: {str(e)}'}