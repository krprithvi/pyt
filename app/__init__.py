from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from config import basedir
from flask.ext.stormpath import (StormpathError, StormpathManager, User, login_required, login_user, logout_user, user,)

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
stormpath_manager = StormpathManager(app)
from app import views, models
