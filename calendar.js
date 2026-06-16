// calendar.js

// 대한민국 기준 공휴일 하드코딩 (2025~2027 기본 예시)
const holidays = {
    // 2025년
    "2025-01-01": "신정",
    "2025-01-28": "설날 연휴",
    "2025-01-29": "설날",
    "2025-01-30": "설날 연휴",
    "2025-03-01": "삼일절",
    "2025-03-03": "대체공휴일(삼일절)",
    "2025-05-05": "어린이날",
    "2025-05-05": "부처님오신날", 
    "2025-05-06": "대체공휴일",
    "2025-06-06": "현충일",
    "2025-08-15": "광복절",
    "2025-10-03": "개천절",
    "2025-10-05": "추석 연휴",
    "2025-10-06": "추석",
    "2025-10-07": "추석 연휴",
    "2025-10-08": "대체공휴일(추석)",
    "2025-10-09": "한글날",
    "2025-12-25": "기독탄신일(크리스마스)",
    
    // 2026년
    "2026-01-01": "신정",
    "2026-02-16": "설날 연휴",
    "2026-02-17": "설날",
    "2026-02-18": "설날 연휴",
    "2026-03-01": "삼일절",
    "2026-03-02": "대체공휴일",
    "2026-05-05": "어린이날",
    "2026-05-24": "부처님오신날",
    "2026-05-25": "대체공휴일",
    "2026-06-03": "지방 선거일",
    "2026-06-06": "현충일",
    "2026-07-17": "제헌절",
    "2026-08-15": "광복절",
    "2026-08-17": "대체공휴일(광복절)",
    "2026-09-24": "추석 연휴",
    "2026-09-25": "추석",
    "2026-09-26": "추석 연휴",
    "2026-09-28": "대체공휴일(추석)",
    "2026-10-03": "개천절",
    "2026-10-05": "대체공휴일(개천절)",
    "2026-10-09": "한글날",
    "2026-12-25": "기독탄신일(크리스마스)",
    
    // 2027년
    "2027-01-01": "신정",
    "2027-02-06": "설날 연휴",
    "2027-02-07": "설날",
    "2027-02-08": "설날 연휴",
    "2027-03-01": "삼일절",
    "2027-05-05": "어린이날",
    "2027-05-13": "부처님오신날",
    "2027-06-06": "현충일",
    "2027-08-15": "광복절",
    "2027-08-16": "대체공휴일",
    "2027-09-14": "추석 연휴",
    "2027-09-15": "추석",
    "2027-09-16": "추석 연휴",
    "2027-10-03": "개천절",
    "2027-10-09": "한글날",
    "2027-12-25": "기독탄신일"
};

let currentMonth = new Date();
let selectedDateStr = "";
let selectedScheduleId = null;

function getSchedules() {
    const data = localStorage.getItem('intranet_schedules');
    return data ? JSON.parse(data) : {};
}

function saveSchedulesToStorage(schedules) {
    localStorage.setItem('intranet_schedules', JSON.stringify(schedules));
}

function openCalendarModal() {
    currentMonth = new Date(); // 항상 열 때 현재 월로 렌더링
    renderCalendar();
    document.getElementById('calendar-modal-overlay').style.display = 'flex';
}

function closeCalendarModal() {
    document.getElementById('calendar-modal-overlay').style.display = 'none';
}

function changeMonth(delta) {
    currentMonth.setMonth(currentMonth.getMonth() + delta);
    renderCalendar();
}

function renderCalendar() {
    const year = currentMonth.getFullYear();
    const month = currentMonth.getMonth();
    
    document.getElementById('calendar-title').innerText = `${year}년 ${month + 1}월`;
    
    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();
    
    const today = new Date();
    const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    
    const calendarBody = document.getElementById('calendar-body');
    calendarBody.innerHTML = '';
    
    const schedules = getSchedules();
    
    // 빈 칸 렌더링
    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement('div');
        emptyDiv.className = 'calendar-day empty';
        calendarBody.appendChild(emptyDiv);
    }
    
    // 실제 날짜 렌더링
    for (let i = 1; i <= lastDate; i++) {
        const currentDayStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        const currentDayOfWeek = new Date(year, month, i).getDay();
        
        const dayDiv = document.createElement('div');
        dayDiv.className = 'calendar-day';
        if (currentDayOfWeek === 0) dayDiv.classList.add('sunday');
        if (currentDayOfWeek === 6) dayDiv.classList.add('saturday');
        if (currentDayStr === todayStr) dayDiv.classList.add('today');
        
        let holidayName = holidays[currentDayStr];
        if (holidayName) {
            dayDiv.classList.add('holiday');
        }
        
        let innerHTML = `<div class="calendar-date-number">${i}</div>`;
        if (holidayName) {
            innerHTML += `<div class="holiday-name">${holidayName}</div>`;
        }
        
        if (schedules[currentDayStr] && schedules[currentDayStr].length > 0) {
            schedules[currentDayStr].forEach((sch, idx) => {
                innerHTML += `<div class="schedule-item" onclick="event.stopPropagation(); openScheduleModal('${currentDayStr}', ${idx}, '${sch.title}')">${sch.title}</div>`;
            });
        }
        
        dayDiv.innerHTML = innerHTML;
        
        // 날짜 클릭 이벤트 -> 스케줄 등록 모달 오픈
        dayDiv.onclick = () => {
            openScheduleModal(currentDayStr, null, '');
        };
        
        calendarBody.appendChild(dayDiv);
    }
}

function openScheduleModal(dateStr, idx, title) {
    selectedDateStr = dateStr;
    selectedScheduleId = idx;
    
    document.getElementById('schedule-date-display').innerText = `${dateStr} 일정`;
    document.getElementById('schedule-date-input').value = dateStr;
    document.getElementById('schedule-title-input').value = title || '';
    
    if (idx !== null) {
        document.getElementById('schedule-modal-title').innerText = "일정 수정";
        document.getElementById('btn-delete-schedule').style.display = 'block';
    } else {
        document.getElementById('schedule-modal-title').innerText = "일정 등록";
        document.getElementById('btn-delete-schedule').style.display = 'none';
    }
    
    document.getElementById('schedule-modal-overlay').style.display = 'flex';
}

function closeScheduleModal() {
    document.getElementById('schedule-modal-overlay').style.display = 'none';
}

function saveSchedule() {
    const title = document.getElementById('schedule-title-input').value.trim();
    if (!title) {
        alert("일정 제목을 입력하세요.");
        return;
    }
    
    let schedules = getSchedules();
    if (!schedules[selectedDateStr]) {
        schedules[selectedDateStr] = [];
    }
    
    if (selectedScheduleId !== null) {
        schedules[selectedDateStr][selectedScheduleId].title = title;
    } else {
        schedules[selectedDateStr].push({ title: title });
    }
    
    saveSchedulesToStorage(schedules);
    closeScheduleModal();
    renderCalendar();
}

function deleteSchedule() {
    if (confirm("이 일정을 삭제하시겠습니까?")) {
        let schedules = getSchedules();
        if (schedules[selectedDateStr] && selectedScheduleId !== null) {
            schedules[selectedDateStr].splice(selectedScheduleId, 1);
            saveSchedulesToStorage(schedules);
        }
        closeScheduleModal();
        renderCalendar();
    }
}
