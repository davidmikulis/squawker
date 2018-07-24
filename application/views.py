from main import app
from flask import request, redirect, url_for, session, g, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Home page
@app.route('/')
def home():
    logged_in = False
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = session.get('access_token', None)
    secret = session.get('access_token_secret', None)
    tweet_text = []
    if key and secret:
        logged_in = True
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        # tweets = api.home_timeline(count=1)
        tweet = api.get_status('1021840695659843584')
        print(tweet.text)
        
    return render_template('home.html', tweet=tweet, logged_in=logged_in)

# Initiates OAuth process. User won't see this page
@app.route('/login')
def get_oauth_request_token():
    CALLBACK_URL = "http://127.0.0.1:5000/verify"
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'], CALLBACK_URL)

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

    print('PRINT', auth.access_token)
    print('PRINT', auth.access_token_secret)
    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('home'))

@app.route('/denied')
def denied():
    return render_template('denied.html')
 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
