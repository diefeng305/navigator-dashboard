// 系统状态卡片渲染函数
function renderSystemCard(data, containerId) {
    const html = `
        <div class="stat-item">
            <span><i class="fa-solid fa-cpu"></i> CPU</span>
            <span>${data.cpu || 0}%</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width: ${data.cpu || 0}%"></div></div>
        <div class="stat-item">
            <span><i class="fa-solid fa-memory"></i> 内存</span>
            <span>${data.memory || 0}%</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width: ${data.memory || 0}%"></div></div>
        <div class="stat-item">
            <span><i class="fa-solid fa-hard-drive"></i> 磁盘</span>
            <span>${data.disk || 0}%</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width: ${data.disk || 0}%"></div></div>
        <div class="stat-item">
            <span><i class="fa-regular fa-clock"></i> 运行时长</span>
            <span>${data.uptime || 0} 小时</span>
        </div>
    `;
    document.getElementById(containerId).innerHTML = html;
}