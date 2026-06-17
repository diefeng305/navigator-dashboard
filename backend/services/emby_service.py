# backend/services/emby_service.py
"""
Emby/Jellyfin 服务 - 获取最近添加的媒体内容
"""
import requests
import json


def fetch_emby_data(card):
    """
    获取 Emby/Jellyfin 最近添加的媒体内容
    支持从 display_config 中读取 media_type 进行筛选
    """
    # 从卡片中获取配置
    api_url = card.get('api_url', '')
    api_key = card.get('api_key', '')
    display_config = card.get('display_config', {})
    
    # 如果 display_config 是字符串，尝试解析为 JSON
    if isinstance(display_config, str):
        try:
            display_config = json.loads(display_config)
        except:
            display_config = {}
    
    # 验证配置
    if not api_url or not api_key:
        return {'error': '请配置 Emby 服务器地址和 API Key'}
    
    # 清理 URL（移除末尾斜杠）
    api_url = api_url.rstrip('/')
    
    # 获取媒体类型筛选参数（默认为 'all'）
    media_type = display_config.get('media_type', 'all')
    
    # 媒体类型映射
    type_mapping = {
        'all': None,
        'movie': 'Movie',
        'shows': 'Series',
        'tv': 'Series',
        'video': 'Video',
        'music': 'MusicAlbum,MusicArtist,Audio',
        'photo': 'Photo',
        'boxset': 'BoxSet'
    }
    
    include_types = type_mapping.get(media_type)
    limit = display_config.get('limit', 20)
    
    try:
        url = f"{api_url}/Items"
        params = {
            'api_key': api_key,
            'Limit': 50,
            'SortBy': 'DateCreated',
            'SortOrder': 'Descending',
            'Fields': 'ProductionYear,CommunityRating,Overview,DateCreated,PrimaryImageAspectRatio,SeriesName,SeriesId',
            'Recursive': 'true',
            'IsVirtualItem': 'false',
            'IsMissing': 'false'
        }
        
        if include_types:
            params['IncludeItemTypes'] = include_types
        else:
            params['IncludeItemTypes'] = 'Movie,Series,Episode,Video,MusicAlbum,Audio,Photo'
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'Items' in data:
                all_items = data['Items']
            elif isinstance(data, list):
                all_items = data
            else:
                all_items = []
            
            # 去重逻辑
            seen_series_ids = set()
            final_items = []
            
            for item in all_items:
                item_type = item.get('Type', '')
                series_id = item.get('SeriesId', '')
                
                if item_type == 'Episode':
                    if series_id and series_id in seen_series_ids:
                        continue
                    else:
                        if series_id:
                            seen_series_ids.add(series_id)
                        final_items.append({
                            'Id': item.get('Id'),
                            'Name': item.get('SeriesName', item.get('Name', '未知剧集')),
                            'Type': 'Series',
                            'ProductionYear': item.get('ProductionYear', ''),
                            'CommunityRating': item.get('CommunityRating', 0),
                            'Overview': item.get('Overview', ''),
                            'ImageTags': item.get('ImageTags', {}),
                            'BackdropImageTags': item.get('BackdropImageTags', [])
                        })
                else:
                    final_items.append(item)
            
            items_data = final_items[:limit]
            
            items = []
            for item in items_data:
                item_id = item.get('Id')
                if not item_id:
                    continue
                
                image_url = None
                if item.get('ImageTags', {}).get('Primary'):
                    image_url = f"{api_url}/Items/{item_id}/Images/Primary?api_key={api_key}&maxHeight=300&maxWidth=200&quality=90"
                elif item.get('BackdropImageTags') and len(item['BackdropImageTags']) > 0:
                    image_url = f"{api_url}/Items/{item_id}/Images/Backdrop?api_key={api_key}&maxHeight=300&maxWidth=200"
                
                media_type_display = item.get('Type', '')
                type_map = {
                    'Movie': '电影',
                    'Series': '剧集',
                    'Episode': '单集',
                    'Music': '音乐',
                    'MusicAlbum': '专辑',
                    'Audio': '音频',
                    'Video': '视频',
                    'Photo': '照片',
                    'BoxSet': '合集'
                }
                
                items.append({
                    'id': item_id,
                    'name': item.get('Name', '未知'),
                    'year': item.get('ProductionYear', ''),
                    'rating': item.get('CommunityRating', 0),
                    'type': type_map.get(media_type_display, media_type_display),
                    'overview': (item.get('Overview') or '')[:100],
                    'image_url': image_url,
                    'url': f"{api_url}/web/index.html#!/item/{item_id}" if item_id else '#'
                })
            
            if len(items) == 0:
                return {'error': '暂无内容'}
            
            return {
                'items': items,
                'count': len(items),
                'server': api_url,
                'media_type': media_type,
                'available_types': ['all', 'movie', 'shows', 'tv', 'video', 'music', 'photo', 'boxset']
            }
        
        return {'error': f'Emby API 请求失败: HTTP {response.status_code}'}

    except requests.exceptions.ConnectionError:
        return {'error': f'无法连接到 Emby 服务器: {api_url}'}
    except requests.exceptions.Timeout:
        return {'error': '连接 Emby 服务器超时'}
    except Exception as e:
        return {'error': f'获取失败: {str(e)}'}