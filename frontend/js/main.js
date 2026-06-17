document.addEventListener('DOMContentLoaded', () => {
    const navList = document.getElementById('navList');
    const pageFrame = document.getElementById('pageFrame');
    const loader = document.getElementById('iframeLoader');
    const logoArea = document.getElementById('logoArea');
    const logoTextDisplay = document.getElementById('logoTextDisplay');
    const userArea = document.getElementById('userArea');
    const userDropdown = document.getElementById('userDropdown');
    const overlay = document.getElementById('modalOverlay');
    const loginModal = document.getElementById('loginModal');
    
    const dropdownChangePwdBtn = document.getElementById('dropdownChangePwdBtn');
    const dropdownAdminBtn = document.getElementById('dropdownAdminBtn');
    const dropdownLogoutBtn = document.getElementById('dropdownLogoutBtn');

    const loginUser = document.getElementById('loginUser');
    const loginPass = document.getElementById('loginPass');
    const submitLogin = document.getElementById('submitLogin');

    let currentUserRole = localStorage.getItem('nav_role') || 'visitor';
    let currentUsername = localStorage.getItem('nav_user') || '';
    let menuItems = [];
    
    let isRestoringState = false;

    function restoreSavedPage() {
        const savedPage = localStorage.getItem('currentPage');
        if (savedPage && savedPage !== '/pages/home.html' && savedPage !== 'null') {
            isRestoringState = true;
            pageFrame.src = savedPage;
            setTimeout(() => { isRestoringState = false; }, 500);
        }
    }

    function saveCurrentPage(url) {
        if (isRestoringState) return;
        if (url && url !== '/pages/home.html' && url !== 'about:blank') {
            localStorage.setItem('currentPage', url);
        } else if (url === '/pages/home.html') {
            localStorage.setItem('currentPage', '/pages/home.html');
        }
    }

    pageFrame.addEventListener('load', () => {
        loader.style.opacity = '0';
        setTimeout(() => { loader.style.display = 'none'; }, 200);
        if (!isRestoringState && pageFrame.src && !pageFrame.src.includes('about:blank')) {
            const urlPath = pageFrame.src.replace(window.location.origin, '');
            if (urlPath !== localStorage.getItem('currentPage')) {
                localStorage.setItem('currentPage', urlPath);
            }
        }
    });

    window.addEventListener('message', (event) => {
        const data = event.data;
        if (!data) return;
        switch (data.type) {
            case 'openLink':
                if (data.url && data.url !== '#') window.open(data.url, '_blank');
                break;
            case 'refreshMenu':
                initSystem();
                break;
            case 'refreshConfig':
                fetch('/api/config').then(res => res.json()).then(config => updateBranding(config));
                break;
            case 'applyTheme':
                if (data.colors) applyTheme(data.colors);
                break;
            case 'applyEffects':
                if (data.effects) applyEffectSettings(data.effects);
                break;
            case 'navigate':
                if (data.url) {
                    loader.style.display = 'flex';
                    loader.style.opacity = '1';
                    pageFrame.src = data.url;
                    saveCurrentPage(data.url);
                }
                break;
        }
    });

    function applyTheme(colors) {
        document.body.style.backgroundColor = colors.bg;
        const sidebar = document.querySelector('.organizr-sidebar');
        if (sidebar) sidebar.style.backgroundColor = colors.sidebarBg;
        const topNav = document.querySelector('.top-navbar');
        if (topNav) topNav.style.backgroundColor = colors.sidebarBg;
        const brandLogo = document.querySelector('.brand-logo');
        if (brandLogo) brandLogo.style.background = `linear-gradient(135deg, ${colors.primary}, ${colors.accent})`;
        
        // 同步更新登录弹窗边框颜色
        const loginModalEl = document.getElementById('loginModal');
        if (loginModalEl) {
            loginModalEl.style.borderColor = `${colors.primary}80`;
        }
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            .menu-item-row.active::before, .sub-item-row.active::before {
                background-color: ${colors.primary};
                box-shadow: 0 0 14px ${colors.primary};
            }
            .user-status-area:hover, .user-status-area.active { border-color: ${colors.primary}; }
            .badge { background: rgba(${hexToRgb(colors.primary)}, 0.1); color: ${colors.primary}; }
            .modal-body .form-group input:focus { border-color: ${colors.primary}; box-shadow: 0 0 0 3px rgba(${hexToRgb(colors.primary)}, 0.1); }
            .modal-body .form-group input:focus ~ label, .modal-body .form-group input:valid ~ label { color: ${colors.primary}; }
            .modal-body .btn-cyan { background: linear-gradient(135deg, ${colors.primary}, ${colors.accent}); }
        `;
        const oldStyle = document.getElementById('dynamic-theme-style');
        if (oldStyle) oldStyle.remove();
        styleSheet.id = 'dynamic-theme-style';
        document.head.appendChild(styleSheet);
    }

    function hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}` : '0, 240, 255';
    }

    function applyEffectSettings(effects) {
        if (effects.blur !== undefined) effects.blur ? document.body.classList.remove('no-blur') : document.body.classList.add('no-blur');
        if (effects.glow !== undefined) effects.glow ? document.body.classList.remove('no-glow') : document.body.classList.add('no-glow');
        if (effects.compact !== undefined) effects.compact ? document.body.classList.add('compact-mode') : document.body.classList.remove('compact-mode');
        if (effects.animation !== undefined) effects.animation ? document.body.classList.remove('no-animation') : document.body.classList.add('no-animation');
    }

    function updateBranding(config) {
        const sidebarTitle = config.sidebar_title || '飞牛私有云';
        const sidebarLetter = config.sidebar_letter || 'O';
        logoArea.textContent = sidebarLetter.toUpperCase();
        logoTextDisplay.textContent = sidebarTitle;
        const pageTitle = document.getElementById('pageTitle');
        if (pageTitle) { pageTitle.textContent = sidebarTitle; document.title = sidebarTitle; }
    }

    function initSystem() {
        Promise.all([
            fetch('/api/config').then(res => res.json()),
            fetch(`/api/navigation?role=${currentUserRole}`).then(res => res.json())
        ]).then(([config, items]) => {
            updateBranding(config);
            menuItems = items;
            renderUserArea();
            buildOrganizrMenu(items);
            restoreSavedPage();
        }).catch(err => console.error('初始化失败:', err));
    }

    function handlePageOpen(item, element) {
        document.querySelectorAll('.menu-item-row, .sub-item-row').forEach(el => el.classList.remove('active'));
        if (element) element.classList.add('active');
        let pageUrl = null;
        if (item.url === '#dashboard_home') pageUrl = '/pages/home.html';
        else if (item.open_type === 'blank') { window.open(item.url, '_blank'); return; }
        else pageUrl = item.url;
        if (pageUrl) {
            loader.style.display = 'flex';
            loader.style.opacity = '1';
            pageFrame.src = pageUrl;
            saveCurrentPage(pageUrl);
        }
    }

    function openAdminPanel() {
        if (currentUserRole !== 'admin') { alert('您没有权限访问系统设置'); return; }
        loader.style.display = 'flex'; loader.style.opacity = '1';
        pageFrame.src = '/pages/admin.html';
        saveCurrentPage('/pages/admin.html');
        document.querySelectorAll('.menu-item-row, .sub-item-row').forEach(el => el.classList.remove('active'));
    }

    function renderUserArea() {
        userArea.innerHTML = '';
        const userIcon = currentUserRole === 'admin' ? 'fa-user-gear' : 'fa-user';
        userArea.innerHTML = `<i class="fa-solid ${userIcon}" style="color: #00f0ff; font-size:13px;"></i>
            <span style="font-size:13px; font-weight:500; color:#cbd5e1; margin-left: 5px;">
                ${currentUserRole === 'visitor' ? '账户登录' : currentUsername}
            </span>`;
    }

    userArea.addEventListener('click', (e) => {
        e.stopPropagation();
        if (currentUserRole === 'visitor') { overlay.style.display = 'block'; loginModal.style.display = 'block'; loginUser.focus(); }
        else { userDropdown.classList.toggle('show'); userArea.classList.toggle('active'); }
    });

    if (dropdownAdminBtn) dropdownAdminBtn.addEventListener('click', () => {
        userDropdown.classList.remove('show'); userArea.classList.remove('active'); openAdminPanel();
    });

    dropdownLogoutBtn.addEventListener('click', () => {
        userDropdown.classList.remove('show'); userArea.classList.remove('active');
        if (confirm('确定安全退出当前会话？')) { localStorage.clear(); location.reload(); }
    });

    document.addEventListener('click', () => { userDropdown.classList.remove('show'); userArea.classList.remove('active'); });

    function executeFormLogin() {
        const u = loginUser.value.trim();
        const p = loginPass.value;
        if (!u || !p) return;
        fetch('/api/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: u, password: p }) })
            .then(res => res.json()).then(data => {
                if (data.success) { localStorage.setItem('nav_role', data.role); localStorage.setItem('nav_user', data.username); location.reload(); }
                else alert(data.message);
            }).catch(err => alert('登录失败: ' + err.message));
    }

    submitLogin.addEventListener('click', executeFormLogin);
    loginUser.addEventListener('keydown', (e) => { if (e.key === 'Enter') loginPass.focus(); });
    loginPass.addEventListener('keydown', (e) => { if (e.key === 'Enter') executeFormLogin(); });
    document.getElementById('closeLogin').addEventListener('click', () => { overlay.style.display = 'none'; loginModal.style.display = 'none'; });

    function buildOrganizrMenu(items) {
        navList.innerHTML = '';
        const homeLi = document.createElement('li');
        homeLi.className = 'menu-item-row';
        homeLi.setAttribute('data-item-id', 'home');
        homeLi.innerHTML = `<div class="item-left-group"><i class="fa-solid fa-house sidebar-icon-fa"></i><span class="nav-title">首页</span></div>`;
        homeLi.addEventListener('click', () => handlePageOpen({ url: '#dashboard_home' }, homeLi));
        navList.appendChild(homeLi);

        const roots = items.filter(item => item.parent_id === 0);
        roots.forEach(root => {
            const children = items.filter(item => item.parent_id === root.id);
            const isFa = (!root.icon || root.icon.startsWith('fa-'));
            const iconHtml = isFa ? `<i class="${root.icon || 'fa-solid fa-globe'} sidebar-icon-fa"></i>` : `<img src="${root.icon}" class="sidebar-icon-custom">`;
            if (children.length > 0) {
                const li = document.createElement('li');
                li.className = 'nav-category-block';
                li.innerHTML = `<div class="menu-item-row"><div class="item-left-group">${iconHtml}<span class="nav-title">${root.title}</span></div><span class="arrow-indicator">➔</span></div><ul class="sub-menu-list"></ul>`;
                const subList = li.querySelector('.sub-menu-list');
                children.forEach(child => {
                    const childIsFa = (!child.icon || child.icon.startsWith('fa-'));
                    const childIconHtml = childIsFa ? `<i class="${child.icon || 'fa-solid fa-link'} sidebar-icon-fa"></i>` : `<img src="${child.icon}" class="sidebar-icon-custom">`;
                    const subLi = document.createElement('li');
                    subLi.className = 'sub-item-row';
                    subLi.setAttribute('data-item-id', child.id);
                    subLi.innerHTML = `<div class="item-left-group">${childIconHtml}<span class="nav-title">${child.title}</span></div>`;
                    subLi.addEventListener('click', (e) => { e.stopPropagation(); handlePageOpen(child, subLi); });
                    subList.appendChild(subLi);
                });
                li.querySelector('.menu-item-row').addEventListener('click', () => li.classList.toggle('open'));
                navList.appendChild(li);
            } else {
                const li = document.createElement('li');
                li.className = 'menu-item-row';
                li.setAttribute('data-item-id', root.id);
                li.innerHTML = `<div class="item-left-group">${iconHtml}<span class="nav-title">${root.title}</span></div>`;
                li.addEventListener('click', () => handlePageOpen(root, li));
                navList.appendChild(li);
            }
        });
    }

    // 修改密码弹窗
    const changePwdModal = document.createElement('div');
    changePwdModal.className = 'organizr-modal';
    changePwdModal.id = 'changePwdModal';
    changePwdModal.innerHTML = `<div class="modal-header"><h4><i class="fa-solid fa-key"></i> 修改密码</h4><span class="close-icon" id="closeChangePwd">&times;</span></div>
        <div class="modal-body"><div class="form-group"><input type="password" id="oldPassword" required><label>原密码</label></div>
        <div class="form-group"><input type="password" id="newPassword1" required><label>新密码</label></div>
        <div class="form-group"><input type="password" id="newPassword2" required><label>确认新密码</label></div>
        <button class="btn-cyan" id="submitChangePwd" style="width:100%; padding:12px;">确认修改</button></div>`;
    document.body.appendChild(changePwdModal);
    if (dropdownChangePwdBtn) {
        dropdownChangePwdBtn.addEventListener('click', () => {
            userDropdown.classList.remove('show'); userArea.classList.remove('active');
            overlay.style.display = 'block'; changePwdModal.style.display = 'block';
            document.getElementById('oldPassword').value = ''; document.getElementById('newPassword1').value = ''; document.getElementById('newPassword2').value = '';
        });
    }
    document.getElementById('closeChangePwd')?.addEventListener('click', () => { overlay.style.display = 'none'; changePwdModal.style.display = 'none'; });
    document.getElementById('submitChangePwd')?.addEventListener('click', () => {
        const oldPwd = document.getElementById('oldPassword').value;
        const newPwd1 = document.getElementById('newPassword1').value;
        const newPwd2 = document.getElementById('newPassword2').value;
        if (!oldPwd || !newPwd1) return alert('请填写完整信息');
        if (newPwd1 !== newPwd2) return alert('两次输入的新密码不一致');
        if (newPwd1.length < 4) return alert('新密码长度至少4位');
        fetch('/api/users/change-password', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: currentUsername, old_password: oldPwd, new_password: newPwd1 })
        }).then(res => res.json()).then(data => {
            if (data.success) { alert('密码修改成功，请重新登录'); localStorage.clear(); location.reload(); }
            else alert(data.message || '修改失败');
        });
    });

    const savedTheme = localStorage.getItem('navigator_theme_config');
    if (savedTheme) { try { applyTheme(JSON.parse(savedTheme)); } catch(e) {} }
    const effects = {
        blur: localStorage.getItem('blurEffectToggle') !== 'false',
        glow: localStorage.getItem('glowEffectToggle') !== 'false',
        compact: localStorage.getItem('compactModeToggle') === 'true',
        animation: localStorage.getItem('iconAnimationToggle') !== 'false'
    };
    applyEffectSettings(effects);
    initSystem();
});