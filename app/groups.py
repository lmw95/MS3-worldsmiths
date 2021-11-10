# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Classes
from app.classes.user import User
from app.classes.group import Group


# Groups blueprint
groups = Blueprint("groups", __name__)