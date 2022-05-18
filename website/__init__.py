# purpose: to make the website folder a python package (which we can then import)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()        # set up database by creating database object
DB_NAME = "database.db"


def create_app():               # create Flask application
    app = Flask(__name__)       # initialize app
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'    # secure cookies and session data (random string for encryption)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'    # use SQLite 3 to create a file for our SQL alchemy database to be stored in (which is ultimately contained in the 'website' folder)
    db.init_app(app)

    from .views import views    # import our blueprints (from views.py and auth.py files)
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')   # register our blueprints 
    app.register_blueprint(auth, url_prefix='/')    # no url prefix, just a slash

    from .models import User, Note, Recommended

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # when the app is created, if not signed in, go to login pg
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))    # we look for primary key here (id)

    return app


def create_database(app):      # function that creates our db, using SQL alchemy URI above
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app) # we pass our app in here
        print('Created Database!')
