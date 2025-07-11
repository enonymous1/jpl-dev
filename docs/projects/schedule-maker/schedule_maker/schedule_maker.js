/**
 * Schedule Maker JavaScript
 * 
 * Interactive schedule creation and management tool.
 * 
 * Author: JPL Development
 * Date: July 2025
 */

class ScheduleMaker {
    constructor() {
        this.currentDate = new Date();
        this.currentView = 'week';
        this.events = [];
        this.selectedDate = null;
        this.selectedTime = null;
        this.editingEvent = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.generateTimeSlots();
        this.renderSchedule();
        this.updateDateDisplay();
    }
    
    setupEventListeners() {
        // View controls
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                this.currentView = e.target.dataset.view;
                this.renderSchedule();
            });
        });
        
        // Date navigation
        document.getElementById('prev-date').addEventListener('click', () => {
            this.navigateDate(-1);
        });
        
        document.getElementById('next-date').addEventListener('click', () => {
            this.navigateDate(1);
        });
        
        document.getElementById('today-btn').addEventListener('click', () => {
            this.currentDate = new Date();
            this.renderSchedule();
            this.updateDateDisplay();
        });
        
        // Header actions
        document.getElementById('new-schedule-btn').addEventListener('click', () => {
            this.newSchedule();
        });
        
        document.getElementById('save-schedule-btn').addEventListener('click', () => {
            this.saveSchedule();
        });
        
        document.getElementById('export-schedule-btn').addEventListener('click', () => {
            this.exportSchedule();
        });
        
        // Event panel
        document.getElementById('close-event-panel').addEventListener('click', () => {
            this.hideEventPanel();
        });
        
        document.getElementById('cancel-event').addEventListener('click', () => {
            this.hideEventPanel();
        });
        
        document.getElementById('modal-overlay').addEventListener('click', () => {
            this.hideEventPanel();
        });
        
        document.getElementById('event-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveEvent();
        });
        
        // Color presets
        document.querySelectorAll('.color-preset').forEach(preset => {
            preset.addEventListener('click', (e) => {
                const color = e.target.dataset.color;
                document.getElementById('event-color').value = color;
                document.querySelectorAll('.color-preset').forEach(p => p.classList.remove('active'));
                e.target.classList.add('active');
            });
        });
    }
    
    generateTimeSlots() {
        const timeSlotsContainer = document.getElementById('time-slots');
        timeSlotsContainer.innerHTML = '';
        
        for (let hour = 6; hour <= 22; hour++) {
            const timeSlot = document.createElement('div');
            timeSlot.className = 'time-slot';
            timeSlot.textContent = this.formatTime(hour, 0);
            timeSlotsContainer.appendChild(timeSlot);
        }
    }
    
    renderSchedule() {
        const header = document.getElementById('schedule-header');
        const body = document.getElementById('schedule-body');
        
        header.innerHTML = '';
        body.innerHTML = '';
        
        if (this.currentView === 'week') {
            this.renderWeekView(header, body);
        } else if (this.currentView === 'day') {
            this.renderDayView(header, body);
        } else if (this.currentView === 'month') {
            this.renderMonthView(header, body);
        }
    }
    
    renderWeekView(header, body) {
        const startOfWeek = this.getStartOfWeek(this.currentDate);
        
        // Render headers
        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(date.getDate() + i);
            
            const dayHeader = document.createElement('div');
            dayHeader.className = 'day-header';
            if (this.isToday(date)) {
                dayHeader.classList.add('today');
            }
            
            const dayName = document.createElement('div');
            dayName.className = 'day-name';
            dayName.textContent = date.toLocaleDateString('en-US', { weekday: 'short' });
            
            const dayNumber = document.createElement('div');
            dayNumber.className = 'day-number';
            dayNumber.textContent = date.getDate();
            
            dayHeader.appendChild(dayName);
            dayHeader.appendChild(dayNumber);
            header.appendChild(dayHeader);
        }
        
        // Render body
        for (let i = 0; i < 7; i++) {
            const date = new Date(startOfWeek);
            date.setDate(date.getDate() + i);
            
            const dayColumn = document.createElement('div');
            dayColumn.className = 'day-column';
            dayColumn.dataset.date = date.toISOString().split('T')[0];
            
            // Add hour lines
            for (let hour = 6; hour <= 22; hour++) {
                const hourLine = document.createElement('div');
                hourLine.className = 'hour-line';
                hourLine.style.top = `${(hour - 6) * 60}px`;
                dayColumn.appendChild(hourLine);
            }
            
            // Add click listener for creating events
            dayColumn.addEventListener('click', (e) => {
                this.handleDayColumnClick(e, date);
            });
            
            body.appendChild(dayColumn);
        }
        
        // Render events
        this.renderEvents();
    }
    
    renderDayView(header, body) {
        // Similar implementation for day view
        const dayHeader = document.createElement('div');
        dayHeader.className = 'day-header today';
        
        const dayName = document.createElement('div');
        dayName.className = 'day-name';
        dayName.textContent = this.currentDate.toLocaleDateString('en-US', { weekday: 'long' });
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = this.currentDate.getDate();
        
        dayHeader.appendChild(dayName);
        dayHeader.appendChild(dayNumber);
        header.appendChild(dayHeader);
        
        // Single day column
        const dayColumn = document.createElement('div');
        dayColumn.className = 'day-column';
        dayColumn.dataset.date = this.currentDate.toISOString().split('T')[0];
        
        for (let hour = 6; hour <= 22; hour++) {
            const hourLine = document.createElement('div');
            hourLine.className = 'hour-line';
            hourLine.style.top = `${(hour - 6) * 60}px`;
            dayColumn.appendChild(hourLine);
        }
        
        dayColumn.addEventListener('click', (e) => {
            this.handleDayColumnClick(e, this.currentDate);
        });
        
        body.appendChild(dayColumn);
        this.renderEvents();
    }
    
    renderMonthView(header, body) {
        // Simplified month view - could be expanded
        header.innerHTML = '<div class="month-header">Month View - Coming Soon</div>';
        body.innerHTML = '<div class="month-placeholder">Month view will be implemented here</div>';
    }
    
    renderEvents() {
        this.events.forEach(event => {
            const eventElement = this.createEventElement(event);
            const dayColumn = document.querySelector(`[data-date="${event.date}"]`);
            if (dayColumn) {
                dayColumn.appendChild(eventElement);
            }
        });
    }
    
    createEventElement(event) {
        const eventEl = document.createElement('div');
        eventEl.className = 'schedule-event';
        eventEl.style.backgroundColor = event.color || '#4F46E5';
        
        const startTime = this.parseTime(event.start_time);
        const endTime = this.parseTime(event.end_time);
        const duration = endTime - startTime;
        
        const top = (startTime - 6) * 60; // 6 AM is the starting point
        const height = duration * 60;
        
        eventEl.style.top = `${top}px`;
        eventEl.style.height = `${height}px`;
        
        const title = document.createElement('div');
        title.className = 'event-title';
        title.textContent = event.title;
        
        const time = document.createElement('div');
        time.className = 'event-time';
        time.textContent = `${event.start_time} - ${event.end_time}`;
        
        eventEl.appendChild(title);
        eventEl.appendChild(time);
        
        // Add click listener for editing
        eventEl.addEventListener('click', (e) => {
            e.stopPropagation();
            this.editEvent(event);
        });
        
        return eventEl;
    }
    
    handleDayColumnClick(e, date) {
        const rect = e.currentTarget.getBoundingClientRect();
        const y = e.clientY - rect.top;
        const hour = Math.floor(y / 60) + 6; // 6 AM is the starting point
        const minute = Math.round((y % 60) / 60 * 4) * 15; // Round to 15-minute intervals
        
        this.selectedDate = date.toISOString().split('T')[0];
        this.selectedTime = this.formatTime(hour, minute);
        
        this.showEventPanel();
    }
    
    showEventPanel(event = null) {
        const panel = document.getElementById('event-panel');
        const overlay = document.getElementById('modal-overlay');
        const form = document.getElementById('event-form');
        
        if (event) {
            // Editing existing event
            this.editingEvent = event;
            document.getElementById('event-panel-title').textContent = 'Edit Event';
            document.getElementById('event-title').value = event.title;
            document.getElementById('event-date').value = event.date;
            document.getElementById('event-start-time').value = event.start_time;
            document.getElementById('event-end-time').value = event.end_time;
            document.getElementById('event-description').value = event.description || '';
            document.getElementById('event-color').value = event.color || '#4F46E5';
        } else {
            // Creating new event
            this.editingEvent = null;
            document.getElementById('event-panel-title').textContent = 'Add Event';
            form.reset();
            if (this.selectedDate) {
                document.getElementById('event-date').value = this.selectedDate;
            }
            if (this.selectedTime) {
                document.getElementById('event-start-time').value = this.selectedTime;
                // Set end time to 1 hour later
                const startHour = parseInt(this.selectedTime.split(':')[0]);
                const endTime = this.formatTime(startHour + 1, 0);
                document.getElementById('event-end-time').value = endTime;
            }
        }
        
        panel.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    hideEventPanel() {
        const panel = document.getElementById('event-panel');
        const overlay = document.getElementById('modal-overlay');
        
        panel.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        
        this.editingEvent = null;
        this.selectedDate = null;
        this.selectedTime = null;
    }
    
    saveEvent() {
        const formData = new FormData(document.getElementById('event-form'));
        const event = {
            id: this.editingEvent ? this.editingEvent.id : Date.now().toString(),
            title: formData.get('title'),
            date: formData.get('date'),
            start_time: formData.get('start_time'),
            end_time: formData.get('end_time'),
            description: formData.get('description'),
            color: formData.get('color')
        };
        
        if (this.editingEvent) {
            // Update existing event
            const index = this.events.findIndex(e => e.id === this.editingEvent.id);
            if (index !== -1) {
                this.events[index] = event;
            }
        } else {
            // Add new event
            this.events.push(event);
        }
        
        this.hideEventPanel();
        this.renderSchedule();
        this.showNotification('Event saved successfully!');
    }
    
    editEvent(event) {
        this.showEventPanel(event);
    }
    
    newSchedule() {
        if (confirm('Create a new schedule? This will clear all current events.')) {
            this.events = [];
            document.getElementById('schedule-name').value = 'My Schedule';
            document.getElementById('schedule-description').value = '';
            this.renderSchedule();
            this.showNotification('New schedule created!');
        }
    }
    
    saveSchedule() {
        const scheduleData = {
            name: document.getElementById('schedule-name').value,
            description: document.getElementById('schedule-description').value,
            events: this.events,
            created_at: new Date().toISOString()
        };
        
        // Save to localStorage for demo purposes
        localStorage.setItem('schedule_maker_data', JSON.stringify(scheduleData));
        this.showNotification('Schedule saved to local storage!');
        
        // In a real application, you would send this to the server
        // fetch('/projects/schedule-maker/api/save-schedule', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(scheduleData)
        // });
    }
    
    exportSchedule() {
        const scheduleData = {
            name: document.getElementById('schedule-name').value,
            description: document.getElementById('schedule-description').value,
            events: this.events,
            exported_at: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(scheduleData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${scheduleData.name.replace(/\\s+/g, '_')}_schedule.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('Schedule exported successfully!');
    }
    
    // Helper methods
    navigateDate(direction) {
        if (this.currentView === 'week') {
            this.currentDate.setDate(this.currentDate.getDate() + (direction * 7));
        } else if (this.currentView === 'day') {
            this.currentDate.setDate(this.currentDate.getDate() + direction);
        } else if (this.currentView === 'month') {
            this.currentDate.setMonth(this.currentDate.getMonth() + direction);
        }
        
        this.renderSchedule();
        this.updateDateDisplay();
    }
    
    updateDateDisplay() {
        const dateEl = document.getElementById('current-date');
        if (this.currentView === 'week') {
            const startOfWeek = this.getStartOfWeek(this.currentDate);
            const endOfWeek = new Date(startOfWeek);
            endOfWeek.setDate(endOfWeek.getDate() + 6);
            dateEl.textContent = `${startOfWeek.toLocaleDateString()} - ${endOfWeek.toLocaleDateString()}`;
        } else if (this.currentView === 'day') {
            dateEl.textContent = this.currentDate.toLocaleDateString('en-US', { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } else if (this.currentView === 'month') {
            dateEl.textContent = this.currentDate.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long' 
            });
        }
    }
    
    getStartOfWeek(date) {
        const start = new Date(date);
        const day = start.getDay();
        const diff = start.getDate() - day;
        start.setDate(diff);
        start.setHours(0, 0, 0, 0);
        return start;
    }
    
    isToday(date) {
        const today = new Date();
        return date.toDateString() === today.toDateString();
    }
    
    formatTime(hour, minute) {
        return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
    }
    
    parseTime(timeString) {
        const [hour, minute] = timeString.split(':').map(Number);
        return hour + (minute / 60);
    }
    
    showNotification(message) {
        // Simple notification - could be enhanced with a proper notification system
        const notification = document.createElement('div');
        notification.className = 'notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    loadSavedSchedule() {
        const saved = localStorage.getItem('schedule_maker_data');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                document.getElementById('schedule-name').value = data.name || 'My Schedule';
                document.getElementById('schedule-description').value = data.description || '';
                this.events = data.events || [];
                this.renderSchedule();
                this.showNotification('Saved schedule loaded!');
            } catch (e) {
                console.error('Error loading saved schedule:', e);
            }
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize the Schedule Maker when the page loads
document.addEventListener('DOMContentLoaded', () => {
    const scheduleMaker = new ScheduleMaker();
    
    // Try to load any saved schedule
    scheduleMaker.loadSavedSchedule();
    
    // Make it globally accessible for debugging
    window.scheduleMaker = scheduleMaker;
});
