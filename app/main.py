# Operating system
import os
# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Flask Mail
from flask_mail import Mail, Message
# Import datetime
from datetime import datetime
# Classes
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
    user = User.check_user_exists(session["user"])
    groups = list(Group.get_all_groups())
    users = list(User.get_all_users())

    return render_template("homepage.html", page_title="Home", groups=groups,
                            users=users, user=user)


# Statements
@main.route("/statements")
def statements():
    return render_template("statements.html", page_title="Our statements")

# FAQs
@main.route("/faqs")
def faqs():
    return render_template("faqs.html", page_title="FAQs")


# Contact us
@main.route("/contact", methods=["GET", "POST"])
def contact():
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
    Renders template with all existing groups and events
    """
    user = User.get_user_id(session["user"])
    #print(user)
    groups = list(Group.get_all_groups())
    members = list(User.get_all_users())
    #print(members)

    ids = mongo.db.users.distinct("_id")
    print(ids)

    return render_template("all-groups-members.html", 
                            page_title="Browse all groups and members",
                            groups=groups, members=members, ids=ids)
