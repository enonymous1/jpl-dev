# Interactive Schedule Maker

A comprehensive schedule creation and management tool featuring drag-and-drop functionality, multiple view modes, and flexible export capabilities.

[![Status: Development](https://img.shields.io/badge/Status-Development-yellow)](https://justinlyons.dev/projects/schedule-maker)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Flask](https://img.shields.io/badge/Flask-3.1+-red.svg)](https://flask.palletsprojects.com)

## 🎯 Project Overview

The Schedule Maker is an interactive web application that simplifies schedule creation and management. It provides an intuitive interface for creating, editing, and organizing events with support for multiple view modes and comprehensive export options.

### 🚀 Live Demo
- **Development**: [https://justinlyons.dev/projects/schedule-maker](https://justinlyons.dev/projects/schedule-maker)
- **Repository**: [https://github.com/enonymous1/jpl-dev](https://github.com/enonymous1/jpl-dev)

## ✨ Features

### Core Functionality
- **📅 Multiple View Modes**: Day, week, and month views for different planning needs
- **🎨 Drag-and-Drop Interface**: Intuitive event creation and editing
- **🎨 Color-Coded Events**: Categorize events with custom colors
- **⚠️ Conflict Detection**: Real-time detection of scheduling conflicts
- **💾 Data Persistence**: Local storage for maintaining schedules between sessions
- **📤 Export Options**: Save schedules as JSON or calendar formats

### User Experience
- **📱 Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **⚡ Real-time Updates**: Instant feedback for all schedule changes
- **🔄 Auto-save**: Automatic saving to prevent data loss
- **📊 Visual Timeline**: Clear time slot visualization
- **🎯 Quick Actions**: Fast event creation with smart defaults

## 🛠️ Technology Stack

### Frontend
- **JavaScript ES6+**: Modern JavaScript features for enhanced functionality
- **CSS Grid & Flexbox**: Advanced layout techniques for responsive design
- **HTML5**: Semantic markup for accessibility
- **Canvas API**: Advanced graphics for timeline rendering (planned)

### Backend
- **Flask 3.1+**: Python web framework
- **Flask Blueprints**: Modular application architecture
- **RESTful API**: Clean API endpoints for data operations

### Data Management
- **Local Storage**: Client-side persistence
- **JSON**: Data exchange format
- **Calendar Export**: Standard calendar format support (planned)

## 📁 Project Structure

```
projects/schedule_maker/
├── README.md                    # This documentation
├── __init__.py                  # Blueprint initialization
├── routes.py                    # Flask routes and API endpoints
└── templates/
    └── schedule_maker.html      # Main application template

static/projects/schedule_maker/
├── schedule_maker.css           # Project-specific styles
└── schedule_maker.js           # Main application logic
```

## 🚦 Getting Started

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome 80+, Firefox 75+, Safari 13+, Edge 80+)

### Installation

1. **Navigate to project directory**
   ```bash
   cd jpl-dev
   ```

2. **Set up virtual environment** (if not already done)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   python app.py
   ```

5. **Access the Schedule Maker**
   Open your browser to `http://localhost:5000/projects/schedule-maker`

## 📖 Usage Guide

### Creating Events

1. **Click on a time slot** in the schedule grid to create a new event
2. **Fill in event details** in the popup form:
   - Event title (required)
   - Date and time range
   - Description (optional)
   - Color category
3. **Save the event** to add it to your schedule

### Managing Events

- **Edit events**: Click on existing events to modify details
- **Delete events**: Use the delete option in the edit form
- **Move events**: Drag events to different time slots (planned feature)
- **Resize events**: Adjust event duration by dragging edges (planned feature)

### View Controls

- **Day View**: Focus on a single day with detailed hourly breakdown
- **Week View**: See the full week with events displayed across days
- **Month View**: Overview of the entire month (coming soon)

### Data Management

#### Save & Load
- **Auto-save**: Changes are automatically saved to local storage
- **Manual save**: Use the save button for explicit saving
- **Load data**: Previous schedules are automatically loaded on page refresh

#### Export Options
- **JSON Export**: Download complete schedule data for backup
- **Calendar Export**: Import into other calendar applications (planned)

## 🔧 Development

### Architecture

The Schedule Maker follows a modular architecture:

```javascript
class ScheduleMaker {
    constructor()     // Initialize the application
    init()           // Set up event listeners and render initial view
    renderSchedule() // Main rendering logic for different views
    handleEvents()   // Event creation and management
    saveData()       // Data persistence logic
}
```

### Key Components

1. **Schedule Grid**: Main calendar interface with time slots
2. **Event Panel**: Modal for creating and editing events
3. **View Controls**: Buttons for switching between day/week/month views
4. **Date Navigation**: Controls for moving between time periods

### API Endpoints

```
POST /projects/schedule-maker/api/save-schedule
GET  /projects/schedule-maker/api/load-schedule/<id>
```

### Local Development

```bash
# Watch for changes during development
python app.py

# Access the application
http://localhost:5000/projects/schedule-maker
```

## 🎨 Customization

### Themes
The Schedule Maker inherits the portfolio's theme system:
- Automatic dark/light mode detection
- Consistent color palette with the main site
- Customizable event colors

### Configuration
Modify default settings in `schedule_maker.js`:

```javascript
const CONFIG = {
    defaultView: 'week',
    timeRange: { start: 6, end: 22 },
    colors: ['#4F46E5', '#10B981', '#F59E0B'],
    autoSave: true
};
```

## 📊 Performance

- **Load Time**: < 1 second on modern browsers
- **Memory Usage**: Optimized for handling 100+ events
- **Browser Support**: Modern browsers with ES6+ support
- **Mobile Performance**: Smooth interaction on touch devices

## 🗺️ Roadmap

### Version 1.0 (Current Development)
- [x] Basic schedule creation and viewing
- [x] Multiple view modes (Day, Week)
- [x] Event creation and editing
- [x] Local storage persistence
- [x] Export functionality
- [ ] Month view implementation
- [ ] Advanced conflict detection

### Version 1.1 (Planned)
- [ ] Drag-and-drop event movement
- [ ] Event categories and filtering
- [ ] Recurring events support
- [ ] Calendar import/export (.ics format)
- [ ] Print-friendly layouts

### Version 2.0 (Future)
- [ ] Multi-user collaboration
- [ ] Cloud synchronization
- [ ] Mobile app companion
- [ ] Integration with external calendars
- [ ] Advanced reporting and analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/schedule-improvement`)
3. Make your changes following the existing code style
4. Test thoroughly across different browsers
5. Commit with clear messages (`git commit -am 'Add recurring events feature'`)
6. Push to your branch (`git push origin feature/schedule-improvement`)
7. Create a Pull Request

### Development Guidelines
- Follow ES6+ JavaScript standards
- Maintain responsive design principles
- Test on multiple browsers and devices
- Update documentation for new features
- Ensure accessibility compliance

## 🐛 Known Issues

- Month view is not yet implemented
- Drag-and-drop functionality is planned for v1.1
- Internet Explorer is not supported (modern browsers only)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 📚 Related Resources

### Development Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [JavaScript ES6+ Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)

### Calendar Standards
- [iCalendar Specification](https://tools.ietf.org/html/rfc5545)
- [CalDAV Protocol](https://tools.ietf.org/html/rfc4791)

---

**Developed by**: JPL Development  
**Last Updated**: July 11, 2025  
**Version**: 1.0.0-dev  
**Status**: Active Development

For questions or support, please create an issue on GitHub or contact [support@justinlyons.dev](mailto:support@justinlyons.dev)
