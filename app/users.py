# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Flask Paginate
from flask_paginate import Pagination, get_page_args
# Werkzeug security
from werkzeug.security import generate_password_hash, check_password_hash
# Regex
import re
# Import datetime
from datetime import datetime
# Classes
from app.classes.user import User
from app.classes.group import Group
from app import mongo


# User blueprint
users = Blueprint("users", __name__)


# Profile
@users.route("/get_profile", methods=["GET", "POST"])
def get_profile():
    """
    Renders the user's profile
    Gets user's email from MongoDB to check in session
    Get's user's id to generate 'user since' value
    """

    user = User.check_user_exists(session["user"].lower())
    user_id = User.get_user_id(session["user"].lower())

    groups_created = list(Group.find_groups_by_id(user["groups_created"]))
    groups_member = list(Group.find_groups_by_id(user["groups_member_of"]))

    following = list(User.find_users_in_array(user["following"]))
    followers = list(User.find_users_in_array(user["followers"]))

    if user:
        return render_template("profile.html", page_title="My profile", user=user,
                                user_id=user_id, groups_created=groups_created,
                                groups_member=groups_member, following=following,
                                followers=followers)


# Get other member profiles
@users.route("/member_profile/<user_id>")
def member_profile(user_id):
    """
    Gets the user id
    Get's member's groups and following
    """
    user = User.get_user_by_id(user_id)
    user_id = User.get_user_id(user["email"])

    groups_created = list(Group.find_groups_by_id(user["groups_created"]))
    groups_member = list(Group.find_groups_by_id(user["groups_member_of"]))

    following = list(User.find_users_in_array(user["following"]))
    followers = list(User.find_users_in_array(user["followers"]))

    return render_template("member.html", page_title="", 
                            user_id=user_id, user=user,
                            groups_member=groups_member,
                            groups_created=groups_created,
                            following=following, followers=followers)


# Follow other members
@users.route("/follow/<user_id>")
def follow(user_id):
    """
    Gets session user id
    Gets user id of member to be followed
    Adds member to 'following' list
    """
    user = User.get_user_id(session["user"])
    session_id = user
    print(session_id)

    member = User.get_user_by_id(user_id)["_id"]
    user_id = member
    print(user_id)

    if user:
        User.add_to_list(session_id, "following", user_id)
        User.add_to_list(user_id, "followers", session_id)

    return redirect(url_for('users.member_profile', user_id=user_id))


# Profile settings
@users.route("/settings/<user_id>", methods=["GET", "POST"])
def settings(user_id):
    """
    Gets user id and current email
    Renders settings page
    """
    user = User.get_user_by_id(user_id)
    email = User.get_user_by_id(user_id)["email"]

    return render_template("profile-settings.html", page_title="Profile settings", user=user, email=email)


# Change email
@users.route("/edit_email/<user_id>")
def edit_email():
    """
    Gets user id and current email in session
    Checks to see if new email and confirmation match
    If matches, updates new email to Mongo DB
    Sets new email in session cookie
    Redirects user to 'profile-settings.html'
    If disparities, flashes user to prompt re-attempt

    """
    user = User.get_user_by_id(user_id)
    email = User.get_user_by_id(user_id)["email"]

    if request.form.get("new-email") == request.form.get("confirm-email"):
        if request.method == "POST":

            updated_email = {"email": request.form.get("new-email")}
            new_email = request.form.get("new-email")

            try:
                User.add_to_db(user_id, updated_email)
                flash("Email updated successfully!")
                session["user"] = new_email
                return render_template("profile-settings.html", page_title="Profile settings",
                                user=user, email=new_email)
            except Exception as e:
                print(e)

    else:
        flash("Emails do not match! Try entering them again.")
        return render_template("profile-settings.html", page_title="Profile settings",
                                user=user, email=email)            


