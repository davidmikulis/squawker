from main import app
from flask import request, redirect, url_for, session, g, flash, render_template

# Library to assist with Twitter APIs
import tweepy

# Date and time libraries
from datetime import datetime


class Timeline():
    def datamine_media(self, media):
        if media is not None:
            own_url = media[0].get('url', None)
            media_url = media[0].get('media_url_https', None)
            return own_url, media_url
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
@app.route('/')
def timeline():
    logged_in = False
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = session.get('access_token', None)
    secret = session.get('access_token_secret', None)
    processed_tweets = []
    if key and secret:
        logged_in = True
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        raw_tweets = api.home_timeline(tweet_mode='extended')
        tl = Timeline()
        for tweet in raw_tweets:
            if hasattr(tweet, 'retweeted_status'):
                status = tweet.retweeted_status
                tweet_type = 'retweet'
            elif tweet.is_quote_status:
                status = tweet
                tweet_type = 'quote'
            else:
                status = tweet
                tweet_type = 'tweet'
            url_list = status.entities.get('urls', [])
            hashtags_list = status.entities.get('hashtags', [])
            mentions_list = status.entities.get('user_mentions', [])
            own_url, media_url = tl.datamine_media(status.entities.get('media', None))
            processed_text = tl.process_text(status.full_text, hashtags_list, mentions_list, url_list, own_url)
            # Assigned mined values to tweet object
            tweet.text_list = processed_text.splitlines()
            tweet.media_url = media_url
            tweet.tweet_type = tweet_type
            processed_tweets.append(tweet)
    return render_template('timeline.html', tweets=processed_tweets, logged_in=logged_in)

# Testing
# def timeline():
#     logged_in = False
#     auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
#     key = session.get('access_token', None)
#     secret = session.get('access_token_secret', None)
#     if key and secret:
#         logged_in = True
#         auth.set_access_token(key, secret)
#         api = tweepy.API(auth)
#         tweet = api.get_status('1022555951801487362', tweet_mode='extended')
#         tl = Timeline()
#         if hasattr(tweet, 'retweeted_status'):
#             status = tweet.retweeted_status
#             tweet_type = 'retweet'
#         elif tweet.is_quote_status:
#             status = tweet
#             tweet_type = 'quote'
#         else:
#             status = tweet
#             tweet_type = 'tweet'
#         url_list = status.entities.get('urls', None)
#         hashtags_list = status.entities.get('hashtags', None)
#         mentions_list = status.entities.get('user_mentions', None)
#         own_url, media_url = tl.datamine_media(status.entities.get('media', None))
#         print(status.full_text, flush=True)
#         processed_text = tl.process_text(status.full_text, hashtags_list, mentions_list, url_list, own_url)
#         # Assigned mined/processed values to tweet object
#         tweet.text_list = processed_text.splitlines()
#         tweet.media_url = media_url
#         tweet.tweet_type = tweet_type
#         tweet.time_stamp_str = tl.time_stamp_str(tweet.created_at)

#         return render_template('timeline_test.html', 
#             tweet=tweet, 
#             logged_in=logged_in
#         )
    
#     return render_template('timeline_test.html',
#         logged_in=logged_in
#     )