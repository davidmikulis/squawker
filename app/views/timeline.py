from app import app
from flask import request, redirect, url_for, session, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Date and time libraries
from datetime import datetime

# Database models
from app.models.user import UserModel

# Obfuscator utility
from app.utils.obfuscator import deobfuscate_str


class Timeline():
    def apply_flock_filter(self, raw_tweets, friend_ids):
        return [tweet for tweet in raw_tweets if tweet.user.id_str in friend_ids]

    def datamine_media(self, media):
        if media is not None:
            own_url = media[0].get('url', None)
            media_urls = [m.get('media_url_https', None) for m in media]
            return own_url, media_urls
        return None, None

    def process_text(self, text, hashtags_list, mentions_list, url_list, own_url):
        processed_text = text
        processed_text = self.replace_hashtags(processed_text, hashtags_list)
        processed_text = self.replace_mentions(processed_text, mentions_list)
        processed_text = self.replace_urls(processed_text, url_list)
        processed_text = self.remove_own_url(processed_text, own_url)
        return processed_text

    def replace_hashtags(self, text, hashtags_list):
        for hashtag in hashtags_list:
            text = text.replace('#' + hashtag['text'], '<a href="https://twitter.com/hashtag/{h}" target="_blank">#{h}</a>'.format(h=hashtag['text']))
        return text

    def replace_mentions(self, text, mentions_list):
        for mention in mentions_list:
            text = text.replace('@' + mention['screen_name'], '<a href="https://twitter.com/{m}" target="_blank">@{m}</a>'.format(m=mention['screen_name']))
        return text

    def replace_urls(self, text, url_list):
        for url in url_list:
            text = text.replace(url['url'], '<a href="{}" target="_blank">{}</a>'.format(url['url'], url['display_url']))
        return text

    def remove_own_url(self, text, own_url):
        if own_url is not None:
            return text.replace(own_url, '')
        else:
            return text

    def time_stamp_str(self, created_at):
        print(str(created_at))
        # processed_time = datetime.strptime(str(created_at),'%a %b %d %H:%M:%S +0000 %Y')
        # print(processed_time, flush=True)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), flush=True)

# Timeline
@app.route('/t')
def timeline():
    obf_key = session.get('access_token', None)
    obf_secret = session.get('access_token_secret', None)
    if obf_key is None or obf_secret is None:
        return render_template('login.html')
    # Read user from request or search DB
    user = request.args.get('user', None)
    if user is None:
        user = UserModel.find_by_access_token(obf_key)
    # Prepare to use Twitter API
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = deobfuscate_str(obf_key, app.secret_key)
    secret = deobfuscate_str(obf_secret, app.secret_key)
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    tl = Timeline()
    # Acquire tweets from Twitter and filter by flock members
    raw_tweets = api.home_timeline(tweet_mode='extended', count=200)
    print(len(raw_tweets), flush=True)
    filtered_tweets = tl.apply_flock_filter(raw_tweets, user.last_flock().chosen_ids())
    print(len(filtered_tweets), flush=True)
    # Perform additional processing on the Tweet objects
    processed_tweets = []
    for tweet in filtered_tweets:
        tweet_types = []
        status = tweet
        if hasattr(tweet, 'retweeted_status'):
            status = tweet.retweeted_status
            tweet_types.append('retweet')
        if hasattr(tweet, 'quoted_status'):
            tweet_types.append('quote')

        url_list = status.entities.get('urls', [])
        hashtags_list = status.entities.get('hashtags', [])
        mentions_list = status.entities.get('user_mentions', [])
        own_url, media_urls = tl.datamine_media(status.entities.get('media', None))
        processed_text = tl.process_text(status.full_text, hashtags_list, mentions_list, url_list, own_url)
        # Assigned mined values to tweet object
        tweet.text_list = processed_text.splitlines()
        tweet.media_urls = media_urls
        tweet.tweet_types = tweet_types
        processed_tweets.append(tweet)
    return render_template('timeline.html', tweets=processed_tweets)
