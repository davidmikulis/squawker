from app import app
from flask import request, redirect, url_for, session, flash, render_template 
import json
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
# TODO: Cache friend IDs in session variable

# On 'GET', check for their latest flock, and send back those friends
# If no latest flock, send back all friends

# On 'POST', gather the flock that the user sent and save it to the database
# Return the same page with a success message

class Setup():
    pass

# Setup
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        flock_name = request.form.get('name', '')
        available_friend_ids = json.loads(request.form.get('available_friends', '[]'))
        chosen_friend_ids = json.loads(request.form.get('chosen_friends', '[]'))

        # Get user from DB for user ID
        user = UserModel.find_by_access_token(session.get('access_token'))
        user_id = user.user_id

        # Save flock to DB
        flock = FlockModel.find_by_name(user_id, flock_name)
        if flock is not None:
            flock.config = {'chosen_friend_ids': chosen_friend_ids}
        else:
            flock = FlockModel(user_id, flock_name, {'chosen_friend_ids': chosen_friend_ids})

        try:
            saved_flock = flock.save_to_db()
        except:
            flash('There was an issue saving this flock, please try again.', 'danger')

        # Save latest flock to user
        user.last_flock_id = saved_flock.flock_id
        try:
            saved_user = user.save_to_db()
        except:
            flash('There was an issue saving this flock, please try again.', 'danger')

        flash(f'Flock "{flock_name}" has been saved.', 'success')
        # Turn the received IDs back into "Friend objects" from DB to re-render
        # Can refactor later to use session to avoid DB call
        available_friends = FriendModel.find_by_id_str_list(available_friend_ids)
        chosen_friends = FriendModel.find_by_id_str_list(chosen_friend_ids)

        return render_template('setup.html', 
            available_friends=available_friends, 
            chosen_friends=chosen_friends,
            flock_name=saved_flock.name,
            home_selected='',
            setup_selected='-selected',
            about_selected=''
            )

    if request.method == 'GET':
        auth = tweepy.OAuthHandler(app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
        key = session.get('access_token', None)
        secret = session.get('access_token_secret', None)
        if key is None or secret is None:
            return redirect(url_for('login'))
        
        deobf_key = deobfuscate_str(key, app.secret_key)
        deobf_secret = deobfuscate_str(secret, app.secret_key)
        auth.set_access_token(deobf_key, deobf_secret)
        api = tweepy.API(auth)

        # Gather list of all IDs for friends to show
        friend_ids = [str(_id) for _id in api.friends_ids()]
        # Get a list of the friends and IDs stored in the DB
        db_friends = FriendModel.find_by_id_str_list(friend_ids)
        db_friend_ids = [friend.id_str for friend in db_friends]
        # Identify missing friends that need to be gathered from Twitter
        missing_friends = list(set(friend_ids).difference(db_friend_ids))
        all_friends = [] + db_friends
        friends_to_save = []

        # Gather the remaining friends from Twitter
        if len(missing_friends) > 0:
            try:
                for f in api.lookup_users(user_ids=missing_friends):
                    all_friends.append(f)
                    friends_to_save.append(FriendModel(f.id_str, f.screen_name, f.name, f.verified, f.profile_image_url_https))
                if len(friends_to_save) > 0:
                    FriendModel.bulk_save_to_db(friends_to_save)
            except tweepy.RateLimitError:
                return render_template('rate_limit.html', action='friends')

        # Get user from DB for user ID
        user = UserModel.find_by_access_token(session.get('access_token'))
        if user.last_flock_id:
            flock_name = user.last_flock().name
            chosen_friend_ids = user.last_flock().chosen_ids()
            chosen_friends = [friend for friend in all_friends if friend.id_str in chosen_friend_ids]
            available_friends = [friend for friend in all_friends if friend.id_str not in chosen_friend_ids]
        else:
            available_friends = all_friends
            chosen_friends = []
            flock_name = ''

        # Pass list of "User" object friends to HTML
        return render_template('setup.html', 
            available_friends=available_friends, 
            chosen_friends=chosen_friends, 
            flock_name=flock_name,
            home_selected='',
            setup_selected='-selected',
            about_selected=''
            )