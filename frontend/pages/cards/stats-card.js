// 统计卡片渲染函数
function renderStatsCard(data, containerId) {
    const html = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${data.nav_links || 0}</div>
                <div>导航链接</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${data.users || 0}</div>
                <div>注册用户</div>
            </div>
        </div>
    `;
    document.getElementById(containerId).innerHTML = html;
}