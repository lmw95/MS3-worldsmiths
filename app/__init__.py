from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from app.settings import Settings


mongo = PyMongo()


mail = Mail()


def run_app(default_config=Settings):
    """
    Creates instance of app
    Imports Blueprints for rendering
    """
    # Create instance of app
    app = Flask(__name__)
    app.config.from_object(default_config)
    mongo.init_app(app)
    mail.init_app(app)

    # Import Blueprints
    from app.users import users
    from app.groups import groups
    from app.main import main

    app.register_blueprint(users)
    app.register_blueprint(groups)
    app.register_blueprint(main)

    return app 
