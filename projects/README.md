# JPL Development - Project Documentation

This directory contains individual project documentation and components for the JPL Development portfolio.

## 📁 Project Structure

```
projects/
├── README.md                     # This index file
├── __init__.py                   # Projects package initialization
└── gsa_mas_checklist/           # GSA MAS Checklist Project
    ├── README.md                # Detailed project documentation
    ├── __init__.py              # Blueprint initialization
    ├── routes.py                # Flask routes
    ├── templates/               # Project-specific templates
    └── static/                  # Project-specific assets
```

## 🚀 Available Projects

### 1. Interactive GSA MAS New Offeror Checklist
**Status**: Active ✅  
**Location**: `gsa_mas_checklist/`  
**Description**: A comprehensive interactive checklist for GSA Multiple Award Schedule offer preparation.

**Key Features**:
- Step-by-step checklist validation
- SINs selection with filtering
- Rich text notes management
- Data export/import capabilities
- Dark/light theme support

**Tech Stack**: Flask, JavaScript, CSS Grid, Local Storage

📖 **[View Full Documentation](gsa_mas_checklist/README.md)**

## 🏗️ Project Development Guidelines

### Adding New Projects

1. **Create Project Directory**
   ```bash
   mkdir projects/new_project_name
   ```

2. **Initialize as Flask Blueprint**
   ```python
   # projects/new_project_name/__init__.py
   from flask import Blueprint
   
   new_project_bp = Blueprint('new_project', __name__, 
                             url_prefix='/projects/new-project')
   
   from . import routes
   ```

3. **Register in Main App**
   ```python
   # app.py
   from projects.new_project_name import new_project_bp
   app.register_blueprint(new_project_bp)
   ```

4. **Add to Project Data**
   ```python
   # config/projects.py
   ProjectData(
       id="new_project",
       title="New Project Title",
       # ... other configuration
   )
   ```

5. **Create Project README**
   Use the GSA MAS Checklist README as a template.

### Documentation Standards

Each project should include:
- **README.md**: Comprehensive project documentation
- **Installation instructions**: Clear setup steps
- **Usage guide**: How to use the project
- **API documentation**: If applicable
- **Contributing guidelines**: Development workflow
- **License information**: Legal requirements

### Code Organization

- **Blueprint structure**: Each project as a Flask Blueprint
- **Template isolation**: Project templates in project directories
- **Static asset management**: Project-specific CSS/JS in static/
- **Data separation**: Configuration in config/ directory
- **Route prefixes**: Consistent URL patterns (`/projects/project-name`)

## 🔧 Development Workflow

### Local Development
1. Set up the main Flask application
2. Individual projects run as integrated blueprints
3. Use `python app.py` for development server
4. Projects accessible at `/projects/{project-name}`

### Static Site Generation
1. Use `python freeze.py` to generate static files
2. All projects included in static build
3. Deploy to GitHub Pages via GitHub Actions

### Testing Strategy
- **Unit tests**: Test individual project components
- **Integration tests**: Test project integration with main app
- **End-to-end tests**: Test complete user workflows
- **Accessibility tests**: Ensure WCAG compliance

## 📊 Project Status Overview

| Project | Status | Last Updated | Tech Stack |
|---------|--------|--------------|------------|
| GSA MAS Checklist | ✅ Active | 2025-07-11 | Flask, JavaScript, CSS |
| Future Project 1 | 📋 Planned | - | TBD |
| Future Project 2 | 📋 Planned | - | TBD |

## 🤝 Contributing to Projects

1. **Choose a project** from the available list or propose a new one
2. **Read the project README** for specific guidelines
3. **Follow the development workflow** outlined above
4. **Submit a pull request** with your changes
5. **Update documentation** as needed

## 📚 Additional Resources

- **Main Portfolio**: [justinlyons.dev](https://justinlyons.dev)
- **GitHub Repository**: [jpl-dev](https://github.com/enonymous1/jpl-dev)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Blueprint Patterns**: [Flask Blueprint Documentation](https://flask.palletsprojects.com/en/2.0.x/blueprints/)

---

**Maintained by**: JPL Development  
**Last Updated**: July 11, 2025
