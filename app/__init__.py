from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .home import home as home_blueprint
from .login import login as login_blueprint
from .config import Config

#application config
app = Flask(__name__)
app.secret_key = "cevacheiesecreta"
app.config.from_object(Config)

#database config
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    team = db.Column(db.String(64))
    level = db.Column(db.Integer)
    active = db.Column(db.Boolean, default=False)
    pass_hash = db.Column(db.String(64))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(120))
    prio = db.Column(db.Integer)

def create_app():
    app.register_blueprint(home_blueprint)
    app.register_blueprint(login_blueprint)
    return app