import os

from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy

# allow http transport
# (https requires ssl keys, not good for local testing)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# init flask app
app = Flask(__name__)

# default values
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set database uri for SQLAlchemy
if os.environ.get('DB_URI') is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' \
        + os.path.join(basedir, '../database.sqlite3')

app.config['CSRF_ENABLED'] = True
app.secret_key = 'no one can guess this'
# enable debug for auto reloads
app.debug = True

# database
db = SQLAlchemy(app)
