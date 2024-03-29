import os
from . import mail
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
from flask_mail import Message
from datetime import datetime
from flask_paginate import Pagination, get_page_args
from app.classes.user import User
from app.classes.group import Group
from app import mongo


# Main blueprint
main = Blueprint("main", __name__)


# Homepage
@main.route("/")
@main.route("/homepage")
def homepage():
    """
    Gets all groups
    Render homepage.html template
    """
    groups = list(Group.get_all_groups())
    users = list(User.get_all_users())

    return render_template("homepage.html", page_title="Home", groups=groups,
                           users=users)


# Search through all events and memembers
@main.route("/search", methods=["GET", "POST"])
def search():
    """
    Renders template for 'all-members-groups.html"
    Displays query results
    Uses user info to render correct functions and displays
    """
    if session:
        user = User.check_user_exists(session["user"])
    else:
        user = None

    if user:
        user_following = User.check_user_exists(session["user"].lower())
        following = list(User.find_users_in_array(user_following["following"]))
    else:
        user_following = []
        following = []

    members = list(User.get_all_users())
    groups = list(Group.get_all_groups())

    # User query results
    user_query = request.form.get("finder")
    group_results = list(Group.find_groups_by_query(user_query))
    member_results = list(User.find_users_by_query(user_query))

    return render_template("all-groups-members.html",
                           page_title="Search", user=user,
                           user_query=user_query, group_results=group_results,
                           member_results=member_results,
                           groups=groups, members=members,
                           following=following, search=True)


# Contact us
@main.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Gets info from contact form submission
    Sends confirmation email to sender via Flask Mail
    Flashes confirmation
    Redirects user to 'contact.html'
    """
    if request.method == "POST":
        sender_name = request.form.get('full-name')
        sender_email = request.form.get('email')
        sender_reason = request.form.get('reason')
        sender_message = request.form.get('message')
        admin_email = os.environ.get('MAIL_DEFAULT_SENDER')
        recipients = [sender_email, admin_email]

        # Sending bulk emails with Flask - https://pythonhosted.org/Flask-Mail/
        with mail.connect() as conn:
            for recipient in recipients:
                if recipient == admin_email:
                    subject = f"New query from: {sender_name}, {sender_email}"
                    message = f"Reason: {sender_reason} \nMessage: {sender_message}"

                elif recipient == sender_email:
                    subject = "Thank your for your message..."
                    message = f"Thank you, {sender_name}! \nWe have received your message will get back to you within 2-3 working days."

            msg = Message(
                recipients=[recipient], body=message, subject=subject)

            conn.send(msg)

        flash("Thanks {}, we have recieved your message".format(
            request.form.get("full-name")))
        return redirect(url_for('main.contact'))

    return render_template("contact.html", page_title="Contact us")


# Browse all events/groups page
@main.route("/browse_all")
def browse_all():
    """
    Checks to see if user is following members
    Checks to see if user is part of any groups
    Renders template with all existing groups and events ready for searching
    """
    groups = list(Group.get_all_groups())
    members = list(User.get_all_users())

    user = User.check_user_exists(session["user"])

    user_following = User.check_user_exists(session["user"].lower())
    following = list(User.find_users_in_array(user_following["following"]))

    return render_template("all-groups-members.html",
                           page_title="Browse all groups and members",
                           following=following,
                           groups=groups, members=members)
