// --- DATA & STATE ---
// Compute the Monday of the current week at UTC noon.
function currentWeekMonday() {
    const now = new Date();
    const utc = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), 12));
    const day = utc.getUTCDay(); // 0=Sun
    utc.setUTCDate(utc.getUTCDate() - (day === 0 ? 6 : day - 1));
    return utc;
}

let weekStartDate = currentWeekMonday();
let monthlyViewDate = (() => {
    const m = currentWeekMonday();
    return new Date(Date.UTC(m.getUTCFullYear(), m.getUTCMonth(), 1, 12));
})();
let visibleMonthCount = 3;
let currentView = 'weekly';

const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const daysOfWeekShort = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// Default to empty — no seed data on first run.
// Use loadSeedData() (wired to the empty-state prompt) to populate demo data.
let employees = {};
let allSchedules = {};

let shiftInfo = { 
    's1': { title: 'Morning', subtitle: '(8am - 4pm)', color: 'bg-sky-400', order: 1, hours: 8 }, 
    's2': { title: 'Evening', subtitle: '(4pm - 12am)', color: 'bg-amber-400', order: 2, hours: 8 }, 
    's3': { title: 'Night', subtitle: '(12am - 8am)', color: 'bg-indigo-500', order: 3, hours: 8 } 
};


// --- PERSISTENCE ---
const STORAGE_KEY = 'schedule_maker_data';

function saveState() {
    const state = {
        employees,
        allSchedules,
        shiftInfo,
        weekStartDate: weekStartDate.toISOString(),
        monthlyViewDate: monthlyViewDate.toISOString(),
        visibleMonthCount,
        currentView,
    };
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (e) {
        alert('Save failed: ' + e.message);
    }
}

function loadState() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return false;
    try {
        const state = JSON.parse(saved);
        const isObj = v => v !== null && typeof v === 'object' && !Array.isArray(v);
        if (!isObj(state)) return false;
        if (isObj(state.employees)) employees = state.employees;
        if (isObj(state.allSchedules)) allSchedules = state.allSchedules;
        if (isObj(state.shiftInfo)) shiftInfo = state.shiftInfo;
        if (state.weekStartDate) weekStartDate = new Date(state.weekStartDate);
        if (state.monthlyViewDate) monthlyViewDate = new Date(state.monthlyViewDate);
        if (typeof state.visibleMonthCount === 'number') visibleMonthCount = state.visibleMonthCount;
        if (state.currentView) currentView = state.currentView;
        return true;
    } catch (e) {
        console.warn('Failed to load saved schedule:', e);
        return false;
    }
}

