from app import app
from flask import request, redirect, url_for, session, render_template

# Library to assist with Twitter APIs
import tweepy

# Save our user to the database
from app.models.user import UserModel

# Obfuscate the key and secret
from app.utils.obfuscator import obfuscate_str
from app.utils.obfuscator import obfuscate_user_id

# Initiates OAuth process. User won't see this page
@app.route('/request_token')
def get_oauth_request_token():
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'], app.config['CALLBACK_URL'])

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    session['request_token'] = auth.request_token

    return redirect(redirect_url)

# Callback URL to obtain access token
@app.route('/verify')
def get_oauth_access_token():

    # User denies permission to the app in Twitter
    denied = request.args.get('denied')
    if denied:
        return redirect(url_for('denied'))
    
    verifier = request.args['oauth_verifier']

    # Swap Request Token for Access Token
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    request_token = session['request_token']
    del session['request_token']

    auth.request_token = request_token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    # Obfuscate the token and secret
    obf_access_token = obfuscate_str(auth.access_token, app.secret_key)
    obf_access_token_secret = obfuscate_str(auth.access_token_secret, app.secret_key)

    # Store the token and secret in the session
    session['access_token'] = obf_access_token
    session['access_token_secret'] = obf_access_token_secret

    # Check if this user has used the app before
    user = UserModel.find_by_access_token(obf_access_token)
    if user is not None:
        # User has used this app before but on a different browser/cleared local storage
        access_token = user.access_token
        user_id = obfuscate_user_id(user.user_id, app.secret_key)
        # Save User ID and Access Token to local storage and redirect to timeline
        return redirect(url_for('save_to_local_storage', access_token=access_token, user_id=user_id, redirect='timeline'))

    user = UserModel(obf_access_token, obf_access_token_secret)
    try:
        user.save_to_db()
    except:
        print('Error occured saving user to database', flush=True)

    access_token = user.access_token
    user_id = obfuscate_user_id(user.user_id, app.secret_key)
    # Save User ID and Access Token to local storage and redirect to setup
    return redirect(url_for('save_to_local_storage', access_token=access_token, user_id=user_id, redirect='setup'))


@app.route('/denied')
def denied():
    return render_template('denied.html')