import os
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable debug mode.
DEBUG = True

# Connect to the database

# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql://databaseweb:pass_admin@postgresql-databaseweb.alwaysdata.net:5432/databaseweb_fyyur_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yanord:yanord@localhost/cl_dbname'

print(os.getenv("FLASK_ENV"))
if "development" == os.getenv("FLASK_ENV"):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://admin:pass_admin@localhost:5432/fyyur_db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yanord:yanord@localhost:3306/cl_dbname'
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://databaseweb:pass_admin@postgresql-databaseweb.alwaysdata.net:5432/databaseweb_fyyur_db'



# SQLALCHEMY_ECHO = True


app = Flask(__name__)
# moment = Moment(app)
# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Service, Activite, Fichier


db.app = app
db.init_app(app)
# db.drop_all()
# db.create_all()


# migrate = Migrate(app, db)
# db.init_app(app)
