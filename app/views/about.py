from app import app
from flask import request, redirect, url_for, session, render_template

@app.route('/about')
def about():
    return render_template('about.html',
        home_selected='',
        setup_selected='',
        about_selected='-selected'
        )