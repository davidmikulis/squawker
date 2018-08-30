from app import app
from flask import request, redirect, url_for, session, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Read user and flocks from database
from app.models.user import UserModel
from app.models.flock import FlockModel

# Deobfuscate id and token
from app.utils.obfuscator import deobfuscate_str
from app.utils.obfuscator import deobfuscate_user_id

# Landing page - check if user is in the database

@app.route('/is_logged_in/<string:user_id>/<string:access_token>/')
def is_logged_in(user_id, access_token):
    user_id = request.args.get('user_id')
    access_token = request.args.get('access_token')
    deobf_user_id = deobfuscate_user_id(user_id, app.secret_key)
    deobf_access_token = deobfuscate_str(access_token, app.secret_key)
    user = UserModel.find_by_id_and_token(deobf_user_id, deobf_access_token)

    if user is not None:
        return redirect(url_for('timeline', user=user))
    else:
        return redirect(url_for('login'))