# Operating system
import os
# Flask Mail
from flask_mail import Mail, Message
# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Werkzeug Security
from werkzeug.security import generate_password_hash, check_password_hash
# Regex
import re
# ObjectId
from bson.objectid import ObjectId
# Datetime
from datetime import datetime
# Classes
from app.classes.user import User
from app.classes.group import Group


# Auth blueprint
auth = Blueprint("auth", __name__)


# Sign-up
@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """
    Check if user exists by email
    If user exists, flash message prompting user to login or try again
    If user does exist, creates dictionary of user info taken from form
    Gets registration date
    Checks if data is valid
    Adds data to MongoDB
    Redirect user to 'log-in.html' 
    """
    if request.method == "POST":
        existing_user = User.check_user_exists(
            request.form.get("email").lower()
        )

        # https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
        reg_date = datetime.now().strftime("%d %b %Y")

        new = User(first_name=request.form.get("fname").lower(),
                    last_name=request.form.get("lname").lower(),
                    email=request.form.get("email").lower(),
                    password=request.form.get("password"),
                    user_member_since=reg_date)

        if existing_user:
            flash("This email is already linked to an account. Please try a different one or log-in.")
            return redirect(url_for("auth.sign_up"))
        else:
            try:
                new.add_to_db()
                flash("Registration successful, welcome aboard! You can now log in.")
                return redirect(url_for("auth.log_in"))
            except Exception as e:
                print(e)
    
    return render_template("sign-up.html", page_title="Sign up")


# Log in
@auth.route("/log_in", methods=["GET", "POST"])
def log_in():
    """
    Check if user exists by email
    Check if password is valid
    If no email exists, prompt user to sign up or use different email
    If email and/or passworc are incorrect, flash message to prompt re-attempt
    If email and password match, creates 'session cookie' using user email
    Redirects user to 'welcome.html' with user's first name
    """
    if request.method == "POST":
        existing_user = User.check_user_exists(
            request.form.get("email").lower()
        )

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email").lower()
                return redirect(url_for("auth.welcome", first_name=session["user"]))
            else:
                flash("Email and/or password incorrect, please try again")
                return redirect(url_for("auth.log_in"))

    return render_template("log-in.html", page_title="Log in")


# Welcome page
@auth.route("/welcome/<first_name>", methods=["GET", "POST"])
def welcome(first_name):
    """
    Checks in session user's email
    Gets user's first name from DB using email
    Displays user's first name in heading
    """

    first_name = User.check_user_exists(session["user"])["first_name"]

    if session["user"]:
        return render_template(
            "welcome.html", page_title="Welcome back", first_name=first_name)


# Reset password modal
@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    """
    Dummy password reset
    Submits form but does not send or retrieve any data
    Flashes message to user that password link has been sent to email
    """
    flash("Password reset link sent! Please check your inbox (and junk!)")
    return render_template("log-in.html", page_title="Log in")


# Log-out
@auth.route("/log_out")
def log_out():
    """
    Removes user from session cookies
    Redirects user to 'log-in.html'
    Flashses message to user to signify successful logout
    """
    session.pop("user")
    flash("You have been logged out. Come back soon!")
    return redirect(url_for("auth.log_in"))

