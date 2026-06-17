# backend/services/system_service.py
"""
系统状态服务 - 支持本地系统状态和 NAS 系统状态
"""
import time
import json


def fetch_system_data(card):
    """
    获取系统状态数据
    支持两种模式:
    1. 本地模式: 获取容器自身的系统状态 (默认)
    2. NAS 模式: 通过 API 获取 NAS 系统状态
    """
    display_config = card.get('display_config', {})
    if isinstance(display_config, str):
        try:
            display_config = json.loads(display_config)
        except:
            display_config = {}
    
    # 检查是否是 NAS 模式
    nas_type = display_config.get('nas_type', '')
    
    if nas_type:
        # NAS 模式
        return fetch_nas_status(card, display_config, nas_type)
    else:
        # 本地模式
        return fetch_local_status()


def fetch_stats_data(card=None):
    """
    获取统计信息（导航链接数和用户数）
    """
    import sqlite3
    import os
    
    DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/navigator.db')
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        nav_count = cursor.execute("SELECT COUNT(*) FROM nav_items WHERE url != '' AND url IS NOT NULL").fetchone()[0]
        user_count = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        conn.close()
        return {'nav_links': nav_count, 'users': user_count}
    except Exception as e:
        print(f'[系统服务] 获取统计失败: {e}')
        return {'nav_links': 0, 'users': 0}


def fetch_local_status():
    """获取本地系统状态"""
    try:
        import psutil
        return {
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'uptime': int(time.time() - psutil.boot_time()) // 3600
        }
    except ImportError:
        return {'cpu': 25, 'memory': 45, 'disk': 60, 'uptime': 24}


def fetch_nas_status(card, config, nas_type):
    """
    通过 API 获取 NAS 系统状态
    """
    import requests
    
    api_url = config.get('api_url', '').rstrip('/')
    
    # 从 card 获取 api_key（用户名）
    username = card.get('api_key', '')
    password = config.get('password', '')
    
    # 如果是 Unraid 模式，使用 api_key
    if nas_type == 'unraid':
        api_key = card.get('api_key', '')
    else:
        api_key = ''
    
    if not api_url:
        return {'error': '请配置 NAS 地址'}
    
    try:
        if nas_type == 'synology':
            return fetch_synology_status(api_url, username, password)
        elif nas_type == 'fnos':
            return fetch_fnos_status(api_url, username, password)
        elif nas_type == 'qnap':
            return fetch_qnap_status(api_url, username, password)
        elif nas_type == 'unraid':
            return fetch_unraid_status(api_url, api_key)
        else:
            return {'error': f'不支持的 NAS 类型: {nas_type}'}
    except requests.exceptions.ConnectionError:
        return {'error': f'无法连接到 NAS: {api_url}'}
    except requests.exceptions.Timeout:
        return {'error': '连接超时'}
    except Exception as e:
        return {'error': f'获取数据失败: {str(e)}'}


def fetch_synology_status(api_url, username, password):
    """
    获取群晖系统状态
    """
    try:
        from synology_dsm import SynologyDSM
        dsm = SynologyDSM(api_url, username, password, 5001)
        dsm.login()
        
        cpu_usage = 0
        memory_usage = 0
        disk_usage = 0
        cpu_temp = None
        disk_temps = []
        
        try:
            cpu_info = dsm.cpu
            if hasattr(cpu_info, 'system_load'):
                cpu_usage = cpu_info.system_load
        except:
            pass
        
        try:
            memory_info = dsm.memory
            if memory_info.total_ram > 0:
                memory_usage = (1 - memory_info.available_ram / memory_info.total_ram) * 100
        except:
            pass
        
        try:
            storage_info = dsm.storage
            if storage_info.disks:
                for disk in storage_info.disks:
                    if disk.size_bytes > 0:
                        disk_usage = max(disk_usage, (1 - disk.avail_bytes / disk.size_bytes) * 100)
                    if hasattr(disk, 'temperature') and disk.temperature:
                        disk_temps.append({
                            'name': disk.name,
                            'temperature': disk.temperature
                        })
        except:
            pass
        
        try:
            if hasattr(dsm, 'temperature'):
                cpu_temp = dsm.temperature.cpu
        except:
            pass
        
        dsm.logout()
        
        return {
            'mode': 'nas',
            'nas_type': 'synology',
            'cpu': round(cpu_usage, 1),
            'memory': round(memory_usage, 1),
            'disk': round(disk_usage, 1),
            'uptime': 0,
            'cpu_temp': cpu_temp,
            'disk_temps': disk_temps,
            'system_temp': cpu_temp
        }
        
    except ImportError:
        return {'error': '请安装 py-synologydsm-api: pip install py-synologydsm-api'}
    except Exception as e:
        return {'error': f'获取群晖状态失败: {str(e)}'}


