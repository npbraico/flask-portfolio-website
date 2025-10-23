from flask import Flask
from flask import render_template, request, redirect, url_for
import DAL

app = Flask(__name__)

# Flask 3.x removed before_first_request; call initializer at import time instead
try:
    DAL.ensure_db()
except Exception as e:
    print(f"DB init error: {e}")
@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    title = request.form.get('title')
    description = request.form.get('description')
    image_filename = request.form.get('image_filename')
    
    DAL.addProject(title, description, image_filename)
    
    return redirect(url_for('projectsPage'))

@app.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    DAL.deleteProject(project_id)
    return redirect(url_for('projectsPage'))

@app.route('/index')
def indexPage():
    return render_template('index.html')

@app.route('/projects')
def projectsPage():
    projects = DAL.getAllProjects()
    return render_template('projects.html', projects=projects)

@app.route('/resume')
def resumePage():
    return render_template('resume.html')

@app.route('/thankyou')
def thankYouPage():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)