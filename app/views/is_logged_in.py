from app import app
from flask import request, redirect, url_for, session, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Landing page - check if user is logged in on local storage

@app.route('/is_logged_in/<string:user_id>/<string:access_token>/')
def is_logged_in(user_id, access_token):
    pass
