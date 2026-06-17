// 完整农历日历组件 - 支持农历显示和节假日

class LunarCalendar {
    constructor() {
        // 农历数据 (1900-2100)
        this.lunarInfo = [
            0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
            0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
            0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
            0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
            0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
            0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
            0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
            0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
            0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
            0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
            0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
            0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x05176, 0x052b0, 0x0a930,
            0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
            0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
            0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0
        ];
        
        this.nStr1 = ['日', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'];
        this.nStr2 = ['初', '十', '廿', '卅'];
        
        // 节气数据 (2020-2030 简化版，实际可根据需要扩展)
        this.solarTerms = {
            '小寒': [5, 6], '大寒': [20, 21], '立春': [3, 4, 5], '雨水': [18, 19], '惊蛰': [5, 6],
            '春分': [20, 21], '清明': [4, 5], '谷雨': [19, 20], '立夏': [5, 6], '小满': [20, 21],
            '芒种': [5, 6], '夏至': [21, 22], '小暑': [7, 8], '大暑': [22, 23], '立秋': [7, 8],
            '处暑': [22, 23], '白露': [7, 8], '秋分': [22, 23], '寒露': [8, 9], '霜降': [23, 24],
            '立冬': [7, 8], '小雪': [22, 23], '大雪': [7, 8], '冬至': [21, 22]
        };
        
        // 节假日数据 (固定日期)
        this.festivals = {
            '1-1': '元旦',
            '2-14': '情人节',
            '3-8': '妇女节',
            '3-12': '植树节',
            '4-1': '愚人节',
            '5-1': '劳动节',
            '5-4': '青年节',
            '6-1': '儿童节',
            '7-1': '建党节',
            '8-1': '建军节',
            '9-10': '教师节',
            '10-1': '国庆节',
            '10-31': '万圣节',
            '11-11': '光棍节',
            '12-25': '圣诞节'
        };
        
        // 农历节日
        this.lunarFestivals = {
            '1-1': '春节',
            '1-15': '元宵节',
            '2-2': '龙抬头',
            '5-5': '端午节',
            '7-7': '七夕节',
            '8-15': '中秋节',
            '9-9': '重阳节',
            '12-8': '腊八节',
            '12-23': '小年',
            '12-30': '除夕'
        };
    }

    // 获取农历年份信息
    getLunarYearInfo(year) {
        return this.lunarInfo[year - 1900];
    }

    // 获取农历月份天数
    getLunarMonthDays(year, month) {
        const info = this.getLunarYearInfo(year);
        if (month > 12 || month < 1) return 0;
        return (info & (0x10000 >> month)) ? 30 : 29;
    }

    // 获取农历闰月
    getLeapMonth(year) {
        return this.getLunarYearInfo(year) & 0xf;
    }

    // 获取农历闰月天数
    getLeapMonthDays(year) {
        const info = this.getLunarYearInfo(year);
        return (info & 0x10000) ? 30 : 29;
    }

    // 获取农历年总天数
    getLunarYearDays(year) {
        let sum = 348;
        for (let i = 0x8000; i > 0x8; i >>= 1) {
            sum += (this.getLunarYearInfo(year) & i) ? 1 : 0;
        }
        return sum + this.getLeapMonthDays(year);
    }

    // 公历转农历
    solarToLunar(date) {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        
        // 计算从1900年1月31日到当前日期的天数
        const baseDate = new Date(1900, 0, 31);
        let offset = Math.floor((date - baseDate) / (24 * 60 * 60 * 1000));
        
        let i = 1900;
        let temp = 0;
        let lunarYear = 1900;
        for (i = 1900; i <= 2100; i++) {
            temp = this.getLunarYearDays(i);
            if (offset - temp < 1) break;
            offset -= temp;
        }
        lunarYear = i;
        
        let leap = this.getLeapMonth(lunarYear);
        let isLeap = false;
        let lunarMonth = 1;
        
        for (let j = 1; j <= 12; j++) {
            if (leap > 0 && j === leap + 1 && !isLeap) {
                j--;
                isLeap = true;
                temp = this.getLeapMonthDays(lunarYear);
            } else {
                temp = this.getLunarMonthDays(lunarYear, j);
            }
            
            if (offset < temp) break;
            offset -= temp;
            lunarMonth = j + 1;
        }
        
        if (leap > 0 && lunarMonth > leap && !isLeap) {
            lunarMonth--;
        }
        
        return {
            year: lunarYear,
            month: lunarMonth,
            day: offset + 1,
            isLeap: isLeap,
            monthName: this.getLunarMonthName(lunarMonth, isLeap),
            dayName: this.getLunarDayName(offset + 1)
        };
    }
    
    getLunarMonthName(month, isLeap) {
        const monthNames = ['正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
        return (isLeap ? '闰' : '') + monthNames[month - 1];
    }
    
    getLunarDayName(day) {
        if (day === 0) return '';
        if (day <= 10) {
            return this.nStr2[0] + this.nStr1[day];
        } else if (day === 20) {
            return this.nStr2[2] + this.nStr1[10];
        } else if (day === 30) {
            return this.nStr2[3] + this.nStr1[10];
        } else {
            const tens = Math.floor(day / 10);
            const ones = day % 10;
            return this.nStr2[tens] + (ones === 0 ? this.nStr1[10] : this.nStr1[ones]);
        }
    }
    
    // 获取节气
    getSolarTerm(year, month, day) {
        // 简化节气判断
        const termMap = {
            '1-5': '小寒', '1-20': '大寒', '2-4': '立春', '2-19': '雨水',
            '3-5': '惊蛰', '3-20': '春分', '4-4': '清明', '4-20': '谷雨',
            '5-5': '立夏', '5-21': '小满', '6-6': '芒种', '6-21': '夏至',
            '7-7': '小暑', '7-22': '大暑', '8-7': '立秋', '8-23': '处暑',
            '9-7': '白露', '9-22': '秋分', '10-8': '寒露', '10-23': '霜降',
            '11-7': '立冬', '11-22': '小雪', '12-7': '大雪', '12-21': '冬至'
        };
        const key = `${month}-${day}`;
        return termMap[key] || '';
    }
    
    // 获取节假日
    getFestival(year, month, day, lunar) {
        const solarKey = `${month}-${day}`;
        const lunarKey = `${lunar.month}-${lunar.day}`;
        
        // 检查公历节日
        if (this.festivals[solarKey]) {
            return this.festivals[solarKey];
        }
        
        // 检查农历节日
        if (this.lunarFestivals[lunarKey] && !lunar.isLeap) {
            return this.lunarFestivals[lunarKey];
        }
        
        return '';
    }
    
    // 获取生肖
    getZodiac(year) {
        const zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
        return zodiacs[(year - 4) % 12];
    }
}

// 日历弹窗组件
class CalendarDialog {
    constructor() {
        this.calendar = new LunarCalendar();
        this.currentDate = new Date();
        this.isOpen = false;
        this.createDialog();
    }
    
    createDialog() {
        const dialog = document.createElement('div');
        dialog.className = 'calendar-dialog-overlay';
        dialog.id = 'calendarDialog';
        dialog.innerHTML = `
            <div class="calendar-dialog">
                <div class="calendar-header">
                    <button class="calendar-nav prev-month"><i class="fa-solid fa-chevron-left"></i></button>
                    <span class="calendar-title"></span>
                    <button class="calendar-nav next-month"><i class="fa-solid fa-chevron-right"></i></button>
                    <button class="calendar-close"><i class="fa-solid fa-times"></i></button>
                </div>
                <div class="calendar-weekdays">
                    <span>日</span><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span>
                </div>
                <div class="calendar-days" id="calendarDays"></div>
                <div class="calendar-footer" id="calendarFooter"></div>
            </div>
        `;
        document.body.appendChild(dialog);
        
        dialog.querySelector('.prev-month').onclick = () => this.changeMonth(-1);
        dialog.querySelector('.next-month').onclick = () => this.changeMonth(1);
        dialog.querySelector('.calendar-close').onclick = () => this.close();
        dialog.onclick = (e) => { if (e.target === dialog) this.close(); };
        
        this.dialog = dialog;
    }
    
    open() {
        if (!this.isOpen) {
            this.currentDate = new Date();
            this.render();
            this.dialog.style.display = 'flex';
            this.isOpen = true;
        }
    }
    
    close() {
        if (this.isOpen) {
            this.dialog.style.display = 'none';
            this.isOpen = false;
        }
    }
    
    changeMonth(delta) {
        this.currentDate.setMonth(this.currentDate.getMonth() + delta);
        this.render();
    }
    
    render() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        const today = new Date();
        
        // 更新标题
        this.dialog.querySelector('.calendar-title').textContent = `${year}年 ${month + 1}月`;
        
        // 获取当月第一天和最后一天
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const startDayOfWeek = firstDay.getDay();
        const daysInMonth = lastDay.getDate();
        
        // 生成日历格子
        let html = '';
        
        // 填充空白
        for (let i = 0; i < startDayOfWeek; i++) {
            html += '<div class="calendar-day empty"></div>';
        }
        
        // 存储有节假日的日期信息
        let holidayInfo = [];
        
        // 填充日期
        for (let d = 1; d <= daysInMonth; d++) {
            const date = new Date(year, month, d);
            const isToday = this.isToday(date);
            const lunar = this.calendar.solarToLunar(date);
            const solarTerm = this.calendar.getSolarTerm(year, month + 1, d);
            const festival = this.calendar.getFestival(year, month + 1, d, lunar);
            
            let extraClass = '';
            let festivalHtml = '';
            
            if (festival) {
                extraClass = 'has-festival';
                festivalHtml = `<span class="festival-badge">${festival}</span>`;
                holidayInfo.push({ date: d, festival, lunar: lunar.dayName });
            } else if (solarTerm) {
                extraClass = 'has-term';
                festivalHtml = `<span class="term-badge">${solarTerm}</span>`;
            }
            
            if (d === 1) extraClass += ' first-day';
            
            html += `
                <div class="calendar-day ${isToday ? 'today' : ''} ${extraClass}" 
                     data-year="${year}" data-month="${month}" data-day="${d}"
                     data-lunar="${lunar.monthName}${lunar.dayName}"
                     data-festival="${festival || ''}">
                    <span class="solar-day">${d}</span>
                    <span class="lunar-day">${lunar.dayName}</span>
                    ${festivalHtml}
                </div>
            `;
        }
        
        this.dialog.querySelector('.calendar-days').innerHTML = html;
        
        // 更新底部农历信息
        const now = new Date();
        const currentLunar = this.calendar.solarToLunar(now);
        const currentFestival = this.calendar.getFestival(now.getFullYear(), now.getMonth() + 1, now.getDate(), currentLunar);
        const zodiac = this.calendar.getZodiac(now.getFullYear());
        
        let footerHtml = `
            <div style="line-height:1.6;">
                <div><strong>农历</strong> ${currentLunar.monthName}${currentLunar.dayName}</div>
                <div><strong>生肖</strong> ${zodiac}年</div>
        `;
        
        if (currentFestival) {
            footerHtml += `<div><strong>今日节日</strong> ${currentFestival}</div>`;
        }
        
        footerHtml += `</div>`;
        this.dialog.querySelector('.calendar-footer').innerHTML = footerHtml;
        
        // 绑定点击事件
        document.querySelectorAll('.calendar-day:not(.empty)').forEach(day => {
            day.onclick = () => {
                const year = parseInt(day.dataset.year);
                const month = parseInt(day.dataset.month);
                const dayNum = parseInt(day.dataset.day);
                const lunarInfo = day.dataset.lunar || '';
                const festival = day.dataset.festival || '';
                const date = new Date(year, month, dayNum);
                const lunar = this.calendar.solarToLunar(date);
                const zodiacSign = this.calendar.getZodiac(year);
                const solarTerm = this.calendar.getSolarTerm(year, month + 1, dayNum);
                
                let infoHtml = `
                    <div style="line-height:1.8;">
                        <div><strong>📅 ${year}年${month+1}月${dayNum}日</strong></div>
                        <div><strong>🌙 农历</strong> ${lunar.monthName}${lunar.dayName}</div>
                        <div><strong>🐉 生肖</strong> ${zodiacSign}年</div>
                `;
                
                if (festival) {
                    infoHtml += `<div><strong>🎉 节日</strong> ${festival}</div>`;
                }
                
                if (solarTerm) {
                    infoHtml += `<div><strong>🌱 节气</strong> ${solarTerm}</div>`;
                }
                
                infoHtml += `</div>`;
                this.dialog.querySelector('.calendar-footer').innerHTML = infoHtml;
                
                // 高亮选中日期
                document.querySelectorAll('.calendar-day').forEach(d => d.classList.remove('selected'));
                day.classList.add('selected');
            }.bind(this);
        });
    }
    
    isToday(date) {
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }
}

// 全局日历实例
let calendarDialog = null;

// 初始化日历
function initCalendar() {
    if (!calendarDialog) {
        calendarDialog = new CalendarDialog();
    }
}

// 打开日历
function openCalendar() {
    if (!calendarDialog) {
        initCalendar();
    }
    calendarDialog.open();
}