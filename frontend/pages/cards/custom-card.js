// 自定义API卡片渲染函数
function renderCustomCard(data, containerId) {
    const html = `<pre style="font-size:12px;color:#94a3b8;overflow-x:auto;">${JSON.stringify(data, null, 2)}</pre>`;
    document.getElementById(containerId).innerHTML = html;
}