// frontend/js/cards/zblog-card.js
/**
 * Z-Blog 卡片组件
 */
var ZblogCard = {
    name: 'zblog',
    
    render: function(cardId, data) {
        if (!data) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>数据为空</p></div>';
        }
        
        if (data.error) {
            return '<div class="error-card"><i class="fa-solid fa-circle-exclamation"></i><p>' + escapeHtml(data.error) + '</p><button class="btn-slate" onclick="window.parent.postMessage({type:\'navigate\', url:\'/pages/admin.html\'}, \'*\')">去配置</button></div>';
        }
        
        if (!data.categories || data.categories.length === 0) {
            return '<div class="empty-card"><i class="fa-solid fa-blog"></i><p>暂无分类数据，请检查 Z-Blog 配置</p></div>';
        }
        
        var categoriesHtml = '<div class="zblog-grid">';
        
        for (var i = 0; i < data.categories.length; i++) {
            var cat = data.categories[i];
            var catName = cat.name || '未命名分类';
            var posts = cat.posts || [];
            
            categoriesHtml += '<div class="zblog-category">';
            categoriesHtml += '<div class="zblog-cat-title"><i class="fa-solid fa-folder"></i> ' + escapeHtml(catName) + '</div>';
            categoriesHtml += '<ul class="zblog-post-list">';
            
            if (posts.length > 0) {
                for (var j = 0; j < posts.length; j++) {
                    var post = posts[j];
                    var postTitle = post.title || '无标题';
                    var postUrl = post.url || '#';
                    var postThumb = post.thumbnail || '';
                    
                    var thumbHtml = postThumb ? 
                        '<img src="' + escapeHtml(postThumb) + '" class="zblog-thumb">' : 
                        '<div class="zblog-thumb-placeholder"><i class="fa-regular fa-file-lines"></i></div>';
                    
                    categoriesHtml += '<li class="zblog-post-item">';
                    categoriesHtml += '<a href="' + escapeHtml(postUrl) + '" target="_blank" class="zblog-post-link">';
                    categoriesHtml += '<span class="zblog-thumb-wrapper">' + thumbHtml + '</span>';
                    categoriesHtml += '<span class="zblog-post-title">' + escapeHtml(postTitle) + '</span>';
                    categoriesHtml += '</a>';
                    categoriesHtml += '</li>';
                }
            } else {
                categoriesHtml += '<li class="zblog-post-empty">暂无文章</li>';
            }
            
            categoriesHtml += '</ul>';
            categoriesHtml += '</div>';
        }
        
        categoriesHtml += '</div>';
        return categoriesHtml;
    }
};

window.ZblogCard = ZblogCard;

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