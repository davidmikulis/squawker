# Basic Flask
from flask import Flask

# MySQL integration
# from flask_mysqldb import MySQL

# Initialize application
app = Flask(__name__)
from oauth import *
from setup import *
from timeline import *

# Load application configuration
app.config.from_pyfile('config.cfg')

# Initialize MySQL
# mysql = MySQL(app)
 
if __name__ == '__main__':
    app.run()