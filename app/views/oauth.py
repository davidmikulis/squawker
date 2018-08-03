from app import app
from flask import request, redirect, url_for, session, render_template

# Library to assist with Twitter APIs
import tweepy

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

    denied = request.args.get('denied')
    if denied:
        return redirect(url_for('denied'))
    
    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    request_token = session['request_token']
    del session['request_token']

    auth.request_token = request_token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    api = tweepy.API(auth)

    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('setup'))


@app.route('/denied')
def denied():
    return render_template('denied.html')