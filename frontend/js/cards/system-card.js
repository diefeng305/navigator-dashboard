// frontend/js/cards/system-card.js
/**
 * 系统状态卡片组件
 * 支持本地系统和 NAS 系统
 */
var SystemCard = {
    name: 'system',
    
    render: function(cardId, data) {
        if (!data) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>数据为空</p></div>';
        }
        
        if (data.error) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>' + escapeHtml(data.error) + '</p><button class="btn-slate" onclick="window.parent.postMessage({type:\'navigate\', url:\'/pages/admin.html\'}, \'*\')">去配置</button></div>';
        }
        
        // 判断是 NAS 模式还是本地模式
        var isNas = data.mode === 'nas';
        var nasType = data.nas_type || '';
        var nasTypeLabels = {
            'synology': '群晖',
            'fnos': '飞牛',
            'qnap': '威联通',
            'unraid': 'Unraid'
        };
        var nasTypeLabel = nasTypeLabels[nasType] || nasType;
        
        // 构建统计信息
        var html = '';
        
        // NAS 模式显示类型标签
        if (isNas && nasTypeLabel) {
            html += '<div class="system-nas-badge"><i class="fa-solid fa-server"></i> ' + escapeHtml(nasTypeLabel) + '</div>';
        }
        
        // CPU
        var cpuValue = data.cpu || 0;
        html += '<div class="stat-row"><span><i class="fa-solid fa-cpu"></i> CPU</span><span>' + cpuValue + '%</span></div>';
        html += '<div class="progress-bar"><div class="progress-fill" style="width: ' + cpuValue + '%"></div></div>';
        
        // 内存
        var memoryValue = data.memory || 0;
        html += '<div class="stat-row"><span><i class="fa-solid fa-memory"></i> 内存</span><span>' + memoryValue + '%</span></div>';
        html += '<div class="progress-bar"><div class="progress-fill" style="width: ' + memoryValue + '%"></div></div>';
        
        // 磁盘
        var diskValue = data.disk || 0;
        html += '<div class="stat-row"><span><i class="fa-solid fa-hard-drive"></i> 磁盘</span><span>' + diskValue + '%</span></div>';
        html += '<div class="progress-bar"><div class="progress-fill" style="width: ' + diskValue + '%"></div></div>';
        
        // 运行时长（如果有）
        if (data.uptime && data.uptime > 0) {
            html += '<div class="stat-row"><span><i class="fa-regular fa-clock"></i> 运行时长</span><span>' + data.uptime + ' 小时</span></div>';
        }
        
        // ========== 温度信息 ==========
        var hasTemp = false;
        
        // 系统温度
        if (data.system_temp !== undefined && data.system_temp !== null) {
            hasTemp = true;
            var tempColor = data.system_temp > 60 ? '#ef4444' : '#00f0ff';
            html += '<div class="stat-row temp-row"><span><i class="fa-solid fa-thermometer-half"></i> 系统温度</span><span style="color:' + tempColor + '; font-weight:600;">' + data.system_temp + '°C</span></div>';
        }
        
        // CPU 温度（如果与系统温度不同）
        if (data.cpu_temp !== undefined && data.cpu_temp !== null && data.cpu_temp !== data.system_temp) {
            hasTemp = true;
            var cpuTempColor = data.cpu_temp > 60 ? '#ef4444' : '#00f0ff';
            html += '<div class="stat-row temp-row"><span><i class="fa-solid fa-microchip"></i> CPU 温度</span><span style="color:' + cpuTempColor + '; font-weight:600;">' + data.cpu_temp + '°C</span></div>';
        }
        
        // 磁盘温度列表
        if (data.disk_temps && data.disk_temps.length > 0) {
            hasTemp = true;
            for (var i = 0; i < data.disk_temps.length; i++) {
                var disk = data.disk_temps[i];
                var diskTempColor = disk.temperature > 60 ? '#ef4444' : '#00f0ff';
                html += '<div class="stat-row temp-row"><span><i class="fa-solid fa-hdd"></i> ' + escapeHtml(disk.name) + '</span><span style="color:' + diskTempColor + '; font-weight:600;">' + disk.temperature + '°C</span></div>';
            }
        }
        
        // 如果没有温度数据，显示提示
        if (!hasTemp && isNas) {
            html += '<div class="stat-row temp-row" style="color:#64748b; font-size:12px;"><span><i class="fa-solid fa-info-circle"></i> 温度数据</span><span>暂不可用</span></div>';
        }
        
        return html;
    }
};

window.SystemCard = SystemCard;

// 确保 escapeHtml 可用
if (typeof escapeHtml === 'undefined') {
    window.escapeHtml = function(str) {
        if (!str) return '';
        return String(str).replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    };
}