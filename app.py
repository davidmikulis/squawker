# app/main.py
# -*- coding: utf-8 -*-
from flask import Flask, request, redirect, url_for, session, g, flash, render_template

import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DEBUG=True
load_dotenv()
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
CALLBACK_URL = "http://127.0.0.1:5000/verify"

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = os.environ.get("DEVELOPMENT_KEY")





# @twitter.tokengetter
# def get_twitter_token(token=None):
#     return session.get('twitter_token')

@app.route('/')
def home():
    return "Hello world."

@app.route('/login')
def get_oauth_request_token():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    print('request token dict?', auth.request_token)
    print('request token', auth.request_token['oauth_token'], auth.request_token['oauth_token_secret'])
    session['request_token'] = (auth.request_token['oauth_token'], auth.request_token['oauth_token_secret'])

    return redirect(redirect_url)

@app.route('/verify')
def get_oauth_access_token():
    
    verifier = request.args['oauth_verifier']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    request_token = session['request_token']
    del session['request_token']

    auth.set_request_token(request_token[0], request_token[1])

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    
    api = tweepy.API(auth)

    print(api)
    print(auth.access_token['oauth_token'])

    return redirect(url_for('home'))


 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))

 
 
if __name__ == '__main__':
    app.run()