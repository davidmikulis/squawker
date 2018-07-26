from main import app
from flask import request, redirect, url_for, session, g, flash, render_template
import re

# Library to assist with Twitter APIs
import tweepy

class Timeline():
    def datamine_media(self, media):
        if media is not None:
            own_url = media[0].get('url', None)
            media_url = media[0].get('media_url_https', None)
            return own_url, media_url
        return None, None

    def generate_re(self):
        hashtag_re = re.compile(r'#([\w]+)')
        mention_re = re.compile(r'@([\w]+)')
        return hashtag_re, mention_re

    def process_text(self, text, hashtag_re, mention_re, url_list, own_url):
        processed_text = self.sub_hashtag_mention(text, hashtag_re, mention_re)
        processed_text = self.replace_urls(processed_text, url_list)
        processed_text = self.remove_own_url(processed_text, own_url)
        return processed_text

    def sub_hashtag_mention(self, text, hashtag_re, mention_re):
        hashtag_text = hashtag_re.sub(r'<a href="https://twitter.com/hashtag/\1" target="_blank">#\1</a>', text)
        hashtag_mention_text = mention_re.sub(r'<a href="https://twitter.com/\1" target="_blank">@\1</a>', hashtag_text)
        return hashtag_mention_text

    def replace_urls(self, text, url_list):
        url_text = text
        for url in url_list:
            url_text = url_text.replace(url['url'], '<a href="{}" target="_blank">{}</a>'.format(url['url'], url['display_url']))
        return url_text

    def remove_own_url(self, text, own_url):
        if own_url is not None:
            return text.replace(own_url, '')
        else:
            return text


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
        hashtag_re, mention_re = tl.generate_re()
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
            url_list = status.entities.get('urls', None)
            own_url, media_url = tl.datamine_media(status.entities.get('media', None))
            processed_text = tl.process_text(status.full_text, hashtag_re, mention_re, url_list, own_url)
            # Assigned mined values to tweet object
            tweet.text_list = processed_text.splitlines()
            tweet.media_url = media_url
            tweet.tweet_type = tweet_type
            processed_tweets.append(tweet)
    return render_template('timeline.html', tweets=processed_tweets, logged_in=logged_in)

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
#         hashtag_re, mention_re = tl.generate_re()
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
#         own_url, media_url = tl.datamine_media(status.entities.get('media', None))
        
#         processed_text = tl.process_text(status.full_text, hashtag_re, mention_re, url_list, own_url)
#         # Assigned mined/processed values to tweet object
#         tweet.text_list = processed_text.splitlines()
#         tweet.media_url = media_url
#         tweet.tweet_type = tweet_type

#         return render_template('timeline_test.html', 
#             tweet=tweet, 
#             logged_in=logged_in
#         )
    
#     return render_template('timeline_test.html',
#         logged_in=logged_in
#     )