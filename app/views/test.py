from app import app
from flask import request, redirect, url_for, session, render_template

@app.route('/test')
def test():
    print(str(request.args), flush=True)
    print(request.args['param'], flush=True)
    print(request.args['derpy'], flush=True)
    return render_template('login.html')