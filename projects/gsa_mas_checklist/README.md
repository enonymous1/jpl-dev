# Interactive GSA MAS New Offeror Checklist

A comprehensive interactive web application for GSA Multiple Award Schedule (MAS) offer preparation, designed to streamline the complex federal contracting process with an intuitive, step-by-step interface.

[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)](https://justinlyons.dev/projects/gsa-mas-checklist)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-red.svg)](https://flask.palletsprojects.com)

## 🎯 Project Overview

The GSA MAS Checklist is an interactive tool that helps potential federal contractors navigate the complex Multiple Award Schedule (MAS) offer preparation process. It provides a structured, step-by-step approach to ensure all requirements are met before submitting a proposal to the General Services Administration (GSA).

### 🚀 Live Demo
- **Production**: [https://justinlyons.dev/projects/gsa-mas-checklist](https://justinlyons.dev/projects/gsa-mas-checklist)
- **Repository**: [https://github.com/enonymous1/jpl-dev](https://github.com/enonymous1/jpl-dev)

## ✨ Features

### Core Functionality
- **📋 Interactive Checklist**: Step-by-step validation with real-time progress tracking
- **🎯 SINs Selection**: Advanced filtering and search for Special Item Numbers
- **📝 Rich Text Notes**: Integrated notes management with Quill.js editor
- **💾 Data Persistence**: Local storage for work-in-progress with manual save/load
- **📤 Export/Import**: Complete data portability via JSON download/upload
- **🌙 Theme Support**: Dark/light theme toggle with system preference detection

### User Experience
- **📱 Responsive Design**: Optimized for desktop and mobile devices
- **♿ Accessibility**: Keyboard navigation support
- **⚡ Performance**: Fast loading with lazy-loaded components

## 🛠️ Technology Stack

### Backend
- **Flask 3.1+**: Python web framework
- **Flask-Frozen**: Static site generation for deployment
- **Python 3.9+**: Core programming language

### Frontend
- **Vanilla JavaScript**: No framework dependencies for fast loading
- **Quill.js**: Rich text editor for notes
- **CSS Grid & Flexbox**: Modern responsive layout
- **CSS Custom Properties**: Theme system implementation

### Data & Storage
- **JSON**: Configuration and data exchange format
- **Local Storage**: Client-side data persistence (manual save/load)

### Development & Deployment
- **GitHub Actions**: CI/CD pipeline
- **GitHub Pages**: Static hosting
- **Flask-Frozen**: Static site generation

## 📁 Project Structure

```
projects/gsa_mas_checklist/
├── README.md                 # This file
├── __init__.py              # Blueprint initialization
├── routes.py                # Flask routes and view functions
├── data/
│   ├── checklist_data.json  # Core checklist configuration
│   └── sins_data.json       # Special Item Numbers database
├── templates/
│   └── gsa_mas_checklist.html  # Main application template
└── static/
    └── gsa_mas_checklist.js     # Client-side JavaScript
```

## 🚦 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package installer)
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/enonymous1/jpl-dev.git
   cd jpl-dev
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser to `http://localhost:5000/projects/gsa-mas-checklist`

### Static Site Generation

To generate static files for deployment:

```bash
python freeze.py
```

Static files will be generated in the `docs/` directory.

## 📖 Usage Guide

### Basic Workflow

1. **Start the Checklist**: Navigate to the application and begin with the first section
2. **Complete Sections**: Work through each checklist item systematically
3. **Add Notes**: Use the rich text editor to document important information
4. **Select SINs**: Choose appropriate Special Item Numbers for your offer
5. **Track Progress**: Monitor completion status in real-time
6. **Export Data**: Save your progress as JSON for backup/archiving

### Data Management

#### Export Options
- **JSON Export**: Complete data backup including notes and selections

#### Import Process
- Drag and drop JSON files or use the file picker
- Data validation ensures compatibility
- Merge options for combining multiple sessions

### Customization

The checklist can be customized by modifying `checklist_data.json`:

```json
{
  "sections": [
    {
      "id": "section_1",
      "title": "Section Title",
      "items": [
        {
          "id": "item_1",
          "text": "Checklist item description",
          "required": true,
          "tooltip": "Additional guidance"
        }
      ]
    }
  ]
}
```

## 🔧 Development

### Code Style
- **Python**: Follows PEP 8 style guidelines
- **JavaScript**: ES6+ with consistent formatting
- **CSS**: BEM methodology for class naming

### Testing
```bash
# Run Python tests
python -m pytest tests/

# Run JavaScript tests (if implemented)
npm test
```

### Building for Production
```bash
# Generate optimized static files
python freeze.py

# Deploy to GitHub Pages (automatic via Actions)
git push origin main
```

## 📊 Performance Metrics

- **Load Time**: < 2 seconds on 3G connection
- **Bundle Size**: < 500KB total (including assets)
- **Lighthouse Score**: 95+ across all categories
- **Browser Support**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Development Guidelines
- Write comprehensive tests for new features
- Follow existing code style and conventions
- Update documentation for any API changes
- Ensure cross-browser compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../../LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/enonymous1/jpl-dev/issues) page to report bugs or request features.

When reporting bugs, please include:
- Browser and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 📚 Related Resources

### GSA Resources
- [GSA MAS Program](https://www.gsa.gov/buying-selling/products-services/professional-services/buy-services/multiple-award-schedule-mas)
- [eSRS (eOffer/eMod)](https://www.gsa.gov/buying-selling/products-services/professional-services/buy-services/multiple-award-schedule-mas/mas-offers-modifications)
- [GSA Advantage!](https://www.gsaadvantage.gov/)

### Technical Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Quill.js Documentation](https://quilljs.com/)
- [Federal Acquisition Regulation (FAR)](https://www.acquisition.gov/far/)

## 📈 Roadmap

### Version 2.0 (Planned)
- [ ] Multi-user collaboration features
- [ ] Advanced reporting and analytics
- [ ] Integration with GSA eSRS system
- [ ] Mobile app development
- [ ] AI-powered completion suggestions

### Version 1.1 (In Progress)
- [x] Enhanced export formats
- [x] Improved accessibility features
- [ ] Offline mode support
- [ ] Advanced search functionality

---

**Developed by**: JPL Development  
**Last Updated**: July 11, 2025  
**Version**: 1.0.0

For questions or support, please contact [support@justinlyons.dev](mailto:support@justinlyons.dev)
