from flask import Flask
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app=Flask(__name__)
app.config['SECRET_KEY']='653e33351c6f4a262c1bceda061a6cb3'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager=LoginManager(app)
from flask_1 import routes