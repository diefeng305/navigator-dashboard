// 天气卡片渲染函数 - 支持 API 模式和 iframe 模式

function renderWeatherCard(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    // 检查是否是 iframe 模式
    if ((data.mode === 'iframe' || data.display_config?.mode === 'iframe') && (data.iframe_url || data.display_config?.iframe_url)) {
        renderIframeWeather(data, container);
        return;
    }
    
    // API 模式渲染
    renderApiWeather(data, container);
}

function renderIframeWeather(data, container) {
    let iframeUrl = data.iframe_url || data.display_config?.iframe_url || '';
    
    // 如果用户粘贴了完整的 iframe 代码，提取 src
    const srcMatch = iframeUrl.match(/src=["']([^"']+)["']/);
    if (srcMatch) {
        iframeUrl = srcMatch[1];
    }
    
    // 获取高度配置
    const height = (data.display_config?.height || data.height || 150);
    
    const html = `
        <div class="weather-iframe-container">
            <iframe 
                src="${escapeHtml(iframeUrl)}" 
                frameborder="0" 
                scrolling="no" 
                allowtransparency="true"
                style="width:100%; height:${height}px; border:none;"
                onload="this.style.opacity='1'"
            ></iframe>
        </div>
    `;
    container.innerHTML = html;
}

function renderApiWeather(data, container) {
    if (data.error) {
        container.innerHTML = `
            <div class="error-card">
                <i class="fa-solid fa-circle-exclamation"></i>
                <p>${escapeHtml(data.error)}</p>
                <button class="btn-slate" style="margin-top:12px;" onclick="window.parent.postMessage({type:'navigate', url:'/pages/home-settings.html'}, '*')">去配置</button>
            </div>
        `;
        return;
    }
    
    const temp = data.temperature;
    const displayTemp = temp !== undefined && temp !== null ? Math.round(temp) : '--';
    
    const html = `
        <div class="weather-info">
            <div><i class="fa-solid fa-location-dot"></i> ${escapeHtml(data.city || 'Unknown')}</div>
            <div class="weather-temp">${displayTemp}°</div>
            <div class="weather-desc">${escapeHtml(data.description || '')}</div>
            <div class="weather-details">
                <div><i class="fa-solid fa-droplet"></i> ${data.humidity || '--'}%</div>
                <div><i class="fa-regular fa-clock"></i> ${new Date().toLocaleTimeString()}</div>
            </div>
        </div>
    `;
    container.innerHTML = html;
}