# Operating system
import os
# Flask
from flask import (Flask, render_template, request, flash, url_for, redirect, session)
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from app.users import users
from app.groups import groups
from app.main import main

if os.path.exists("env.py"):
    import env


# Create instance of app
app = Flask(__name__)


# Flask mail settings
mail_settings = {
    "MAIL_SERVER": os.environ.get("MAIL_SERVER"),
    "MAIL_PORT": os.environ.get("MAIL_PORT"),
    "MAIL_USE_SSL": os.environ.get("MAIL_USE_SSL"),
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("SENDGRID_API_KEY"),
    "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_DEFAULT_SENDER")
}


# Configure mail settings
app.config.update(mail_settings)


# Create instance of mail
mail = Mail(app)


# Mongo variables
mongo_settings = {
    "MONGO_DBNAME": os.environ.get("MONGO_DBNAME"),
    "MONGO_URI": os.environ.get("MONGO_URI")
}


# Configure PyMongo settings
app.config.update(mongo_settings)


# Create instance of mongo
mongo = PyMongo(app)


# Other variables
SECRET_KEY = os.environ.get("SECRET_KEY")


# Render blueprints
app.register_blueprint(users)
app.register_blueprint(groups)
app.register_blueprint(main)


# Environment settings
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
