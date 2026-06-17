# backend/routes/__init__.py
"""
路由模块 - 统一注册所有路由
"""
from flask import Blueprint

# 创建蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/api')
nav_bp = Blueprint('nav', __name__, url_prefix='/api')
card_bp = Blueprint('card', __name__, url_prefix='/api')
user_bp = Blueprint('user', __name__, url_prefix='/api')
config_bp = Blueprint('config', __name__, url_prefix='/api')
icon_bp = Blueprint('icon', __name__, url_prefix='/api')
home_bp = Blueprint('home', __name__, url_prefix='/api')


def register_blueprints(app):
    """注册所有蓝图到应用"""
    from .auth_routes import auth_bp as _auth_bp
    from .nav_routes import nav_bp as _nav_bp
    from .card_routes import card_bp as _card_bp
    from .user_routes import user_bp as _user_bp
    from .config_routes import config_bp as _config_bp
    from .icon_routes import icon_bp as _icon_bp
    from .home_routes import home_bp as _home_bp
    
    app.register_blueprint(_auth_bp)
    app.register_blueprint(_nav_bp)
    app.register_blueprint(_card_bp)
    app.register_blueprint(_user_bp)
    app.register_blueprint(_config_bp)
    app.register_blueprint(_icon_bp)
    app.register_blueprint(_home_bp)


__all__ = [
    'register_blueprints',
    'auth_bp',
    'nav_bp', 
    'card_bp',
    'user_bp',
    'config_bp',
    'icon_bp',
    'home_bp'
]