# Change password
@users.route("/edit_password/<user_id>", methods=["GET", "POST"])
def edit_password(user_id):
    """
    Gets user id
    Checks to see if new passowrd and current password match
    If match, updates password in DB
    If disparities, flashes message to prompt re-attempt
    Redirects user to 'profile-settings.html'
    """
    user = User.get_user_by_id(user_id)

    if request.form.get("new-password") == request.form.get("confirm-password"):
        if request.method == "POST":

            updated_password = {"password": generate_password_hash(request.form.get("new-password"))}
            new_password = request.form.get("new-password")

            try:
                User.add_to_db(user_id, updated_password)
                flash("Password updated successfully!")
                return render_template("profile-settings.html", page_title="Profile settings", user=user)
            except Exception as e:
                print(e)

    else:
        flash("Passwords do not match! Please try entering them again.")
        return render_template("profile-settings.html", page_title="Profile settings", user=user)


# Edit account
@users.route("/edit_account", methods=["GET", "POST"])
def edit_account():
    """
    Gets user id
    Gets user details from DB to display in form
    Update user info to the DB
    Redirect user to 'profile-settings.html'
    """
    user = User.get_user_by_id(user_id)

    first_name = User.get_user_by_id(user_id)["first_name"]
    last_name = User.get_user_by_id(user_id)["last_name"]

    if request.method == "POST":
        updated_names = { 
            "first_name": request.form.get("new-fname"),
            "last_name": request.form.get("new-lname")
        }

        new_fname = request.form.get("new-fname")
        new_lname = request.form.get("new-lname")

        try:
            Users.add_to_db(user_id, updated_names)
            flash("Account details successfully updated!")
            return render_template("profile-settings.html", page_title="Profile settings", user=user,
                                    first_name=new_fname,
                                    last_name=new_lname)
        except Exception as e:
            print(e)

    else:
        flash("Sorry, account could not be updated right now.")
        return render_template("profile-settings.html", page_title="Profile settings", user=user)


# Edit profile
@users.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    """
    Finds user's id
    Creates dictionary of user's info from form
    Updates user infomation in MongoDB
    Flashes message to notify user that update is successful
    Redirect user to 'profile.html'
    """
    user = User.get_user_by_id(user_id)

    if request.method == "POST":
        updated_info = {
            "user_city": request.form.get("city"),
            "user_location": request.form.get("country"),
            "nickname": request.form.get("nickname"),
            "user_interests": request.form.get("interests"),
            "user_project_1": request.form.get("link-1"),
            "user_project_2": request.form.get("link-2"),
            "user_project_3": request.form.get("link-3"),
            "user_biography": request.form.get("bio"),
            "profile_pic_url": request.form.get("profile-pic"),
            "user_banner_url": request.form.get("banner")
        }

        try:
            User.edit_user(user_id, updated_info)
            flash("Profile updated!")
            return redirect(url_for("users.get_profile", page_title="My profile", user=user))
        except Exception as e:
            print(e)

    return render_template("edit-profile.html", page_title="Edit profile", user=user) 


# Delete account
@users.route("/delete_account/<user_id>", methods=["GET", "POST"])
def delete_account(user_id):
    """
    Triggers confirmation modal
    Removes user from any groups
    Deletes groups associated with user
    Removes user from session cookie
    Removes user from MongoDB
    Flashes user to confirm account deletion
    Redicts user to 'sign-up.html'
    """

    # TO SORT
    
    # Get user
    #user = User.check_user_exists(session["user"])
    # Get user's groups
    #groups = mongo.db.groups.distinct("_id")
    #OR
    #groups_two = list(Group.find_groups_by_id(user["groups_created"]))
    # Get and delete user's groups
    #user = User.check_user_exists(session["user"])
    #user_groups = list(Group.find_groups_by_id(user["groups_created"]))
    #for group in user_groups:
    # Group.delete_group(group)
    #User.remove_from_list(user["_id"], "groups_member_of", group_id)
  
    session.pop("email", None)
    session.pop("user")
    User.delete_user(user_id)
    flash("We're sorry to see you go! Please do come back and join the adventure again soon.")
    return redirect(url_for("auth.sign_up"))