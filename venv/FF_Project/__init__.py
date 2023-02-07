import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'mysecret'

######################################################
### Database set up ##################################
######################################################

basedir = os.path.abspath(os.path.dirname(__file__))
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()
Migrate(app,db)
db.create_all()

######################################################
### Blueprint set up #################################
######################################################

from FF_Project.views import core
from FF_Project.models import data

app.register_blueprint(core)
app.register_blueprint(data)