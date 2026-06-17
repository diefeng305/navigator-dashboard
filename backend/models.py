import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../data/navigator.db')

def init_db():
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'visitor'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nav_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            icon TEXT,
            parent_id INTEGER DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            min_role_required TEXT DEFAULT 'visitor',
            open_type TEXT DEFAULT 'iframe'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY, 
            value TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS home_quick_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT DEFAULT 'fa-solid fa-link',
            url TEXT NOT NULL,
            sort_order INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS local_icons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT,
            path TEXT NOT NULL,
            file_size INTEGER,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS home_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            card_type TEXT NOT NULL,
            api_url TEXT,
            api_key TEXT,
            sort_order INTEGER DEFAULT 0,
            enabled INTEGER DEFAULT 1,
            refresh_interval INTEGER DEFAULT 60,
            display_config TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
    
    cursor.execute("SELECT COUNT(*) FROM system_config WHERE key='show_welcome'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('show_welcome', 'true')")
    
    cursor.execute("SELECT COUNT(*) FROM system_config WHERE key='show_datetime'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('show_datetime', 'true')")
    
    cursor.execute("SELECT COUNT(*) FROM system_config WHERE key='custom_welcome'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('custom_welcome', '')")
    
    cursor.execute("SELECT COUNT(*) FROM nav_items")
    if cursor.fetchone()[0] == 0:
        default_items = [
            ('常用服务', '', 'fa-solid fa-star', 0, 10, 'visitor', 'iframe'),
            ('开发工具', '', 'fa-solid fa-code', 0, 20, 'visitor', 'iframe'),
            ('媒体娱乐', '', 'fa-solid fa-film', 0, 30, 'visitor', 'iframe'),
            ('百度', 'https://www.baidu.com', 'fa-brands fa-baidu', 1, 1, 'visitor', 'blank'),
            ('Google', 'https://www.google.com', 'fa-brands fa-google', 1, 2, 'visitor', 'blank'),
            ('GitHub', 'https://github.com', 'fa-brands fa-github', 1, 3, 'visitor', 'blank'),
        ]
        for item in default_items:
            cursor.execute('''
                INSERT INTO nav_items (title, url, icon, parent_id, sort_order, min_role_required, open_type) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', item)
    
    cursor.execute("SELECT COUNT(*) FROM home_quick_links")
    if cursor.fetchone()[0] == 0:
        default_links = [
            ('NAS 管理', 'fa-solid fa-server', '#', 10),
            ('文件管理', 'fa-solid fa-folder-open', '#', 20),
            ('下载中心', 'fa-solid fa-download', '#', 30),
            ('影视中心', 'fa-solid fa-film', '#', 40),
        ]
        for link in default_links:
            cursor.execute("INSERT INTO home_quick_links (name, icon, url, sort_order) VALUES (?, ?, ?, ?)", link)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("数据库初始化完成！管理员账号: admin / admin123")
