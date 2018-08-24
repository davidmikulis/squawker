from app import app
from flask import request, redirect, url_for, session, render_template

@app.route('/login')
def login():
    # key = session.get('access_token', None)
    # secret = session.get('access_token_secret', None)
    # print(f'key {key}', flush=True)
    # print(f'secret {secret}', flush=True)
    # if key and secret:
    #     return redirect(url_for('timeline'))
    return render_template('login.html')