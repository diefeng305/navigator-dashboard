# 🚀 Navigator - 个人导航页与仪表盘系统

<div align="center">

![Docker Pulls](https://img.shields.io/docker/pulls/diefeng305/navigator-dashboard)
![GitHub stars](https://img.shields.io/github/stars/diefeng305/navigator-dashboard)
![GitHub license](https://img.shields.io/github/license/diefeng305/navigator-dashboard)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green)

**一个功能完整的个人导航页系统，让所有服务触手可及**

[快速开始](#-快速开始) | [功能特性](#-功能特性) | [配置指南](#-配置指南)

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

### 2. 📊 首页卡片系统

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

## 🚀 快速开始

### 方式一：Docker 一键部署（推荐）

```bash
# 1. 拉取镜像
docker pull diefeng305/navigator-dashboard:latest

# 2. 创建数据目录
mkdir -p navigator-data

# 3. 启动容器
docker run -d \
  --name navigator \
  -p 5000:5000 \
  -v $(pwd)/navigator-data:/app/data \
  --restart unless-stopped \
  diefeng305/navigator-dashboard:latest

# 4. 访问
# http://localhost:5000
# 管理员账号: admin / admin123
```

### 方式二：Docker Compose 部署

创建 `docker-compose.yaml`：

```yaml
services:
  navigator:
    image: diefeng305/navigator-dashboard:latest
    container_name: navigator
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

```bash
docker-compose up -d
```

### 方式三：源码运行

```bash
# 1. 克隆项目
git clone https://github.com/diefeng305/navigator-dashboard.git
cd navigator-dashboard

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python backend/app.py

# 4. 访问
# http://localhost:5000
# 管理员账号: admin / admin123
```

---

## 🔧 配置指南

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `FLASK_ENV` | 运行环境 (development/production) | `development` |
| `FLASK_DEBUG` | 调试模式 | `1` |
| `PYTHONUNBUFFERED` | Python 输出不缓冲 | `1` |

### 卡片配置

#### 天气预报卡片

**iframe 模式（最简单）**：
1. 前往天气网站获取 iframe 代码
2. 粘贴到配置框中即可

**API 模式（OpenWeatherMap）**：
1. 注册 [OpenWeatherMap](https://openweathermap.org/api) 获取 API Key
2. 填写 API Key 和城市名称

#### Emby 卡片

1. 在 Emby 后台获取 API Key
2. 填写 Emby 服务器地址和 API Key
3. 选择要显示的媒体类型

#### Z-Blog 卡片

1. 在 Z-Blog 后台启用 XML-RPC 协议
2. 填写 XML-RPC 地址、用户名和密码

#### 系统状态卡片（NAS 监控）

| NAS 类型 | 配置说明 |
|----------|----------|
| 群晖 | 地址 + 端口(5000/5001) + 用户名 + 密码 |
| 飞牛 | 地址 + 端口(5666/8000) + 用户名 + 密码 |
| 威联通 | 地址 + 端口(8080) + 用户名 + 密码 |
| Unraid | 地址 + 端口(24940) + API Key |

---

## 📁 项目结构

```
navigator-dashboard/
├── .github/
│   └── workflows/
│       └── docker-build.yml
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── card_service.py
│   │   ├── weather_service.py
│   │   ├── emby_service.py
│   │   ├── system_service.py
│   │   └── zblog_service.py
│   └── utils/
│       ├── __init__.py
│       └── db_utils.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── style.css
│   │   └── calendar.css
│   ├── js/
│   │   ├── main.js
│   │   ├── calendar.js
│   │   └── cards/
│   │       ├── card-loader.js
│   │       ├── emby-card.js
│   │       ├── system-card.js
│   │       ├── stats-card.js
│   │       └── zblog-card.js
│   ├── pages/
│   │   ├── home.html
│   │   ├── admin.html
│   │   └── home-settings.html
│   └── assets/
│       └── icons/
├── data/
│   └── navigator.db
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── .gitignore
├── .dockerignore
└── README.md
```

---

## 🛠️ 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | Flask | 3.1.3 |
| 编程语言 | Python | 3.11 |
| 数据库 | SQLite | 3 |
| 前端 | 原生 JavaScript + CSS3 | - |
| 图标库 | Font Awesome | 6.4 |
| 容器化 | Docker + Docker Compose | - |

---

## 📊 数据库结构

```sql
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
```

---

## 🔄 API 接口文档

### 认证相关

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/login` | POST | 用户登录 |

### 导航菜单

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/navigation` | GET | 获取导航菜单 |
| `/api/navigation/add` | POST | 添加菜单项 |
| `/api/navigation/update/<id>` | POST | 更新菜单项 |
| `/api/navigation/delete/<id>` | POST | 删除菜单项 |

### 卡片管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/home/cards` | GET | 获取所有卡片配置 |
| `/api/home/cards` | POST | 添加卡片 |
| `/api/home/cards/<id>` | PUT | 更新卡片 |
| `/api/home/cards/<id>` | DELETE | 删除卡片 |
| `/api/home/cards/data` | GET | 获取所有卡片数据 |
| `/api/home/cards/single/<id>` | GET | 获取单个卡片数据 |

### 系统配置

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/config` | GET | 获取系统配置 |
| `/api/config/update` | POST | 更新系统配置 |
| `/api/home/page-config` | GET | 获取页面配置 |
| `/api/home/page-config` | POST | 更新页面配置 |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Font Awesome](https://fontawesome.com/) - 图标库
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [OpenWeatherMap](https://openweathermap.org/) - 天气数据

---

## 📧 联系方式

- GitHub: [@diefeng305](https://github.com/diefeng305)
- 项目地址: [https://github.com/diefeng305/navigator-dashboard](https://github.com/diefeng305/navigator-dashboard)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by diefeng305

</div>