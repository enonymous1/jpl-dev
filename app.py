from flask import Flask, render_template
from flask_frozen import Freezer
from projects.gsa_mas_checklist import gsa_mas_checklist_bp

app = Flask(__name__)
app.config['FREEZER_DESTINATION'] = 'docs'
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

# Register project blueprints
app.register_blueprint(gsa_mas_checklist_bp)

# Custom filter to convert newlines to HTML breaks
@app.template_filter('nl2br')
def nl2br_filter(text):
    if text is None:
        return ''
    return text.replace('\n', '<br>\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
