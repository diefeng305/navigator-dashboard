// 卡片共享工具函数

// 格式化速度
function formatSpeed(bytes) {
    if (!bytes) return '0 B/s';
    if (bytes < 1024) return bytes + ' B/s';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB/s';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB/s';
}

// HTML 转义
function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

// 获取卡片图标
function getCardIcon(type) {
    const icons = {
        weather: 'fa-solid fa-cloud-sun',
        system: 'fa-solid fa-microchip',
        stats: 'fa-solid fa-chart-line',
        qbit: 'fa-solid fa-download',
        emby: 'fa-solid fa-film',
        custom: 'fa-solid fa-code'
    };
    return icons[type] || 'fa-solid fa-chart-simple';
}