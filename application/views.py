from main import app
from flask import request, redirect, url_for, session, g, flash, render_template
import re

# Library to assist with Twitter APIs
import tweepy

# Home page
@app.route('/')
def timeline():
    logged_in = False
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = session.get('access_token', None)
    secret = session.get('access_token_secret', None)
    tweets = []
    if key and secret:
        logged_in = True
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        raw_tweets = api.home_timeline(tweet_mode='extended')
        mention_re = re.compile(r'@([\w]+)')
        hashtag_re = re.compile(r'#([\w]+)')
        for tweet in raw_tweets:
            full_text = mention_re.sub(r'<a href="https://twitter.com/\1">@\1</a>', tweet.full_text)
            full_text = hashtag_re.sub(r'<a href="https://twitter.com/hashtag/\1">#\1</a>', full_text)
            tweet.text_list = full_text.splitlines()
            # tweet.media_url = tweet.entities['media'][0]['media_url_https']
            tweets.append(tweet)
    return render_template('home.html', tweets=tweets, logged_in=logged_in)

# def timeline():
#     logged_in = False
#     auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
#     key = session.get('access_token', None)
#     secret = session.get('access_token_secret', None)
#     if key and secret:
#         logged_in = True
#         auth.set_access_token(key, secret)
#         api = tweepy.API(auth)
#         tweet = api.get_status('1022257363833839617', tweet_mode='extended')
#         mention_re = re.compile(r'@([\w]+)')
#         hashtag_re = re.compile(r'#([\w]+)')
#         full_text = mention_re.sub(r'<a href="https://twitter.com/\1">@\1</a>', tweet.full_text)
#         full_text = hashtag_re.sub(r'<a href="https://twitter.com/hashtag/\1">#\1</a>', full_text)
#         tweet.text_list = full_text.splitlines()

#         # tweet.mention_list = [mention['id_str'] for mention in tweet.entities['user_mentions']]
#         tweet.media_url = tweet.entities['media'][0]['media_url_https']

#         return render_template('home_test.html', 
#             tweet=tweet, 
#             logged_in=logged_in
#         )
    
#     return render_template('home_test.html',
#         logged_in=logged_in
#     )
 
@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))
