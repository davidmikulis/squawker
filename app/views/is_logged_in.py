from app import app
from flask import request, redirect, url_for, session, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Read user and flocks from database
from app.models.user import UserModel
from app.models.flock import FlockModel

# Landing page - check if user is in the database

@app.route('/is_logged_in')
def is_logged_in():
    user_id = request.args.get('user_id')
    access_token = request.args.get('access_token')
    user = UserModel.find_by_id_and_token(user_id, access_token)

    if user is not None:
        return redirect(url_for('timeline', user=user))
    else:
        return redirect(url_for('about'))