def fetch_fnos_status(api_url, username, password):
    """
    获取飞牛 OS 系统状态
    """
    import requests
    import json
    
    try:
        # 飞牛 OS API 端点尝试列表
        endpoints = [
            '/api/v1/auth/login',
            '/auth/login',
            '/api/auth/login'
        ]
        
        session = requests.Session()
        
        # 尝试不同的登录端点
        login_success = False
        login_resp = None
        
        for endpoint in endpoints:
            try:
                login_url = api_url + endpoint
                login_data = {
                    'username': username,
                    'password': password
                }
                print(f'[飞牛] 尝试登录: {login_url}')
                login_resp = session.post(login_url, json=login_data, timeout=10)
                if login_resp.status_code == 200:
                    login_success = True
                    print(f'[飞牛] 登录成功: {login_url}')
                    break
            except Exception as e:
                print(f'[飞牛] 登录尝试失败: {str(e)}')
                continue
        
        if not login_success:
            return {'error': '登录失败，请检查地址、用户名和密码是否正确'}
        
        login_result = login_resp.json()
        if login_result.get('code') != 0:
            return {'error': f'登录失败: {login_result.get("message", "未知错误")}'}
        
        # 获取 token（如果有）
        token = login_result.get('data', {}).get('token', '')
        if token:
            session.headers.update({'Authorization': f'Bearer {token}'})
        
        # 尝试不同的资源端点
        resource_endpoints = [
            '/api/v1/system/resource',
            '/api/system/resource',
            '/api/v1/system/status',
            '/api/system/status'
        ]
        
        resource_data = None
        for endpoint in resource_endpoints:
            try:
                url = api_url + endpoint
                print(f'[飞牛] 尝试获取资源: {url}')
                resp = session.get(url, timeout=10)
                if resp.status_code == 200:
                    resource_data = resp.json()
                    print(f'[飞牛] 获取资源成功: {url}')
                    break
            except Exception as e:
                print(f'[飞牛] 资源获取失败: {str(e)}')
                continue
        
        session.close()
        
        if resource_data is None:
            return {'error': '无法获取系统资源数据，请检查飞牛 OS 版本是否支持 API'}
        
        cpu_usage = 0
        memory_usage = 0
        disk_usage = 0
        cpu_temp = None
        disk_temps = []
        system_temp = None
        
        if resource_data.get('code') == 0:
            data = resource_data.get('data', {})
            
            # CPU
            cpu_info = data.get('cpu', {})
            if isinstance(cpu_info, dict):
                cpu_usage = cpu_info.get('usage', 0)
                if 'percent' in cpu_info:
                    cpu_usage = cpu_info.get('percent', 0)
            elif isinstance(cpu_info, (int, float)):
                cpu_usage = cpu_info
            
            # 内存
            memory_info = data.get('memory', {})
            if isinstance(memory_info, dict):
                memory_usage = memory_info.get('usage', 0)
                if 'percent' in memory_info:
                    memory_usage = memory_info.get('percent', 0)
                if 'used_percent' in memory_info:
                    memory_usage = memory_info.get('used_percent', 0)
            elif isinstance(memory_info, (int, float)):
                memory_usage = memory_info
            
            # 磁盘
            disk_info = data.get('disk', {})
            if isinstance(disk_info, dict):
                disk_usage = disk_info.get('usage', 0)
                if 'percent' in disk_info:
                    disk_usage = disk_info.get('percent', 0)
            elif isinstance(disk_info, (int, float)):
                disk_usage = disk_info
            
            # 温度
            temp_info = data.get('temperature', {})
            if isinstance(temp_info, dict):
                cpu_temp = temp_info.get('cpu')
                system_temp = temp_info.get('system', cpu_temp)
            
            # 磁盘温度
            disks = data.get('disks', [])
            if isinstance(disks, list):
                for disk in disks:
                    if isinstance(disk, dict) and disk.get('temperature'):
                        disk_temps.append({
                            'name': disk.get('name', disk.get('device', '未知')),
                            'temperature': disk.get('temperature')
                        })
        
        # 如果上面的解析没有获取到数据，尝试直接从响应中提取
        if cpu_usage == 0 and memory_usage == 0 and disk_usage == 0:
            # 可能是不同的数据结构
            if 'data' in resource_data:
                data = resource_data['data']
                # 尝试提取
                if 'cpu' in data:
                    if isinstance(data['cpu'], dict):
                        cpu_usage = data['cpu'].get('usage', 0)
                    else:
                        cpu_usage = data['cpu'] if isinstance(data['cpu'], (int, float)) else 0
                if 'memory' in data:
                    if isinstance(data['memory'], dict):
                        memory_usage = data['memory'].get('usage', 0)
                    else:
                        memory_usage = data['memory'] if isinstance(data['memory'], (int, float)) else 0
                if 'disk' in data:
                    if isinstance(data['disk'], dict):
                        disk_usage = data['disk'].get('usage', 0)
                    else:
                        disk_usage = data['disk'] if isinstance(data['disk'], (int, float)) else 0
        
        return {
            'mode': 'nas',
            'nas_type': 'fnos',
            'cpu': round(cpu_usage, 1),
            'memory': round(memory_usage, 1),
            'disk': round(disk_usage, 1),
            'uptime': 0,
            'cpu_temp': cpu_temp,
            'disk_temps': disk_temps,
            'system_temp': system_temp
        }
        
    except requests.exceptions.ConnectionError:
        return {'error': f'无法连接到飞牛服务器: {api_url}，请检查地址和端口是否正确'}
    except requests.exceptions.Timeout:
        return {'error': '连接飞牛服务器超时'}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'error': f'获取飞牛状态失败: {str(e)}'}