function exportState() {
    const state = {
        employees,
        allSchedules,
        shiftInfo,
        weekStartDate: weekStartDate.toISOString(),
        monthlyViewDate: monthlyViewDate.toISOString(),
        visibleMonthCount,
        currentView,
    };
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `schedule_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 100);
}

function importState(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const state = JSON.parse(e.target.result);
            const isObj = v => v !== null && typeof v === 'object' && !Array.isArray(v);
            if (!isObj(state) || !isObj(state.employees) || !isObj(state.allSchedules)) {
                alert('Import failed: file does not match expected schedule backup format.\nRequired keys: employees, allSchedules (each must be an object).');
                return;
            }
            employees = state.employees;
            allSchedules = state.allSchedules;
            if (isObj(state.shiftInfo)) shiftInfo = state.shiftInfo;
            if (state.weekStartDate) weekStartDate = new Date(state.weekStartDate);
            if (state.monthlyViewDate) monthlyViewDate = new Date(state.monthlyViewDate);
            if (typeof state.visibleMonthCount === 'number') visibleMonthCount = state.visibleMonthCount;
            switchView(state.currentView || currentView);
            renderAvailableEmployees();
        } catch (err) {
            alert('Import failed: ' + err.message);
        }
    };
    reader.readAsText(file);
}

// Populate demo employees and schedules relative to the current week.
// Intended for first-run preview only — not production data.
function loadSeedData() {
    const monday = currentWeekMonday();
    const d = (offset) => {
        const dt = new Date(monday);
        dt.setUTCDate(dt.getUTCDate() + offset);
        return dt.toISOString().split('T')[0];
    };
    employees = {
        1:  { name: 'Liam P.',     color: 'bg-blue-100 text-blue-800',   phone: '555-0101', email: 'liam.p@example.com',     notes: 'Prefers morning shifts.', rules: { 'Monday-s1': true, 'Monday-s2': true, 'Monday-s3': true } },
        2:  { name: 'Olivia C.',   color: 'bg-green-100 text-green-800',  phone: '555-0102', email: 'olivia.c@example.com',   notes: '', rules: {} },
        3:  { name: 'Noah B.',     color: 'bg-yellow-100 text-yellow-800',phone: '555-0103', email: 'noah.b@example.com',     notes: '', rules: { 'Friday-s3': true, 'Saturday-s3': true } },
        4:  { name: 'Emma G.',     color: 'bg-purple-100 text-purple-800',phone: '555-0104', email: 'emma.g@example.com',     notes: 'Unavailable on Wednesdays.', rules: { 'Wednesday-s1': true, 'Wednesday-s2': true, 'Wednesday-s3': true } },
        5:  { name: 'James W.',    color: 'bg-pink-100 text-pink-800',    phone: '555-0105', email: 'james.w@example.com',    notes: '', rules: {} },
        6:  { name: 'Ava M.',      color: 'bg-indigo-100 text-indigo-800',phone: '555-0106', email: 'ava.m@example.com',      notes: '', rules: {} },
        7:  { name: 'William R.',  color: 'bg-red-100 text-red-800',      phone: '555-0107', email: 'william.r@example.com',  notes: '', rules: {} },
        8:  { name: 'Sophia L.',   color: 'bg-teal-100 text-teal-800',    phone: '555-0108', email: 'sophia.l@example.com',   notes: 'Can cover extra shifts.', rules: {} },
        9:  { name: 'Mason H.',    color: 'bg-orange-100 text-orange-800',phone: '555-0109', email: 'mason.h@example.com',    notes: '', rules: {} },
        10: { name: 'Isabella K.', color: 'bg-cyan-100 text-cyan-800',    phone: '555-0110', email: 'isabella.k@example.com', notes: '', rules: {} },
    };
    allSchedules = {
        [d(0)]:  { 's1': [1, 4],      's2': [7, 8],    's3': [5]    },
        [d(1)]:  { 's1': [2, 5],      's2': [6, 9],    's3': [1]    },
        [d(2)]:  { 's1': [3, 6],      's2': [5, 10],   's3': [2]    },
        [d(3)]:  { 's1': [1, 7],      's2': [4, 8],    's3': [9]    },
        [d(4)]:  { 's1': [2, 8],      's2': [3, 7],    's3': [10]   },
        [d(5)]:  { 's1': [9, 10],     's2': [1, 2, 3]              },
        [d(6)]:  {                     's2': [9, 10],   's3': [4, 5] },
        [d(7)]:  { 's1': [2, 4],      's2': [6, 8],    's3': [1]    },
        [d(14)]: { 's1': [1, 3],      's2': [5, 7],    's3': [9]    },
        [d(25)]: { 's1': [10, 8],     's2': [2, 4]                  },
    };
    weekStartDate = new Date(monday);
    monthlyViewDate = new Date(Date.UTC(monday.getUTCFullYear(), monday.getUTCMonth(), 1, 12));
    saveState();
    switchView(currentView);
    renderAvailableEmployees();
    updateDateDisplay();
}

// --- DOM Elements ---
const weeklyViewContainer = document.getElementById('weekly-view');
const monthlyViewContainer = document.getElementById('monthly-view');
const weeklyViewBtn = document.getElementById('weekly-view-btn');
const monthlyViewBtn = document.getElementById('monthly-view-btn');
const modalOverlay = document.getElementById('modal-overlay');

// --- FUNCTIONS ---
const formatDate = (date, options) => date.toLocaleDateString('en-US', { timeZone: 'UTC', ...options });

function updateDateDisplay() {
    const endDate = new Date(weekStartDate);
    endDate.setUTCDate(endDate.getUTCDate() + 6);
    document.getElementById('date-range-button').textContent = `${formatDate(weekStartDate, {month: 'long', day: 'numeric', year: 'numeric'})} - ${formatDate(endDate, {month: 'long', day: 'numeric', year: 'numeric'})}`;
}

function updateMonthlyDateDisplay() {
    const endDate = new Date(monthlyViewDate);
    endDate.setUTCMonth(endDate.getUTCMonth() + visibleMonthCount - 1);
    document.getElementById('date-range-button').textContent = `${formatDate(monthlyViewDate, {month: 'long', year: 'numeric'})} - ${formatDate(endDate, {month: 'long', year: 'numeric'})}`;
}

function renderSchedule() {
    const scheduleBody = document.getElementById('schedule-body');
    const scheduleHeader = document.getElementById('schedule-header-row');
    const monthTitle = document.getElementById('weekly-view-month-title');
    scheduleBody.innerHTML = '';
    scheduleHeader.innerHTML = '';

    const endDate = new Date(weekStartDate);
    endDate.setUTCDate(endDate.getUTCDate() + 6);
    const startMonthStr = formatDate(weekStartDate, { month: 'long', year: 'numeric' });
    const endMonthStr = formatDate(endDate, { month: 'long', year: 'numeric' });
    monthTitle.textContent = startMonthStr === endMonthStr ? startMonthStr : `${formatDate(weekStartDate, { month: 'long' })} - ${formatDate(endDate, { month: 'long', year: 'numeric' })}`;

    scheduleHeader.innerHTML += `<th scope="col" class="px-6 py-3 rounded-tl-lg">Shift</th>`;
    for(let i=0; i<7; i++) {
        const dayDate = new Date(weekStartDate);
        dayDate.setUTCDate(dayDate.getUTCDate() + i);
        scheduleHeader.innerHTML += `<th scope="col" class="px-6 py-3">${daysOfWeekShort[dayDate.getUTCDay()]} ${dayDate.getUTCDate()}</th>`;
    }

    const sortedShifts = Object.entries(shiftInfo).sort(([, a], [, b]) => a.order - b.order);

    sortedShifts.forEach(([shiftId, shift]) => {
        const row = document.createElement('tr');
        row.className = 'bg-white border-b';
        
        const shiftCell = document.createElement('th');
        shiftCell.scope = 'row';
        shiftCell.className = 'px-6 py-4 font-medium text-slate-900 whitespace-nowrap';
        shiftCell.innerHTML = `<button data-shift-id="${shiftId}" class="text-left hover:text-sky-600">
                                    <span class="block font-bold">${shift.title}</span>
                                    <span class="text-xs font-normal">${shift.subtitle}</span>
                                </button>`;
        row.appendChild(shiftCell);
        
        for(let i=0; i<7; i++) {
            const dayDate = new Date(weekStartDate);
            dayDate.setUTCDate(dayDate.getUTCDate() + i);
            const dateKey = dayDate.toISOString().split('T')[0];

            const dayCell = document.createElement('td');
            dayCell.className = 'p-2 editable-cell transition-all align-top';
            dayCell.dataset.dateKey = dateKey;
            dayCell.dataset.shiftId = shiftId;
            
            const daySchedule = allSchedules[dateKey];
            const employeeIds = daySchedule && daySchedule[shiftId] ? daySchedule[shiftId] : [];

            const cellContent = document.createElement('div');
            cellContent.className = 'flex flex-col space-y-2 min-h-[4rem]';
            if (employeeIds.length > 0) {
                employeeIds.forEach(id => {
                   cellContent.appendChild(createEmployeePill(id, dateKey, shiftId));
                });
            }
            dayCell.appendChild(cellContent);
            row.appendChild(dayCell);
        }
        scheduleBody.appendChild(row);
    });
    addDragAndDropListeners();
    addShiftEditListeners();
}

function renderAvailableEmployees() {
    const container = document.getElementById('available-employees-container');
    container.innerHTML = '';
    const ids = Object.keys(employees);
    if (ids.length === 0) {
        const msg = document.createElement('span');
        msg.className = 'text-slate-400 text-sm';
        msg.textContent = 'No employees yet — add one below, or ';
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'text-sky-600 underline hover:text-sky-800 text-sm';
        btn.textContent = 'load sample data';
        btn.addEventListener('click', loadSeedData);
        container.appendChild(msg);
        container.appendChild(btn);
        return;
    }
    ids.forEach(id => {
        container.appendChild(createEmployeePill(id));
    });
    addDragAndDropListeners();
}

function createEmployeePill(employeeId, fromDateKey = null, fromShiftId = null) {
    const employee = employees[employeeId];
    const pill = document.createElement('div');
    pill.className = `relative draggable-employee px-2 py-1 text-xs font-semibold rounded-full text-center ${employee.color} cursor-pointer`;
    pill.textContent = employee.name;
    pill.draggable = true;
    pill.dataset.employeeId = employeeId;
    if(fromDateKey) pill.dataset.fromDateKey = fromDateKey;
    if(fromShiftId) pill.dataset.fromShiftId = fromShiftId;
    
    pill.addEventListener('click', (e) => {
        e.stopPropagation();
        console.log('Employee pill clicked:', employeeId);
        try {
            showEmployeeModal(employeeId);
        } catch (error) {
            console.error('Error showing employee modal:', error);
        }
    });
    pill.addEventListener('mouseover', (e) => showEmployeePopover(e, employeeId));
    pill.addEventListener('mouseout', hideEmployeePopover);

    // Check for rule violations
    if (fromDateKey && fromShiftId) {
        const dayIndex = new Date(fromDateKey + 'T12:00:00Z').getUTCDay();
        const dayName = daysOfWeek[dayIndex];
        const ruleKey = `${dayName}-${fromShiftId}`;
        if (employee.rules[ruleKey]) {
            const alertIcon = document.createElement('div');
            alertIcon.className = 'absolute -top-1 -right-1';
            alertIcon.innerHTML = `<svg class="w-4 h-4 text-red-500 bg-white rounded-full" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>`;
            pill.appendChild(alertIcon);
        }
    }

    return pill;
}

function renderMonthlyCalendars() {
    const container = document.getElementById('monthly-calendars-container');
    container.innerHTML = '';
    
    const gridClasses = { 3: 'md:grid-cols-3', 6: 'md:grid-cols-2 lg:grid-cols-3', 9: 'md:grid-cols-2 lg:grid-cols-3', 12: 'md:grid-cols-2 lg:grid-cols-4' };
    container.className = `grid grid-cols-1 gap-8 ${gridClasses[visibleMonthCount]}`;

    const endDate = new Date(monthlyViewDate);
    endDate.setUTCMonth(endDate.getUTCMonth() + visibleMonthCount - 1);
    document.getElementById('monthly-view-title').textContent = `${formatDate(monthlyViewDate, {month: 'long', year: 'numeric'})} - ${formatDate(endDate, {month: 'long', year: 'numeric'})}`;

    for (let i = 0; i < visibleMonthCount; i++) {
        const date = new Date(monthlyViewDate);
        date.setUTCMonth(date.getUTCMonth() + i);
        container.appendChild(createMonthElement(date));
    }
    
    document.querySelectorAll('.calendar-day-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const selectedDateStr = e.currentTarget.dataset.date;
            if (!selectedDateStr) return;
            
            weekStartDate = new Date(selectedDateStr);
            switchView('weekly');
        });
    });
}

function createMonthElement(date) {
    const calWrapper = document.createElement('div');
    calWrapper.className = 'bg-white p-4 rounded-lg shadow-sm';
    const month = date.getUTCMonth();
    const year = date.getUTCFullYear();
    const firstDay = new Date(Date.UTC(year, month, 1));
    const daysInMonth = new Date(Date.UTC(year, month + 1, 0)).getUTCDate();
    const startingDay = firstDay.getUTCDay();
    
    let html = `<h3 class="text-lg font-semibold text-center mb-4">${formatDate(date, {month: 'long', year: 'numeric'})}</h3>`;
    html += `<div class="grid grid-cols-7 gap-1 text-center text-xs font-bold text-slate-500">${daysOfWeekShort.map(d => `<div>${d}</div>`).join('')}</div>`;
    html += `<div class="grid grid-cols-7 gap-1 mt-2">`;
    for (let i = 0; i < startingDay; i++) html += `<div></div>`;

    for (let i = 1; i <= daysInMonth; i++) {
        const dayDate = new Date(Date.UTC(year, month, i, 12));
        const dateStr = dayDate.toISOString();
        const dateKey = dateStr.split('T')[0];
        const scheduledShifts = allSchedules[dateKey];
        let shiftDots = '';
        if (scheduledShifts && Object.keys(scheduledShifts).length > 0) {
            shiftDots += `<div class="absolute bottom-1.5 left-1/2 -translate-x-1/2 flex space-x-0.5">`;
            const shiftIds = Object.keys(scheduledShifts).sort((a, b) => shiftInfo[a].order - shiftInfo[b].order);
            shiftIds.forEach(shiftId => {
                if (shiftInfo[shiftId] && scheduledShifts[shiftId].length > 0) {
                    shiftDots += `<div class="w-1.5 h-1.5 ${shiftInfo[shiftId].color} rounded-full"></div>`;
                }
            });
            shiftDots += `</div>`;
        }
        html += `<div><button data-date="${dateStr}" class="relative calendar-day-btn w-full h-10 flex items-center justify-center rounded-lg transition-all">${i}${shiftDots}</button></div>`;
    }
    html += `</div>`;
    calWrapper.innerHTML = html;
    return calWrapper;
}

function renderMonthlyViewLegend() {
    const container = document.getElementById('monthly-view-legend');
    let html = '<div class="flex items-center justify-center flex-wrap gap-x-4 gap-y-2 text-xs text-slate-600"><span class="font-semibold">Legend:</span>';
    const sortedShifts = Object.values(shiftInfo).sort((a,b) => a.order - b.order);
    sortedShifts.forEach(shift => {
        html += `<div class="flex items-center space-x-1.5"><div class="w-2.5 h-2.5 ${shift.color} rounded-full"></div><span>${shift.title}</span></div>`;
    });
    html += '</div>';
    container.innerHTML = html;
}

function switchView(view) {
    currentView = view;
    if (view === 'weekly') {
        weeklyViewContainer.classList.remove('hidden');
        monthlyViewContainer.classList.add('hidden');
        weeklyViewBtn.classList.add('btn-active');
        monthlyViewBtn.classList.remove('btn-active');
        renderSchedule();
        updateDateDisplay();
    } else {
        weeklyViewContainer.classList.add('hidden');
        monthlyViewContainer.classList.remove('hidden');
        monthlyViewBtn.classList.add('btn-active');
        weeklyViewBtn.classList.remove('btn-active');
        renderMonthlyCalendars();
        renderMonthlyViewLegend();
        updateMonthlyDateDisplay();
    }
}

// --- Drag and Drop Logic ---
function addDragAndDropListeners() {
    document.querySelectorAll('.draggable-employee').forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
    });

    document.querySelectorAll('.editable-cell').forEach(cell => {
        cell.addEventListener('dragover', handleDragOver);
        cell.addEventListener('dragleave', handleDragLeave);
        cell.addEventListener('drop', handleDrop);
    });
    
    const trash = document.getElementById('trash-container');
    trash.addEventListener('dragover', handleDragOver);
    trash.addEventListener('dragleave', handleDragLeave);
    trash.addEventListener('drop', handleTrashDrop);
}

function handleDragStart(e) {
    e.dataTransfer.setData('application/json', JSON.stringify({
        employeeId: e.target.dataset.employeeId,
        fromDateKey: e.target.dataset.fromDateKey,
        fromShiftId: e.target.dataset.fromShiftId,
    }));
}

function handleDragOver(e) { e.preventDefault(); e.currentTarget.classList.add('drop-target-active'); if (e.currentTarget.id === 'trash-container') document.getElementById('trash-icon').classList.add('trash-active'); }
function handleDragLeave(e) { e.currentTarget.classList.remove('drop-target-active'); if (e.currentTarget.id === 'trash-container') document.getElementById('trash-icon').classList.remove('trash-active'); }

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drop-target-active');
    const data = JSON.parse(e.dataTransfer.getData('application/json'));
    const employeeId = parseInt(data.employeeId);
    const toDateKey = e.currentTarget.dataset.dateKey;
    const toShiftId = e.currentTarget.dataset.shiftId;

    if (data.fromDateKey && data.fromShiftId) {
        const fromShiftArray = allSchedules[data.fromDateKey][data.fromShiftId];
        const index = fromShiftArray.indexOf(employeeId);
        if (index > -1) fromShiftArray.splice(index, 1);
    }
    
    if (!allSchedules[toDateKey]) allSchedules[toDateKey] = {};
    if (!allSchedules[toDateKey][toShiftId]) allSchedules[toDateKey][toShiftId] = [];
    if (!allSchedules[toDateKey][toShiftId].includes(employeeId)) allSchedules[toDateKey][toShiftId].push(employeeId);
    
    renderSchedule();
}

function handleTrashDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('drop-target-active');
    document.getElementById('trash-icon').classList.remove('trash-active');
    const data = JSON.parse(e.dataTransfer.getData('application/json'));

    if (data.fromDateKey && data.fromShiftId) {
        const employeeId = parseInt(data.employeeId);
        const fromShiftArray = allSchedules[data.fromDateKey][data.fromShiftId];
        const index = fromShiftArray.indexOf(employeeId);
        if (index > -1) fromShiftArray.splice(index, 1);
        renderSchedule();
    }
}

function setupControls() {
    weeklyViewBtn.addEventListener('click', () => switchView('weekly'));
    monthlyViewBtn.addEventListener('click', () => switchView('monthly'));
    document.getElementById('prev-day-btn').addEventListener('click', () => { weekStartDate.setUTCDate(weekStartDate.getUTCDate() - 1); renderSchedule(); updateDateDisplay(); });
    document.getElementById('next-day-btn').addEventListener('click', () => { weekStartDate.setUTCDate(weekStartDate.getUTCDate() + 1); renderSchedule(); updateDateDisplay(); });
    document.getElementById('prev-month-btn').addEventListener('click', () => { monthlyViewDate.setUTCMonth(monthlyViewDate.getUTCMonth() - 1); renderMonthlyCalendars(); updateMonthlyDateDisplay(); });
    document.getElementById('next-month-btn').addEventListener('click', () => { monthlyViewDate.setUTCMonth(monthlyViewDate.getUTCMonth() + 1); renderMonthlyCalendars(); updateMonthlyDateDisplay(); });
    const qtyButtons = document.querySelectorAll('.month-qty-btn');
    qtyButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            visibleMonthCount = parseInt(e.currentTarget.dataset.qty);
            qtyButtons.forEach(btn => btn.classList.remove('btn-active'));
            e.currentTarget.classList.add('btn-active');
            renderMonthlyCalendars();
            updateMonthlyDateDisplay();
        });
    });
    document.querySelector(`.month-qty-btn[data-qty="${visibleMonthCount}"]`).classList.add('btn-active');

    // E3a/E3b: header action buttons — save, export, import, new
    document.getElementById('save-schedule-btn').addEventListener('click', () => {
        saveState();
        const btn = document.getElementById('save-schedule-btn');
        const icon = btn.querySelector('i');
        icon.classList.replace('bi-save', 'bi-check-lg');
        setTimeout(() => icon.classList.replace('bi-check-lg', 'bi-save'), 1000);
    });
    document.getElementById('export-schedule-btn').addEventListener('click', exportState);
    document.getElementById('import-schedule-btn').addEventListener('click', () => {
        document.getElementById('import-schedule-file').click();
    });
    document.getElementById('import-schedule-file').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            importState(file);
            e.target.value = ''; // allow re-importing the same file
        }
    });
    document.getElementById('new-schedule-btn').addEventListener('click', () => {
        if (!confirm('Create a new schedule? This will clear all saved data.')) return;
        localStorage.removeItem(STORAGE_KEY);
        location.reload();
    });
}

function openModal(modalElement) {
    const allModals = modalOverlay.querySelectorAll('.bg-white');
    allModals.forEach(m => m.classList.add('hidden'));
    
    modalOverlay.classList.remove('hidden');
    modalOverlay.classList.add('flex');
    modalElement.classList.remove('hidden');
}

function closeModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    modalOverlay.classList.add('hidden');
    modalOverlay.classList.remove('flex');
}

function showEmployeeModal(employeeId) {
    console.log('showEmployeeModal called with ID:', employeeId);
    const employeeModal = document.getElementById('employee-modal');
    const employee = employees[employeeId];
    console.log('Employee modal element:', employeeModal);
    console.log('Employee data:', employee);
    if (!employee) return;
    
    employeeModal.dataset.employeeId = employeeId;

    let totalHours = 0;
    for(let i=0; i<7; i++) {
        const dayDate = new Date(weekStartDate);
        dayDate.setUTCDate(dayDate.getUTCDate() + i);
        const dateKey = dayDate.toISOString().split('T')[0];
        if (allSchedules[dateKey]) {
            Object.entries(allSchedules[dateKey]).forEach(([shiftId, employeeList]) => {
                if (employeeList.includes(parseInt(employeeId))) {
                    totalHours += shiftInfo[shiftId].hours;
                }
            });
        }
    }

    document.getElementById('employee-modal-name').textContent = employee.name;
    document.getElementById('employee-modal-hours').textContent = totalHours;
    
    document.getElementById('employee-modal-phone-view').textContent = employee.phone;
    document.getElementById('employee-modal-email-view').textContent = employee.email;
    document.getElementById('employee-modal-notes-view').textContent = employee.notes || 'No notes added.';
    document.getElementById('employee-modal-phone-edit').value = employee.phone;
    document.getElementById('employee-modal-email-edit').value = employee.email;
    document.getElementById('employee-modal-notes-edit').value = employee.notes;

    const rulesView = document.getElementById('employee-modal-rules-view');
    const unavailableDays = Object.keys(employee.rules).filter(key => employee.rules[key]).map(key => key.replace(/-(s\d)/, ' $1'));
    rulesView.textContent = unavailableDays.length > 0 ? unavailableDays.join(', ') : 'N/A';

    const rulesContainer = document.getElementById('employee-rules-container').querySelector('div');
    rulesContainer.innerHTML = '';
    daysOfWeek.forEach(day => {
        const shiftHtml = Object.keys(shiftInfo).map(shiftId => {
            const shift = shiftInfo[shiftId];
            const ruleKey = `${day}-${shiftId}`;
            const isChecked = employee.rules[ruleKey] ? 'checked' : '';
            return `<label class="flex items-center space-x-2">
                        <input type="checkbox" data-rule-key="${ruleKey}" class="rounded border-slate-300 text-sky-600 shadow-sm focus:border-sky-300 focus:ring focus:ring-offset-0 focus:ring-sky-200 focus:ring-opacity-50" ${isChecked}>
                        <span>${shift.title}</span>
                    </label>`;
        }).join('');
        rulesContainer.innerHTML += `<div class="space-y-1">
                                        <p class="font-medium">${day}</p>
                                        <div class="pl-4 space-y-1">${shiftHtml}</div>
                                     </div>`;
    });

    setEmployeeModalEditState(false);
    openModal(employeeModal);
}

function showShiftModal(shiftId) {
    console.log('showShiftModal called with ID:', shiftId);
    const shiftModal = document.getElementById('shift-modal');
    const shift = shiftInfo[shiftId];
    console.log('Shift modal element:', shiftModal);
    console.log('Shift data:', shift);
    if (!shift) return;

    document.getElementById('edit-shift-id').value = shiftId;
    document.getElementById('edit-shift-title').value = shift.title;
    document.getElementById('edit-shift-subtitle').value = shift.subtitle;

    openModal(shiftModal);
}

function setupModalsAndFlyouts() {
    document.getElementById('date-range-button').addEventListener('click', () => {
        const [y, m, d] = [weekStartDate.getUTCFullYear(), String(weekStartDate.getUTCMonth() + 1).padStart(2, '0'), String(weekStartDate.getUTCDate()).padStart(2, '0')];
        document.getElementById('week-start-date').value = `${y}-${m}-${d}`;
        openModal(document.getElementById('date-modal'));
    });
    document.getElementById('cancel-date-button').addEventListener('click', closeModal);
    document.getElementById('save-date-button').addEventListener('click', () => {
        const [year, month, day] = document.getElementById('week-start-date').value.split('-').map(Number);
        weekStartDate = new Date(Date.UTC(year, month - 1, day, 12));
        updateDateDisplay(); renderSchedule(); closeModal();
    });

    document.getElementById('employee-modal-close').addEventListener('click', closeModal);
    document.getElementById('employee-edit-toggle').addEventListener('click', () => toggleEmployeeModalEdit());
    document.getElementById('employee-modal-save').addEventListener('click', () => {
        const employeeId = document.getElementById('employee-modal').dataset.employeeId;
        saveEmployeeDetails(employeeId);
        closeModal();
    });
    document.getElementById('employee-modal-remove').addEventListener('click', () => {
        const employeeId = document.getElementById('employee-modal').dataset.employeeId;
        if (confirm(`Are you sure you want to remove ${employees[employeeId].name}? This action cannot be undone.`)) {
            removeEmployee(employeeId);
            closeModal();
        }
    });

    document.getElementById('add-employee-btn').addEventListener('click', () => openModal(document.getElementById('add-employee-modal')));
    document.getElementById('add-employee-cancel').addEventListener('click', closeModal);
    document.getElementById('add-employee-form').addEventListener('submit', (e) => {
        e.preventDefault();
        addEmployee();
        closeModal();
        e.target.reset();
    });
    
    document.getElementById('shift-modal-cancel').addEventListener('click', closeModal);
    document.getElementById('edit-shift-form').addEventListener('submit', (e) => {
        e.preventDefault();
        saveShiftDetails();
        closeModal();
    });

    // Modal overlay click to close
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    const navFlyout = document.getElementById('nav-flyout');
    const overlay = document.getElementById('overlay');
    const openNav = () => { navFlyout.classList.remove('-translate-x-full'); overlay.classList.remove('hidden'); };
    const closeNav = () => { navFlyout.classList.add('-translate-x-full'); overlay.classList.add('hidden'); };
    const navToggle = document.getElementById('nav-toggle');
    if (navToggle) navToggle.addEventListener('click', openNav);
    document.getElementById('nav-close').addEventListener('click', closeNav);
    overlay.addEventListener('click', closeNav);
}

function setEmployeeModalEditState(isEditing) {
    const toggleButton = document.getElementById('employee-edit-toggle');
    
    document.getElementById('employee-modal-view-content').classList.toggle('hidden', isEditing);
    document.getElementById('employee-modal-edit-content').classList.toggle('hidden', !isEditing);
    document.getElementById('employee-modal-save').classList.toggle('hidden', !isEditing);
    
    // Update button text based on state
    toggleButton.textContent = isEditing ? 'Cancel' : 'Edit';
}

function toggleEmployeeModalEdit() {
    const isEditing = document.getElementById('employee-modal-edit-content').classList.contains('hidden');
    setEmployeeModalEditState(isEditing);
}

function saveEmployeeDetails(employeeId) {
    if (!employees[employeeId]) return;
    
    employees[employeeId].phone = document.getElementById('employee-modal-phone-edit').value;
    employees[employeeId].email = document.getElementById('employee-modal-email-edit').value;
    employees[employeeId].notes = document.getElementById('employee-modal-notes-edit').value;
    
    employees[employeeId].rules = {};
    document.querySelectorAll('#employee-rules-container input[type="checkbox"]').forEach(checkbox => {
        if (checkbox.checked) {
            employees[employeeId].rules[checkbox.dataset.ruleKey] = true;
        }
    });

    renderSchedule();
}

function saveShiftDetails() {
    const shiftId = document.getElementById('edit-shift-id').value;
    if (!shiftInfo[shiftId]) return;

    shiftInfo[shiftId].title = document.getElementById('edit-shift-title').value;
    shiftInfo[shiftId].subtitle = document.getElementById('edit-shift-subtitle').value;

    renderSchedule();
    if(currentView === 'monthly') {
        renderMonthlyViewLegend();
    }
}

function addEmployee() {
    const name = document.getElementById('new-employee-name').value;
    if (!name) {
        alert('Employee name is required.');
        return;
    }
    const newId = Math.max(0, ...Object.keys(employees).map(Number)) + 1;
    const colors = ['blue', 'green', 'yellow', 'purple', 'pink', 'indigo', 'red', 'teal', 'orange', 'cyan'];
    const randomColor = colors[newId % colors.length];

    employees[newId] = {
        name: name,
        color: `bg-${randomColor}-100 text-${randomColor}-800`,
        phone: document.getElementById('new-employee-phone').value,
        email: document.getElementById('new-employee-email').value,
        notes: '',
        rules: {}
    };
    renderAvailableEmployees();
}

function removeEmployee(employeeId) {
    const numericId = parseInt(employeeId);
    for (const dateKey in allSchedules) {
        for (const shiftId in allSchedules[dateKey]) {
            allSchedules[dateKey][shiftId] = allSchedules[dateKey][shiftId].filter(id => id !== numericId);
        }
    }
    delete employees[employeeId];
    renderSchedule();
    renderAvailableEmployees();
}

function showEmployeePopover(event, employeeId) {
    const popover = document.getElementById('employee-popover');
    const employee = employees[employeeId];
    if (!employee) return;

    const unavailableDays = Object.keys(employee.rules).filter(key => employee.rules[key]).map(key => key.replace(/-(s\d)/, ` (${shiftInfo[key.split('-')[1]].title})`));
    const rulesText = unavailableDays.length > 0 ? unavailableDays.join(', ') : 'N/A';

    popover.innerHTML = '';

    function makeP(cls) {
        const p = document.createElement('p');
        if (cls) p.className = cls;
        return p;
    }
    function makeDivider() {
        const d = document.createElement('div');
        d.className = 'border-t my-2';
        return d;
    }

    const nameEl = makeP('font-bold text-base');
    nameEl.textContent = employee.name;
    popover.appendChild(nameEl);
    popover.appendChild(makeDivider());

    const phoneEl = makeP();
    const phoneLbl = document.createElement('span');
    phoneLbl.className = 'font-semibold text-slate-500';
    phoneLbl.textContent = 'Phone: ';
    phoneEl.appendChild(phoneLbl);
    phoneEl.appendChild(document.createTextNode(employee.phone));
    popover.appendChild(phoneEl);

    const emailEl = makeP();
    const emailLbl = document.createElement('span');
    emailLbl.className = 'font-semibold text-slate-500';
    emailLbl.textContent = 'Email: ';
    emailEl.appendChild(emailLbl);
    emailEl.appendChild(document.createTextNode(employee.email));
    popover.appendChild(emailEl);

    popover.appendChild(makeDivider());

    const notesLbl = makeP('font-semibold text-slate-500');
    notesLbl.textContent = 'Notes:';
    popover.appendChild(notesLbl);
    const notesVal = makeP('text-xs bg-slate-50 p-1 rounded');
    notesVal.textContent = employee.notes || 'N/A';
    popover.appendChild(notesVal);

    popover.appendChild(makeDivider());

    const unavailLbl = makeP('font-semibold text-slate-500');
    unavailLbl.textContent = 'Unavailable:';
    popover.appendChild(unavailLbl);
    const unavailVal = makeP('text-xs');
    unavailVal.textContent = rulesText;
    popover.appendChild(unavailVal);

    const rect = event.currentTarget.getBoundingClientRect();
    popover.style.left = `${rect.left + rect.width / 2}px`;
    popover.style.top = `${rect.bottom + window.scrollY + 5}px`;
    popover.style.transform = 'translateX(-50%)';
    popover.classList.remove('hidden');
}

function hideEmployeePopover() {
    document.getElementById('employee-popover').classList.add('hidden');
}

function addShiftEditListeners() {
    document.querySelectorAll('button[data-shift-id]').forEach(el => {
        el.addEventListener('click', (e) => {
            const shiftId = e.currentTarget.dataset.shiftId;
            showShiftModal(shiftId);
        });
    });
}

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadState(); // restore from localStorage if available
    setupControls();
    setupModalsAndFlyouts();
    switchView(currentView);
    renderAvailableEmployees();
    weeklyViewBtn.classList.add('btn-active');
});
