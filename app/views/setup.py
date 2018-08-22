from app import app
from flask import request, redirect, url_for, session, flash, render_template 

# Library to assist with Twitter APIs
import tweepy

# Obfuscation of key and secret
from app.utils.obfuscator import deobfuscate_str

from app.models.user import UserModel
from app.models.flock import FlockModel
from app.models.friend import FriendModel
# Page where the user sets up their flocks

# Check the access_token against the database, if it already
# exists then the user has been here before on a different
# browser or cleared their local storage. Read their settings
# from the database and restore their settings.

# To avoid rate limit errors, get a list of friend IDs from api
# Before retrieving friend data, check database for friend IDs and
# retrieve what we can. 
# Ask Twitter for the remaining friends

class Setup():
    pass

# Setup
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    key = session.get('access_token', None)
    secret = session.get('access_token_secret', None)
    if key and secret:
        deobf_key = deobfuscate_str(key, app.secret_key)
        deobf_secret = deobfuscate_str(secret, app.secret_key)
        auth.set_access_token(deobf_key, deobf_secret)
        api = tweepy.API(auth)

        # Gather list of all IDs for friends to show
        friend_ids = api.friends_ids()

        # Get a list of the friends and IDs stored in the DB
        db_friends = FriendModel.find_by_user_id_list(friend_ids)
        db_friend_ids = [friend.user_id for friend in db_friends]

        # Identify missing friends that need to be gathered from Twitter
        missing_friends = list(set(friend_ids).difference(db_friend_ids))
        print('Missing Friends:', flush=True)
        print(str(missing_friends), flush=True)

        # Setup list of friends to pass to HTML
        raw_friends = [] + db_friends
        friends_to_save = []

        # Gather the remaining friends from Twitter
        if len(missing_friends) > 0:
            try:
                for f in api.lookup_users(user_ids=missing_friends):
                    # Process the friend here
                    raw_friends.append(f)
                    friends_to_save.append(FriendModel(f.id, f.screen_name, f.name, f.verified, f.profile_image_url_https))
                if len(friends_to_save) > 0:
                    FriendModel.bulk_save_to_db(friends_to_save)
            except tweepy.RateLimitError:
                return render_template('rate_limit.html', action='friends')

        return render_template('setup.html', friends_list=raw_friends, key=deobf_key, secret=deobf_secret)