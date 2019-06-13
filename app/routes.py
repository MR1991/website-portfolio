from app import app
from flask import render_template
@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/startup')
def index2():
    return render_template('startup.html')

@app.route('/about')
def index3():
    return render_template('index.html')

@app.route('/contact')
def index4():
    return render_template('index.html')
