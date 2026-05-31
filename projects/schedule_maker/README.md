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

### Implemented
- **🗓️ Weekly Schedule Grid**: Visual week-at-a-glance grid with configurable shifts
- **👤 Employee Roster Management**: Add, edit, and remove employees with phone/email/notes
- **🗓️ Shift Assignment**: Assign employees to shifts via modal dialogs
- **🔍 Employee Details Popover**: Hover over an employee pill to see contact info and availability rules
- **📅 Date Navigation**: Move forward/backward through weeks
- **🌙 Theme Support**: Inherits the portfolio dark/light theme system

### Planned
- **💾 Data Persistence**: Save/load schedules to local storage between sessions
- **📤 Export/Import**: Save schedules as JSON; restore from file
- **🎨 Drag-and-Drop**: Move shifts between time slots by dragging
- **⚠️ Conflict Detection**: Real-time detection of scheduling conflicts
- **🔄 Auto-save**: Periodic automatic saving to prevent data loss

## 🛠️ Technology Stack

### Frontend
- **JavaScript ES6+**: Modern JavaScript features for enhanced functionality
- **CSS Grid & Flexbox**: Advanced layout techniques for responsive design
- **HTML5**: Semantic markup for accessibility
- **Canvas API**: Advanced graphics for timeline rendering (planned)

### Backend
- **Flask 3.1+**: Python web framework
- **Flask Blueprints**: Modular application architecture (reference pattern for other blueprints)

### Data Management
- **In-memory state**: Employees, schedules, and shift info live in module-level variables
- **No persistence yet**: Page refresh resets to seed/demo data (see Planned features)

## 📁 Project Structure

```
projects/schedule_maker/
├── README.md                    # This documentation
├── __init__.py                  # Blueprint initialization
├── routes.py                    # Flask route (renders template, no API endpoints)
└── templates/
    └── schedule_maker.html      # Main application template

static/projects/schedule_maker/
├── script.js                    # ✅ ACTIVE — main application logic
└── style.css                    # ✅ ACTIVE — project-specific styles
```

## 🚦 Getting Started

### Prerequisites
- Python 3.9 or higher
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

### Creating Shifts

1. **Navigate to the schedule** via the weekly grid
2. **Click a shift cell** to assign an employee
3. **Select an employee** from the modal dialog
4. **Save** to update the schedule grid

### Managing Employees

- **Add employee**: Use the employee roster panel (name, phone, email, notes, availability rules)
- **Edit employee**: Click the edit icon next to any roster entry
- **Remove employee**: Click the remove icon (also removes that employee from all assigned shifts)
- **View details**: Hover over an employee pill in the schedule grid to see a contact popover

### Date Navigation

- Use the **prev/next week** buttons to move through the schedule
- Current week is highlighted in the grid header

### Data Management

> ⚠️ Schedule data is currently in-memory only. Refreshing the page resets to the demo seed data.
> Save/load and export features are planned for a future release.

## 🔧 Development

### Architecture

The active application lives in `static/projects/schedule_maker/script.js`.
It uses module-level state variables (`employees`, `allSchedules`, `shiftInfo`) and
vanilla DOM manipulation — no class wrappers or build tools required.

Key functions:
- `renderSchedule()` — builds the weekly grid
- `renderAvailableEmployees()` — populates the employee roster panel
- `showShiftModal()` / `closeModal()` — shift assignment dialog
- `addEmployee()` / `removeEmployee()` — roster management
- `showEmployeePopover()` / `hideEmployeePopover()` — hover contact card

### Local Development

```bash
# Watch for changes during development
python app.py

# Access the application
http://localhost:5000/projects/schedule-maker
```

## 🎨 Customization

### Themes
The Schedule Maker inherits the portfolio’s theme system:
- Automatic dark/light mode detection
- Consistent color palette with the main site

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
- [ ] Local storage persistence
- [ ] Export functionality
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
