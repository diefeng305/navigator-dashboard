// frontend/js/cards/emby-card.js
/**
 * Emby 卡片组件
 * 
 * 独立文件，修改此文件不影响 home.html
 */
var EmbyCard = {
    name: 'emby',
    
    render: function(cardId, data) {
        if (!data) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>数据为空</p></div>';
        }
        
        if (data.error) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>' + escapeHtml(data.error) + '</p><button class="btn-slate" onclick="window.parent.postMessage({type:\'navigate\', url:\'/pages/admin.html\'}, \'*\')">去配置</button></div>';
        }
        
        if (!data.items || data.items.length === 0) {
            return '<div class="empty-card"><i class="fa-solid fa-film"></i><p>暂无内容</p></div>';
        }
        
        var typeLabels = {
            'all': '全部',
            'movie': '电影',
            'shows': '剧集',
            'tv': '电视节目',
            'video': '视频',
            'music': '音乐',
            'photo': '照片',
            'boxset': '合集'
        };
        
        var currentType = data.media_type || 'all';
        var availableTypes = data.available_types || ['all', 'movie', 'shows', 'tv', 'video', 'music', 'photo', 'boxset'];
        
        // 生成筛选下拉菜单
        var filterHtml = '<select class="emby-type-filter" data-card-id="' + cardId + '">';
        for (var i = 0; i < availableTypes.length; i++) {
            var type = availableTypes[i];
            var label = typeLabels[type] || type;
            var selected = type === currentType ? 'selected' : '';
            filterHtml += '<option value="' + type + '" ' + selected + '>' + label + '</option>';
        }
        filterHtml += '</select>';
        
        // 存储到全局供 home.html 使用
        window._embyFilterHtml = filterHtml;
        
        // 卡片内容
        var contentHtml = '<div class="media-card-container" data-card-id="' + cardId + '">';
        contentHtml += '<div class="media-scroll-wrapper" id="media-scroll-' + cardId + '">';
        contentHtml += '<div class="media-horizontal-list">';
        
        for (var j = 0; j < data.items.length; j++) {
            var item = data.items[j];
            var itemUrl = item.url || '#';
            var itemImage = item.image_url || '';
            var itemName = item.name || '未知';
            var itemYear = item.year || '';
            
            contentHtml += '<div class="media-item" onclick="window.open(\'' + escapeHtml(itemUrl) + '\', \'_blank\')">';
            contentHtml += '<img src="' + escapeHtml(itemImage) + '" onerror="this.src=\'https://placehold.co/140x200/1e293b/64748b?text=No+Image\'">';
            contentHtml += '<div class="media-title" title="' + escapeHtml(itemName) + '">' + escapeHtml(itemName) + '</div>';
            if (itemYear) {
                contentHtml += '<div class="media-year">' + escapeHtml(itemYear) + '</div>';
            }
            contentHtml += '</div>';
        }
        
        contentHtml += '</div></div>';
        contentHtml += '<button class="card-scroll-btn card-scroll-left" data-card-id="' + cardId + '"><i class="fa-solid fa-chevron-left"></i></button>';
        contentHtml += '<button class="card-scroll-btn card-scroll-right" data-card-id="' + cardId + '"><i class="fa-solid fa-chevron-right"></i></button>';
        contentHtml += '</div>';
        
        return contentHtml;
    },
    
    // 筛选功能 - 只刷新当前卡片
    filter: function(cardId, mediaType) {
        this.saveFilter(cardId, mediaType);
    },
    
    saveFilter: async function(cardId, mediaType) {
        try {
            // 1. 获取当前卡片数据
            var response = await fetch('/api/home/cards/data');
            var cards = await response.json();
            var card = null;
            for (var i = 0; i < cards.length; i++) {
                if (cards[i].id == cardId) {
                    card = cards[i];
                    break;
                }
            }
            if (!card) return;
            
            // 2. 更新 display_config
            var displayConfig = card.display_config || {};
            displayConfig.media_type = mediaType;
            
            // 3. 保存到服务器
            await fetch('/api/home/cards/' + cardId, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: card.title,
                    card_type: card.card_type,
                    api_url: card.api_url,
                    api_key: card.api_key,
                    refresh_interval: card.refresh_interval || 60,
                    sort_order: card.sort_order || 0,
                    display_config: displayConfig,
                    enabled: card.enabled
                })
            });
            
            // 4. 只获取这一张卡片的最新数据
            var singleResponse = await fetch('/api/home/cards/single/' + cardId);
            if (!singleResponse.ok) throw new Error('获取卡片数据失败');
            var newCardData = await singleResponse.json();
            
            // 5. 只更新这个卡片，不刷新整个页面
            this.updateCard(cardId, newCardData);
            
        } catch (error) {
            console.error('筛选失败:', error);
            // 降级方案：刷新整个页面
            if (typeof loadCardsData === 'function') {
                loadCardsData();
            }
        }
    },
    
    // 更新单个卡片
    updateCard: function(cardId, cardData) {
        var cardElement = document.querySelector('.dashboard-card[data-card-id="' + cardId + '"]');
        if (!cardElement) return;
        
        // 获取组件数据
        var componentName = cardData.data.component || 'emby';
        var componentData = cardData.data.data || {};
        var cardTitle = cardData.title || '未命名卡片';
        
        // 重新渲染卡片内容
        var bodyHtml = this.render(cardId, componentData);
        
        // 获取筛选HTML
        var filterHtml = '';
        if (window._embyFilterHtml) {
            filterHtml = window._embyFilterHtml;
            window._embyFilterHtml = null;
        }
        
        // 构建新的卡片头部
        var headerHtml = '<div class="card-header">' +
            '<div class="card-title-section">' +
            '<i class="fa-solid fa-film"></i>' +
            '<h3>' + escapeHtml(cardTitle) + '</h3>' +
            '</div>';
        
        if (filterHtml) {
            headerHtml += '<div class="card-header-filter">' + filterHtml + '</div>';
        }
        
        headerHtml += '</div>';
        
        // 替换卡片内容（保留卡片外层容器）
        var newCardHtml = headerHtml + '<div class="card-body">' + bodyHtml + '</div>';
        cardElement.innerHTML = newCardHtml;
        
        // 重新绑定事件
        this.bindEvents(cardId);
    },
    
    // 绑定卡片内部事件
    bindEvents: function(cardId) {
        var cardElement = document.querySelector('.dashboard-card[data-card-id="' + cardId + '"]');
        if (!cardElement) return;
        
        // 滚动按钮
        var scrollBtns = cardElement.querySelectorAll('.card-scroll-btn');
        for (var i = 0; i < scrollBtns.length; i++) {
            var btn = scrollBtns[i];
            btn.onclick = function(e) {
                e.stopPropagation();
                var scrollWrapper = document.getElementById('media-scroll-' + cardId);
                if (!scrollWrapper) return;
                var direction = this.classList.contains('card-scroll-left') ? -280 : 280;
                scrollWrapper.scrollBy({ left: direction, behavior: 'smooth' });
            };
        }
        
        // 筛选下拉
        var filterSelect = cardElement.querySelector('.emby-type-filter');
        if (filterSelect) {
            filterSelect.onchange = function() {
                var mediaType = this.value;
                if (window.EmbyCard && typeof window.EmbyCard.filter === 'function') {
                    window.EmbyCard.filter(cardId, mediaType);
                }
            };
        }
    }
};

// 注册到全局
window.EmbyCard = EmbyCard;

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