from app import app
from flask import request, redirect, url_for, session, flash, render_template 

# Library to assist with Twitter APIs
import tweepy

# Obfuscation of key and secret
from app.utils.obfuscator import deobfuscate_str

from app.models.user import UserModel
from app.models.flock import FlockModel
# Page where the user sets up their flocks

# Check the access_token against the database, if it already
# exists then the user has been here before on a different
# browser or cleared their local storage. Read their settings
# from the database and restore their settings.

class Setup():
    pass

# Setup
@app.route('/setup')
def setup():
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = session.get('access_token', None)
    secret = session.get('access_token_secret', None)
    if key and secret:
        deobf_key = deobfuscate_str(key, app.secret_key)
        deobf_secret = deobfuscate_str(secret, app.secret_key)
        auth.set_access_token(deobf_key, deobf_secret)
        api = tweepy.API(auth)
        raw_friends = []
        try:
            for friend in tweepy.Cursor(api.friends).items():
                # Process the friend here
                raw_friends.append(friend)
            return render_template('setup.html', friends_list=raw_friends, key=deobf_key, secret=deobf_secret)
        except tweepy.RateLimitError:
            return render_template('rate_limit.html', action='friends')