from app import app
from flask import request, redirect, url_for, session, flash, render_template 

@app.route('/save_to_local_storage')
def save_to_local_storage():
    access_token = request.args.get('access_token', '')
    user_id = request.args.get('user_id', '')
    redirect_location = request.args.get('redirect', '')
    return render_template('save_to_local_storage.html', access_token=access_token, user_id=user_id, redirect=redirect_location)
