from app import app
from flask import request, redirect, url_for, session, flash, render_template

@app.route('/')
def landing():
    return render_template('landing.html')