def fetch_qnap_status(api_url, username, password):
    """
    获取威联通系统状态
    """
    import requests
    
    try:
        session = requests.Session()
        
        login_url = f"{api_url}/cgi-bin/authLogin.cgi"
        login_params = {
            'user': username,
            'pwd': password,
            'service': 'system'
        }
        login_resp = session.get(login_url, params=login_params, timeout=10)
        
        if login_resp.status_code != 200:
            return {'error': '登录失败，请检查用户名和密码'}
        
        sid = login_resp.text.strip()
        if not sid:
            return {'error': '登录失败，无法获取 SID'}
        
        session.params = {'sid': sid}
        
        sysinfo_url = f"{api_url}/cgi-bin/sysInfo.cgi"
        sys_params = {'func': 'get_all'}
        sys_resp = session.get(sysinfo_url, params=sys_params, timeout=10)
        
        temp_url = f"{api_url}/cgi-bin/sysTemp.cgi"
        temp_params = {'func': 'get_all'}
        temp_resp = session.get(temp_url, params=temp_params, timeout=10)
        
        try:
            session.get(f"{api_url}/cgi-bin/authLogout.cgi", timeout=5)
        except:
            pass
        session.close()
        
        cpu_usage = 0
        memory_usage = 0
        disk_usage = 0
        cpu_temp = None
        disk_temps = []
        system_temp = None
        
        if sys_resp.status_code == 200:
            sys_data = sys_resp.json()
            cpu_usage = sys_data.get('cpu_usage', 0)
            memory_total = sys_data.get('mem_total', 1)
            memory_free = sys_data.get('mem_free', 0)
            if memory_total > 0:
                memory_usage = ((memory_total - memory_free) / memory_total) * 100
            disk_usage = sys_data.get('disk_usage', 0)
        
        if temp_resp.status_code == 200:
            temp_data = temp_resp.json()
            if 'cpu' in temp_data:
                try:
                    cpu_temp = float(temp_data['cpu'])
                    system_temp = cpu_temp
                except:
                    pass
            if 'disks' in temp_data:
                for disk in temp_data['disks']:
                    if disk.get('temp'):
                        try:
                            disk_temps.append({
                                'name': disk.get('name', '未知'),
                                'temperature': float(disk['temp'])
                            })
                        except:
                            pass
        
        return {
            'mode': 'nas',
            'nas_type': 'qnap',
            'cpu': round(cpu_usage, 1),
            'memory': round(memory_usage, 1),
            'disk': round(disk_usage, 1),
            'uptime': 0,
            'cpu_temp': cpu_temp,
            'disk_temps': disk_temps,
            'system_temp': system_temp
        }
        
    except Exception as e:
        return {'error': f'获取威联通状态失败: {str(e)}'}


def fetch_unraid_status(api_url, api_key):
    """
    获取 Unraid 系统状态
    """
    import requests
    
    try:
        endpoints = [
            '/api/system/status',
            '/api/status',
            '/api/v1/system/status'
        ]
        
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
            headers['X-API-Key'] = api_key
        
        data = None
        for endpoint in endpoints:
            try:
                url = api_url + endpoint
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    break
            except:
                continue
        
        if data is None:
            return {'error': '无法连接到 Unraid 监控 API，请确保已安装监控容器 (UMA 或 simple-monitoring-api)'}
        
        cpu_usage = 0
        memory_usage = 0
        disk_usage = 0
        cpu_temp = None
        disk_temps = []
        system_temp = None
        uptime = 0
        
        if isinstance(data, dict):
            cpu_usage = data.get('cpu', {}).get('usage', 0) or data.get('cpu_usage', 0)
            memory_usage = data.get('memory', {}).get('usage', 0) or data.get('memory_usage', 0)
            disk_usage = data.get('disk', {}).get('usage', 0) or data.get('disk_usage', 0)
            uptime = data.get('uptime', 0)
            cpu_temp = data.get('temperature', {}).get('cpu')
            system_temp = data.get('temperature', {}).get('system', cpu_temp)
            
            disks = data.get('disks', [])
            if isinstance(disks, list):
                for disk in disks:
                    if isinstance(disk, dict) and disk.get('temperature'):
                        disk_temps.append({
                            'name': disk.get('name', disk.get('device', '未知')),
                            'temperature': disk.get('temperature')
                        })
        
        return {
            'mode': 'nas',
            'nas_type': 'unraid',
            'cpu': round(cpu_usage, 1),
            'memory': round(memory_usage, 1),
            'disk': round(disk_usage, 1),
            'uptime': uptime,
            'cpu_temp': cpu_temp,
            'disk_temps': disk_temps,
            'system_temp': system_temp
        }
        
    except Exception as e:
        return {'error': f'获取 Unraid 状态失败: {str(e)}'}