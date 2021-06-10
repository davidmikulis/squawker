from app import app
from flask import request, redirect, url_for, session, flash, render_template 
import json

from app.models.user import UserModel

# User
@app.route('/get/user/<string:user_id>/<string:access_token>')
def user(user_id, access_token):
    user = UserModel.find_by_id_and_token(user_id, access_token)

    if user is None:
        response = {
            "error": "User not found."
        }
        return json.dumps(response)

    return json.dumps(user.json_me())

# Flock Names
@app.route('/get/flock_names')
def flock_names():
    user_id = request.args.get('user_id')
    access_token = request.args.get('access_token')
    user = UserModel.find_by_id_and_token(user_id, access_token)
    if user is None:
        response = {
            "error": "User not found."
        }
        return json.dumps(response)

    return json.dumps(user.flock_names())