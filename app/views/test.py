# from app import app
# from flask import request, redirect, url_for, session, render_template

import base64

def obfuscate_str(ori_str, key):
    enc = []
    for i in range(len(ori_str)):
        key_c = key[i % len(key)]
        enc_c = (ord(ori_str[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return (base64.urlsafe_b64encode(bytes(enc))).decode("utf-8")

def deobfuscate_str(enc_str, key):
    dec = []
    enc_str = base64.urlsafe_b64decode(enc_str)
    for i in range(len(enc_str)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc_str[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def obfuscate_user_id(ori_user_id, key):
    return obfuscate_str('user_id_'+str(ori_user_id), key)

def deobfuscate_user_id(enc_user_id, key):
    return deobfuscate_str(enc_user_id, key)[8:]

# @app.route('/test')
# def test():
#     print(str(request.args), flush=True)
#     print(request.args['param'], flush=True)
#     print(request.args['derpy'], flush=True)
#     return render_template('login.html')


# def delta_time(cls, tweet_posted):
#     now = datetime.datetime.now()
#     td = now - tweet_posted
#     days = td.days
#     hours = td.seconds//3600
#     minutes = (td.seconds//60)%60
#     if days > 0:
#         return tweet_posted.strftime("%d %B, %Y")
#     elif hours > 0:
#         return str(hours) + 'h'
#     elif minutes > 0:
#         return str(minutes) + 'm'
#     else:
#         return 'few seconds ago'

# # error handlers
# @app.errorhandler(404)
# def not_found(e):
#     if app.debug is not True:
#         now = datetime.datetime.now()
#         r = request.url
#         with open('error.log', 'a') as f:
#             current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
#             f.write("\n404 error at {}: {}".format(current_timestamp, r))
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(e):
#     db.session.rollback()
#     if app.debug is not True:
#         now = datetime.datetime.now()
#         r = request.url
#         with open('error.log', 'a') as f:
#             current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
#             f.write("\n500 error at {}: {}".format(current_timestamp, r))
#     return render_template('500.html'), 500

myDict = {}

key = myDict.get('key', None)
secret = myDict.get('secret', None)

if key and secret:
    print('we have key and secret')
else:
    print('we don\'t have key and secret')

print(deobfuscate_str('i5pycWVul2-TcXyteZt-pGzGkJ17sOVpiH2y4KyFrY2ae7uPn4abmWGnjryQn3ePu54=', 'Xf9837a6cD980c108dH149x810'))