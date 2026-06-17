# backend/services/zblog_service.py
"""
Z-Blog 服务 - 通过 XML-RPC 获取分类和文章
"""
import xmlrpc.client
import re
from datetime import datetime
from urllib.parse import urljoin


def fetch_zblog_data(card):
    """
    获取 Z-Blog 分类和最新文章数据
    """
    # 从卡片中获取配置
    api_url = card.get('api_url', '')
    username = card.get('api_key', '')
    display_config = card.get('display_config', {})
    
    if isinstance(display_config, str):
        try:
            import json
            display_config = json.loads(display_config)
        except:
            display_config = {}
    
    password = display_config.get('password', '')
    
    if not api_url or not username or not password:
        return {'error': '请配置 Z-Blog XML-RPC 地址、用户名和密码'}
    
    posts_per_category = display_config.get('posts_per_category', 3)
    
    try:
        server = xmlrpc.client.ServerProxy(api_url)
        
        categories = get_categories(server, username, password)
        if not categories:
            return {'error': '获取分类失败，请检查用户名和密码是否正确'}
        
        all_posts = get_recent_posts(server, username, password, 50)
        if all_posts is None:
            return {'error': '获取文章失败，请检查 XML-RPC 是否启用'}
        
        # 提取服务器域名用于拼接完整 URL
        server_domain = extract_domain(api_url)
        
        category_list = []
        for cat in categories:
            cat_id = cat.get('categoryId') or cat.get('cat_ID') or cat.get('id')
            cat_name = cat.get('categoryName') or cat.get('cat_name') or cat.get('name')
            cat_url = cat.get('categoryUrl') or cat.get('htmlUrl') or ''
            
            if not cat_id or not cat_name:
                continue
            
            cat_posts = []
            for post in all_posts:
                post_categories = post.get('categories', [])
                if isinstance(post_categories, list) and cat_name in post_categories:
                    cat_posts.append(post)
                elif not isinstance(post_categories, list) and str(post_categories) == str(cat_id):
                    cat_posts.append(post)
            
            cat_posts.sort(key=lambda x: x.get('dateCreated', ''), reverse=True)
            cat_posts = cat_posts[:posts_per_category]
            
            post_list = []
            for post in cat_posts:
                post_title = post.get('title', '')
                post_link = post.get('link', '')
                post_desc = post.get('description', '')
                post_date = post.get('dateCreated', '')
                
                if isinstance(post_date, datetime):
                    post_date = post_date.strftime('%Y-%m-%d')
                elif isinstance(post_date, str):
                    post_date = post_date[:10] if len(post_date) >= 10 else post_date
                else:
                    post_date = ''
                
                # 提取缩略图 - 传入文章链接用于补全相对路径
                thumbnail = extract_thumbnail(post_desc, post_link, server_domain)
                
                post_list.append({
                    'title': post_title,
                    'url': post_link,
                    'description': strip_html(post_desc)[:100],
                    'date': post_date,
                    'thumbnail': thumbnail
                })
            
            if post_list:
                category_list.append({
                    'id': cat_id,
                    'name': cat_name,
                    'url': cat_url,
                    'posts': post_list
                })
        
        if not category_list and all_posts:
            post_list = []
            for post in all_posts[:posts_per_category * 3]:
                post_title = post.get('title', '')
                post_link = post.get('link', '')
                post_desc = post.get('description', '')
                post_date = post.get('dateCreated', '')
                
                if isinstance(post_date, datetime):
                    post_date = post_date.strftime('%Y-%m-%d')
                elif isinstance(post_date, str):
                    post_date = post_date[:10] if len(post_date) >= 10 else post_date
                else:
                    post_date = ''
                
                thumbnail = extract_thumbnail(post_desc, post_link, server_domain)
                
                post_list.append({
                    'title': post_title,
                    'url': post_link,
                    'description': strip_html(post_desc)[:100],
                    'date': post_date,
                    'thumbnail': thumbnail
                })
            
            category_list.append({
                'id': 'latest',
                'name': '最新文章',
                'url': '',
                'posts': post_list
            })
        
        return {
            'categories': category_list,
            'total': len(category_list),
            'server': api_url
        }
        
    except xmlrpc.client.Fault as e:
        return {'error': f'XML-RPC 连接失败: {str(e)}'}
    except ConnectionError:
        return {'error': f'无法连接到 Z-Blog 服务器: {api_url}'}
    except Exception as e:
        return {'error': f'获取数据失败: {str(e)}'}


def get_categories(server, username, password):
    """获取分类列表"""
    methods = [
        lambda: server.metaWeblog.getCategories('', username, password),
        lambda: server.wp.getCategories('', username, password),
    ]
    
    for method in methods:
        try:
            result = method()
            if result and len(result) > 0:
                return result
        except:
            continue
    
    return []


def get_recent_posts(server, username, password, count):
    """获取最新文章列表"""
    try:
        posts = server.metaWeblog.getRecentPosts('', username, password, count)
        return posts
    except:
        pass
    
    try:
        posts = server.mt.getRecentPostTitles('', username, password, count)
        return posts
    except:
        pass
    
    return None


def extract_domain(api_url):
    """
    从 XML-RPC URL 中提取网站域名
    例如: https://blog.example.com/zb_system/xml-rpc/index.php
    返回: https://blog.example.com
    """
    match = re.match(r'(https?://[^/]+)', api_url)
    if match:
        return match.group(1)
    return api_url


def extract_thumbnail(html_content, post_url, server_domain):
    """
    从文章内容中提取缩略图
    支持:
    1. <img src="..."> 标签
    2. Markdown 格式 ![](url)
    3. 相对路径自动补全为完整 URL
    """
    if not html_content:
        return None
    
    image_url = None
    
    # 方法1: 从 <img> 标签提取
    img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if img_match:
        image_url = img_match.group(1)
    
    # 方法2: 如果没找到，尝试从 Markdown 图片格式提取
    if not image_url:
        md_match = re.search(r'!\[[^\]]*\]\(([^)]+)\)', html_content)
        if md_match:
            image_url = md_match.group(1)
    
    # 方法3: 尝试从文章中的图片标签提取 data-src (懒加载)
    if not image_url:
        data_src_match = re.search(r'<img[^>]+data-src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if data_src_match:
            image_url = data_src_match.group(1)
    
    # 方法4: 尝试从文章中的图片标签提取 data-original (懒加载)
    if not image_url:
        data_original_match = re.search(r'<img[^>]+data-original=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if data_original_match:
            image_url = data_original_match.group(1)
    
    if not image_url:
        return None
    
    # 处理相对路径: 补全为完整 URL
    if image_url.startswith('/'):
        # 使用文章链接补全
        if post_url:
            # 从文章链接提取域名
            domain_match = re.match(r'(https?://[^/]+)', post_url)
            if domain_match:
                image_url = domain_match.group(1) + image_url
            else:
                image_url = server_domain + image_url
        else:
            image_url = server_domain + image_url
    elif image_url.startswith('./') or image_url.startswith('../'):
        # 相对路径，尝试用文章链接补全
        if post_url:
            # 去掉文章链接末尾的部分，拼接图片路径
            base_url = re.sub(r'/[^/]+$', '/', post_url)
            image_url = urljoin(base_url, image_url)
        else:
            image_url = urljoin(server_domain + '/', image_url)
    
    # 过滤掉可能的表情符号或占位图
    if image_url and ('emoji' in image_url or 'smiley' in image_url or '1x1' in image_url):
        return None
    
    return image_url


def strip_html(html):
    """去除 HTML 标签"""
    if not html:
        return ''
    return re.sub(r'<[^>]+>', '', html)