// Emby 卡片渲染函数（横向滚动）
function renderEmbyCard(data, containerId) {
    if (data.error) {
        document.getElementById(containerId).innerHTML = `
            <div class="error-card">
                <i class="fa-solid fa-circle-exclamation"></i>
                <p>${escapeHtml(data.error)}</p>
                <button class="btn-slate" style="margin-top:12px;" onclick="window.parent.postMessage({type:'navigate', url:'/pages/home-settings.html'}, '*')">去配置</button>
            </div>
        `;
        return;
    }
    
    if (!data.items || data.items.length === 0) {
        document.getElementById(containerId).innerHTML = `
            <div class="empty-card">
                <i class="fa-solid fa-film"></i>
                <p>暂无最近添加的内容</p>
            </div>
        `;
        return;
    }
    
    const html = `
        <div class="emby-slider-container">
            <div class="emby-scroll-wrapper">
                <div class="emby-horizontal-list">
                    ${data.items.map(item => `
                        <div class="emby-movie-item" data-id="${item.id}">
                            <div class="movie-poster">
                                <img src="${item.image_url}" 
                                     onerror="this.src='https://placehold.co/200x300/1e293b/64748b?text=No+Image'"
                                     alt="${escapeHtml(item.name)}">
                                ${item.year ? `<div class="movie-year">${item.year}</div>` : ''}
                            </div>
                            <div class="movie-info">
                                <div class="movie-title" title="${escapeHtml(item.name)}">${escapeHtml(item.name)}</div>
                                ${item.rating > 0 ? `<div class="movie-rating"><i class="fa-solid fa-star"></i> ${item.rating.toFixed(1)}</div>` : ''}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            <div class="scroll-btn scroll-left"><i class="fa-solid fa-chevron-left"></i></div>
            <div class="scroll-btn scroll-right"><i class="fa-solid fa-chevron-right"></i></div>
        </div>
        ${data.count > 10 ? `<div class="view-more" style="text-align:center; margin-top:12px; font-size:12px; color:#64748b;">共 ${data.count} 条内容</div>` : ''}
    `;
    document.getElementById(containerId).innerHTML = html;
    
    // 绑定滚动按钮事件
    const container = document.getElementById(containerId);
    const scrollLeft = container.querySelector('.scroll-left');
    const scrollRight = container.querySelector('.scroll-right');
    const scrollWrapper = container.querySelector('.emby-scroll-wrapper');
    
    if (scrollLeft) {
        scrollLeft.onclick = () => scrollWrapper.scrollBy({ left: -300, behavior: 'smooth' });
    }
    if (scrollRight) {
        scrollRight.onclick = () => scrollWrapper.scrollBy({ left: 300, behavior: 'smooth' });
    }
}