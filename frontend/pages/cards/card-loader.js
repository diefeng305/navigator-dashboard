// 卡片加载器 - 动态加载对应卡片的渲染函数

// 已加载的卡片模块缓存
const cardModules = {};

// 加载卡片模块
async function loadCardModule(cardType) {
    if (cardModules[cardType]) {
        return cardModules[cardType];
    }
    
    const moduleMap = {
        'weather': '/pages/cards/weather-card.js',
        'system': '/pages/cards/system-card.js',
        'stats': '/pages/cards/stats-card.js',
        'emby': '/pages/cards/emby-card.js',
        'custom': '/pages/cards/custom-card.js',
        'qbit': '/pages/cards/custom-card.js'  // qbit 暂时使用通用渲染
    };
    
    const scriptPath = moduleMap[cardType];
    if (!scriptPath) {
        console.warn(`未知卡片类型: ${cardType}`);
        return null;
    }
    
    try {
        await loadScript(scriptPath);
        cardModules[cardType] = true;
        return true;
    } catch (error) {
        console.error(`加载卡片模块失败: ${cardType}`, error);
        return null;
    }
}

// 动态加载脚本
function loadScript(src) {
    return new Promise((resolve, reject) => {
        // 检查是否已加载
        const existingScript = document.querySelector(`script[src="${src}"]`);
        if (existingScript) {
            resolve();
            return;
        }
        
        const script = document.createElement('script');
        script.src = src;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`加载失败: ${src}`));
        document.head.appendChild(script);
    });
}

// 渲染卡片（主入口）
async function renderCard(card, cardData, containerId) {
    const cardType = card.card_type;
    
    // 先加载共享工具函数
    if (!window.escapeHtml) {
        await loadScript('/pages/cards/card-utils.js');
    }
    
    // 加载卡片模块
    await loadCardModule(cardType);
    
    // 根据卡片类型调用对应的渲染函数
    switch (cardType) {
        case 'weather':
            if (typeof renderWeatherCard === 'function') {
                renderWeatherCard(cardData, containerId);
            } else {
                fallbackRender(cardData, containerId);
            }
            break;
        case 'system':
            if (typeof renderSystemCard === 'function') {
                renderSystemCard(cardData, containerId);
            } else {
                fallbackRender(cardData, containerId);
            }
            break;
        case 'stats':
            if (typeof renderStatsCard === 'function') {
                renderStatsCard(cardData, containerId);
            } else {
                fallbackRender(cardData, containerId);
            }
            break;
        case 'emby':
            if (typeof renderEmbyCard === 'function') {
                renderEmbyCard(cardData, containerId);
            } else {
                fallbackRender(cardData, containerId);
            }
            break;
        default:
            if (typeof renderCustomCard === 'function') {
                renderCustomCard(cardData, containerId);
            } else {
                fallbackRender(cardData, containerId);
            }
    }
}

// 降级渲染
function fallbackRender(data, containerId) {
    const html = `<pre style="font-size:12px;color:#94a3b8;overflow-x:auto;">${JSON.stringify(data, null, 2)}</pre>`;
    document.getElementById(containerId).innerHTML = html;
}