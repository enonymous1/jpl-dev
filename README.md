# JPL-DEV - Justin P. Lyons Digital Portfolio

Hey there, welcome to my digital sandbox! Here, I experiment with code, share my musings, and build things that spark joy. Grab a seat, explore, and let's get acquainted!

## 🚀 Live Site
Visit the live site at: [justinlyons.dev](https://justinlyons.dev)

## 🛠️ Development

This is a Flask-based static site that gets generated and deployed to GitHub Pages.

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Generate Static Site
```bash
# Generate static site in docs/ directory
python freeze.py
```

## 📦 Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch via GitHub Actions. The deployment:

1. Installs Python dependencies
2. Runs Flask-Frozen to generate static files
3. Deploys to GitHub Pages with custom domain
4. Serves the site at justinlyons.dev

## 🎨 Features

- **Modular CSS Architecture** - Split into logical modules for maintainability
- **Dark/Light Theme Toggle** - Automatic theme switching with system preference detection
- **Interactive GSA MAS Checklist** - A comprehensive tool for GSA proposal preparation
- **Responsive Design** - Works seamlessly across all device sizes
- **Smart Tooltips** - Intelligent positioning to prevent off-screen issues

## 📁 Project Structure

```
├── app.py                 # Flask application
├── freeze.py             # Static site generator
├── templates/            # Jinja2 templates
├── static/               # Static assets
│   ├── css/             # Modular CSS files
│   ├── files/           # Downloadable resources
│   └── projects/        # Project-specific assets
├── projects/            # Blueprint modules
├── docs/                # Generated static site (GitHub Pages)
└── .github/workflows/   # GitHub Actions for deployment
```
