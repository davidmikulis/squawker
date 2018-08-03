# Basic Flask
from flask import Flask

# SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Initialize application
app = Flask(__name__)


# Load application configuration
app.config.from_pyfile('config.cfg')
# app.secret_key = os.urandom(32)
db = SQLAlchemy(app)

# Import views defined in __init__/__all__
from app.views import *

@app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception as e:
        print(e, flush=True)