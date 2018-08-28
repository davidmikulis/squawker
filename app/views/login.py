from app import app
from flask import request, redirect, url_for, session, render_template

@app.route('/login')
def login():
    return render_template('login.html')