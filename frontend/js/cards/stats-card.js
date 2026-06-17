// frontend/js/cards/stats-card.js
/**
 * 统计卡片组件
 */
var StatsCard = {
    name: 'stats',
    
    render: function(cardId, data) {
        if (!data) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>数据为空</p></div>';
        }
        
        var navLinks = data.nav_links || 0;
        var users = data.users || 0;
        
        return `
            <div class="stats-grid-2">
                <div class="stat-big-card"><div class="stat-big-number">${navLinks}</div><div class="stat-big-label">导航链接</div></div>
                <div class="stat-big-card"><div class="stat-big-number">${users}</div><div class="stat-big-label">注册用户</div></div>
            </div>
        `;
    }
};

window.StatsCard = StatsCard;