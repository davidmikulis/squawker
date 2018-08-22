from app import app
from flask import request, redirect, url_for, session, render_template

@app.route('/test')
def test():
    print(str(request.args), flush=True)
    print(request.args['param'], flush=True)
    print(request.args['derpy'], flush=True)
    return render_template('login.html')


def delta_time(cls, tweet_posted):
    now = datetime.datetime.now()
    td = now - tweet_posted
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    if days > 0:
        return tweet_posted.strftime("%d %B, %Y")
    elif hours > 0:
        return str(hours) + 'h'
    elif minutes > 0:
        return str(minutes) + 'm'
    else:
        return 'few seconds ago'

# error handlers
@app.errorhandler(404)
def not_found(e):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n404 error at {}: {}".format(current_timestamp, r))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n500 error at {}: {}".format(current_timestamp, r))
    return render_template('500.html'), 500