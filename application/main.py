# Basic Flask
from flask import Flask

# Use Scss for styling
from flask_scss import Scss

# MySQL integration
# from flask_mysqldb import MySQL

# Read .env files
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Load environment variables and set configuration constants
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
CALLBACK_URL = "http://127.0.0.1:5000/verify"

# Initialize application
app = Flask(__name__)
from views import *
from oauth import *
# Load application configuration
app.config.from_pyfile('config.cfg')

# Initialize Scss
Scss(app, static_dir='static', asset_dir='assets')

# Initialize MySQL
# mysql = MySQL(app)


 
 
if __name__ == '__main__':
    app.run(host = '0.0.0.0')