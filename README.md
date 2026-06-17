# 🚀 Navigator - 个人导航页与仪表盘系统

<div align="center">

![Docker Pulls](https://img.shields.io/docker/pulls/你的用户名/navigator-dashboard)
![GitHub stars](https://img.shields.io/github/stars/diefeng305/navigator-dashboard)
![GitHub license](https://img.shields.io/github/license/diefeng305/navigator-dashboard)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)

**一个功能完整的个人导航页系统，让所有服务触手可及**

[在线演示](#) | [快速开始](#-快速开始) | [功能特性](#-功能特性) | [配置指南](#-配置指南)

</div>

---

## 📖 项目简介

Navigator 是一个轻量级、可扩展的个人导航页与仪表盘系统。它可以帮助你统一管理所有内部服务（NAS、Emby、博客等），通过卡片形式展示系统状态、媒体信息、博客动态等，让所有服务触手可及。

### 适用场景

- 🏠 **家庭服务器**：统一管理 NAS、媒体服务器、下载工具等
- 🏢 **小型团队**：内部服务导航和状态监控
- 👨‍💻 **个人开发者**：聚合个人项目和常用工具
- 📚 **博客/内容创作者**：展示最新文章和动态

### 核心优势

- ✅ **开箱即用**：Docker 一键部署，5 分钟即可运行
- ✅ **轻量高效**：基于 Flask + SQLite，资源占用极低
- ✅ **模块化设计**：卡片组件独立加载，易于扩展
- ✅ **安全可控**：数据存储在本地，无第三方依赖
- ✅ **界面美观**：暗色主题 + 发光特效，支持自定义配色

---

## ✨ 功能特性

### 1. 🗂️ 导航菜单管理

| 功能 | 说明 |
|------|------|
| 多级菜单 | 支持父级分类 + 子级条目，无限层级 |
| 图标支持 | 内置 Font Awesome 700+ 图标，支持自定义上传 |
| 权限控制 | 基于角色的访问控制 (visitor/user/special/admin) |
| 打开方式 | iframe 内嵌 / 新窗口打开 |

### 2. 📊 首页卡片系统（核心功能）

卡片系统采用**模块化设计**，每个卡片类型独立为组件，方便扩展：

| 卡片类型 | 功能说明 | 配置难度 |
|----------|----------|----------|
| 🌤️ **天气预报** | 支持 iframe 嵌入 和 OpenWeatherMap API 两种模式 | ⭐ 简单 |
| 💻 **系统状态** | CPU/内存/磁盘使用率，支持本地和 NAS 监控 | ⭐⭐ 中等 |
| 📈 **导航统计** | 导航链接数 + 注册用户数统计 | ⭐ 简单 |
| 🎬 **Emby/Jellyfin** | 最近添加的媒体内容，支持按类型筛选 | ⭐⭐ 中等 |
| 📝 **Z-Blog 博客** | 博客分类和最新文章，支持缩略图 | ⭐⭐ 中等 |
| 🔌 **自定义API** | 接入任意 JSON API 数据 | ⭐⭐⭐ 高级 |

### 3. 🎨 主题与个性化

| 功能 | 说明 |
|------|------|
| Logo 定制 | 自定义侧边栏标题和字母图标 |
| 配色方案 | 6 种预设主题 + 自定义颜色 |
| 布局特效 | 毛玻璃效果、发光动画、紧凑模式 |
| 欢迎区域 | 自定义欢迎语、显示/隐藏日期时间 |
| 农历日历 | 点击日期显示农历和节日信息 |

### 4. 👤 用户管理

| 功能 | 说明 |
|------|------|
| 多用户支持 | 支持创建多个用户账号 |
| 角色权限 | visitor/user/special/admin 四级权限 |
| 密码管理 | 支持修改密码 |

### 5. 🖼️ 图标管理

| 功能 | 说明 |
|------|------|
| 图标上传 | 支持 png/jpg/gif/svg/webp/ico 格式 |
| 图标库 | 内置 Font Awesome 图标库 |

---

## 📸 功能预览

### 首页仪表盘
┌─────────────────────────────────────────────────────────────────────┐
│ 🔷 Navigator 👤 admin │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 📂 我的导航 📊 系统状态 🌤️ 天气预报 │ │
│ │ ├── 常用服务 CPU: 25% ☀️ 26°C 宁波 │ │
│ │ │ ├── 百度 内存: 45% │ │
│ │ │ └── GitHub 磁盘: 60% │ │
│ │ └── 开发工具 │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 📺 最新影视 [全部 ▼] [电影] [剧集] [音乐] │ │
│ │ [🎬 电影A] [🎬 电影B] [📺 剧集C] [🎵 专辑D] │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 📝 博客动态 │ │
│ │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │ │
│ │ │ 技术分类 │ │ 生活分类 │ │ 随笔分类 │ │ │
│ │ │ ├ 📄 文章1 │ │ ├ 📄 文章1 │ │ ├ 📄 文章1 │ │ │
│ │ │ ├ 📄 文章2 │ │ └ 📄 文章2 │ │ └ 📄 文章2 │ │ │
│ │ │ └ 📄 文章3 │ │ │ │ │ │ │
│ │ └─────────────┘ └─────────────┘ └─────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

text

### 系统设置界面
┌─────────────────────────────────────────────────────────────────────┐
│ 🔧 系统设置 │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ 📋 菜单与类目 🖼️ 图标 👤 用户权限 🎨 主题 📊 首页定制 │ │
│ ├─────────────────────────────────────────────────────────────────┤ │
│ │ 个性化文案与Logo │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ 顶部 Logo: [Navigator] 字母图标: [N] │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ │ 自定义配色方案 │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ [暗夜青黛] [紫罗兰] [深海蓝] [翠绿森林] [琥珀暖阳] │ │ │
│ │ │ 主色调: [■] 强调色: [■] 背景色: [■] │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ │ 欢迎区域配置 │ │
│ │ ┌─────────────────────────────────────────────────────────┐ │ │
│ │ │ ☑ 显示欢迎语 ☑ 显示日期时间 │ │ │
│ │ │ 自定义欢迎语: [欢迎回来] │ │ │
│ │ └─────────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘

text

---

## 🚀 快速开始

### 方式一：Docker 一键部署（推荐）

services:
  navigator-dev:
    image: diefeng305/navigator-dashboard:latest
    container_name: navigator-debug-test
    ports:
      - "5500:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/config"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s


docker-compose up -d
方式三：源码运行
bash
# 1. 克隆项目
git clone https://github.com/diefeng305/navigator-dashboard.git
cd navigator-dashboard

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python backend/app.py

# 4. 访问
# http://localhost:5000
🔧 配置指南
环境变量
变量	说明	默认值
FLASK_ENV	运行环境 (development/production)	development
FLASK_DEBUG	调试模式	1
PYTHONUNBUFFERED	Python 输出不缓冲	1
卡片配置
天气预报卡片
iframe 模式（最简单）：

前往天气网站获取 iframe 代码

粘贴到配置框中即可

API 模式（OpenWeatherMap）：

注册 OpenWeatherMap 获取 API Key

填写 API Key 和城市名称

Emby 卡片
在 Emby 后台获取 API Key

填写 Emby 服务器地址和 API Key

选择要显示的媒体类型

Z-Blog 卡片
在 Z-Blog 后台启用 XML-RPC 协议

填写 XML-RPC 地址、用户名和密码

系统状态卡片（NAS 监控）
NAS 类型	配置说明
群晖	地址 + 端口(5000/5001) + 用户名 + 密码
飞牛	地址 + 端口(5666/8000) + 用户名 + 密码
威联通	地址 + 端口(8080) + 用户名 + 密码
Unraid	地址 + 端口(24940) + API Key
📁 项目结构
text
navigator-dashboard/
├── .github/                         # GitHub Actions 配置
│   └── workflows/
│       └── docker-build.yml         # 自动构建镜像
├── backend/                         # 后端代码
│   ├── app.py                       # Flask 主应用 (路由 + API)
│   ├── models.py                    # 数据库模型定义
│   ├── services/                    # 服务层 (卡片数据获取)
│   │   ├── __init__.py
│   │   ├── card_service.py          # 卡片统一调度器
│   │   ├── weather_service.py       # 天气数据服务
│   │   ├── emby_service.py          # Emby 媒体服务
│   │   ├── system_service.py        # 系统状态服务
│   │   └── zblog_service.py         # Z-Blog 博客服务
│   └── utils/                       # 工具函数
│       ├── __init__.py
│       └── db_utils.py              # 数据库工具
├── frontend/                        # 前端代码
│   ├── index.html                   # 主入口页面 (框架)
│   ├── css/                         # 样式文件
│   │   ├── style.css                # 主样式
│   │   └── calendar.css             # 日历样式
│   ├── js/                          # JavaScript
│   │   ├── main.js                  # 主逻辑 (菜单/登录/主题)
│   │   ├── calendar.js              # 日历组件
│   │   └── cards/                   # 卡片组件 (独立加载)
│   │       ├── card-loader.js       # 卡片加载器
│   │       ├── emby-card.js         # Emby 卡片
│   │       ├── system-card.js       # 系统状态卡片
│   │       ├── stats-card.js        # 统计卡片
│   │       └── zblog-card.js        # Z-Blog 卡片
│   ├── pages/                       # 子页面 (iframe 加载)
│   │   ├── home.html                # 首页仪表盘
│   │   ├── admin.html               # 系统设置
│   │   └── home-settings.html       # 首页卡片定制
│   └── assets/                      # 静态资源
│       └── icons/                   # 用户上传的图标
├── data/                            # 数据目录 (运行时创建)
│   └── navigator.db                 # SQLite 数据库
├── screenshots/                     # 截图目录
│   ├── home.png
│   └── admin.png
├── docker-compose.yaml              # Docker Compose 编排
├── Dockerfile                       # Docker 镜像构建
├── requirements.txt                 # Python 依赖
├── .gitignore                       # Git 忽略文件
├── .dockerignore                    # Docker 忽略文件
└── README.md                        # 项目文档
🛠️ 技术栈
层级	技术	版本
后端框架	Flask	3.1.3
编程语言	Python	3.11
数据库	SQLite	3
前端	原生 JavaScript + CSS3	-
图标库	Font Awesome	6.4
容器化	Docker + Docker Compose	-
依赖管理	pip	-
📊 数据库结构
sql
-- 用户表
users (id, username, password, role)

-- 导航菜单表
nav_items (id, title, url, icon, parent_id, sort_order, min_role_required, open_type)

-- 系统配置表
system_config (key, value)

-- 首页快捷链接表
home_quick_links (id, name, icon, url, sort_order)

-- 本地图标表
local_icons (id, filename, original_name, path, file_size, upload_time)

-- 首页卡片配置表
home_cards (id, title, card_type, api_url, api_key, sort_order, enabled, refresh_interval, display_config, created_at, updated_at)
🔄 API 接口文档
认证相关
接口	方法	说明
/api/login	POST	用户登录
导航菜单
接口	方法	说明
/api/navigation	GET	获取导航菜单
/api/navigation/add	POST	添加菜单项
/api/navigation/update/<id>	POST	更新菜单项
/api/navigation/delete/<id>	POST	删除菜单项
卡片管理
接口	方法	说明
/api/home/cards	GET	获取所有卡片配置
/api/home/cards	POST	添加卡片
/api/home/cards/<id>	PUT	更新卡片
/api/home/cards/<id>	DELETE	删除卡片
/api/home/cards/data	GET	获取所有卡片数据
/api/home/cards/single/<id>	GET	获取单个卡片数据
系统配置
接口	方法	说明
/api/config	GET	获取系统配置
/api/config/update	POST	更新系统配置
/api/home/page-config	GET	获取页面配置
/api/home/page-config	POST	更新页面配置
🤝 贡献指南
欢迎提交 Issue 和 Pull Request！

Fork 本仓库

创建你的特性分支 (git checkout -b feature/AmazingFeature)

提交你的更改 (git commit -m 'Add some AmazingFeature')

推送到分支 (git push origin feature/AmazingFeature)

打开 Pull Request

📄 许可证
MIT License - 详见 LICENSE 文件

🙏 致谢
Font Awesome - 图标库

Flask - Web 框架

OpenWeatherMap - 天气数据

📧 联系方式
GitHub: @diefeng305

项目地址: https://github.com/diefeng305/navigator-dashboard

<div align="center">
⭐ 如果这个项目对你有帮助，请给个 Star！

Made with ❤️ by diefeng305

</div> ```