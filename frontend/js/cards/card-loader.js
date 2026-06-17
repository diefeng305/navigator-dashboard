// frontend/js/cards/card-loader.js
/**
 * 卡片加载器 - 动态加载卡片组件
 * 
 * 新增卡片类型只需在 CARD_MODULES 中注册
 * 然后在对应的卡片文件中定义组件对象
 */
var cardComponents = {};

// 卡片组件列表（新增卡片只需在这里添加）
var CARD_MODULES = {
    'system': '/js/cards/system-card.js',
    'stats': '/js/cards/stats-card.js',
    'emby': '/js/cards/emby-card.js',
    'zblog': '/js/cards/zblog-card.js'
};

// 已加载的模块
var loadedModules = {};

function loadCardModule(componentName) {
    return new Promise(function(resolve, reject) {
        // 如果已经加载，直接返回
        if (loadedModules[componentName]) {
            resolve();
            return;
        }
        
        var scriptPath = CARD_MODULES[componentName];
        if (!scriptPath) {
            resolve(); // 未知组件，跳过
            return;
        }
        
        var script = document.createElement('script');
        script.src = scriptPath;
        script.onload = function() {
            loadedModules[componentName] = true;
            resolve();
        };
        script.onerror = function() {
            console.error('加载卡片组件失败:', componentName);
            resolve();
        };
        document.head.appendChild(script);
    });
}

function getCardComponent(componentName) {
    if (cardComponents[componentName]) {
        return cardComponents[componentName];
    }
    
    // 尝试从全局变量获取
    var globalName = componentName.charAt(0).toUpperCase() + componentName.slice(1) + 'Card';
    if (window[globalName]) {
        cardComponents[componentName] = window[globalName];
        return window[globalName];
    }
    
    return null;
}

// 导出到全局
window.cardComponents = cardComponents;
window.loadCardModule = loadCardModule;
window.getCardComponent = getCardComponent;