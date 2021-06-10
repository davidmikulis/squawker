from app import app
from flask import request, redirect, url_for, session, render_template

# Library to assist with Twitter APIs
import tweepy

# Save our user to the database
from app.models.user import UserModel


# Initiates OAuth process. User won't see this page
@app.route('/request_token')
def get_oauth_request_token():
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'], app.config['CALLBACK_URL'])

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.', flush=True)

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
        print('Error! Failed to get access token.', flush=True)

    # Store the token and secret in the session
    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    # Check if this user has used the app before
    user = UserModel.find_by_access_token(auth.access_token)
    if user is not None and user.last_flock_id:
        # User has used this app before but on a different browser/cleared local storage
        # Save User ID and Access Token to local storage and redirect to timeline
        return redirect(url_for('save_to_local_storage', access_token=auth.access_token, user_id=user.user_id, redirect='timeline'))
    elif user is not None:
        # User has used this app before but never saved a flock
        # Save User ID and Access Token to local storage and redirect to setup
        return redirect(url_for('save_to_local_storage', access_token=auth.access_token, user_id=user.user_id, redirect='setup'))

    # User hasn't used this app before
    new_user = UserModel(auth.access_token, auth.access_token_secret)
    try:
        saved_user = new_user.save_to_db()
    except:
        print('Error occured saving user to database', flush=True)

    # Save User ID and Access Token to local storage and redirect to about
    return redirect(url_for('save_to_local_storage', access_token=auth.access_token, user_id=user.user_id, redirect='about'))


@app.route('/denied')
def denied():
    return render_template('denied.html')