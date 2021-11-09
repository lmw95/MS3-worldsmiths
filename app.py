# Import operating system
import os
# Import Flask
from flask import (Flask, render_template, request, flash, url_for, redirect, session)
# Import Flask-Mail
from flask_mail import Mail, Message
# Import PyMongo
from flask_pymongo import PyMongo
# Import Werkzeug security helpers
from werkzeug.security import generate_password_hash, check_password_hash
# Import objectId
from bson.objectid import ObjectId
# Import Regex
import re
# Import datetime
from datetime import datetime
# Set up environment variables
if os.path.exists("env.py"):
    import env


# Create an instance of Flask
app = Flask(__name__)


# Set up Mail configuration settings
mail_settings = {
    "MAIL_SERVER": os.environ.get("MAIL_SERVER"),
    "MAIL_PORT": os.environ.get("MAIL_PORT"),
    "MAIL_USE_SSL": os.environ.get("MAIL_USE_SSL"),
    "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
    "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
    "SECURITY_EMAIL_SENDER": os.environ.get("SECURITY_EMAIL_SENDER"),
    "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_DEFAULT_SENDER")
}

app.config.update(mail_settings)


# Create an instance of Flask-Mail
mail = Mail(app)


# Configure MongoDB variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


# Create an instance of PyMongo
mongo = PyMongo(app)


# Test function to render data.html test page
@app.route("/")
@app.route("/test_groups")
def test_groups():
    groups = mongo.db.groups.find()
    return render_template("test.html", groups=groups)


# Render the home page
@app.route("/homepage")
def homepage():
    return render_template("homepage.html", page_title="Home")

# Render the privacy and accessibility statement template
@app.route("/statements")
def statements():
    return render_template("statements.html", page_title="Our statements")


# Render the frequently asked questions template
@app.route("/faqs")
def faqs():
    return render_template("faqs.html", page_title="FAQs")


# Render the contact form template and implement Flask Mail
# https://pythonbasics.org/flask-mail/
@app.route("/contact", methods=["GET", "POST"])
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
            return redirect(url_for('contact'))

    return render_template("contact.html", page_title="Contact us")


# Render the sign up page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # Check if user exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        # Get user sign up date
        # https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
        reg_date = datetime.now().strftime("%d %b %Y")

        # User data to be added to DB
        register_user = {
            "first_name": request.form.get("fname").lower(),
            "last_name": request.form.get("lname").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "nickname": "",
            "profile_pic_url": "/static/imgs/profile-avatar.png",
            "user_banner_url": "/static/icons/book.png",
            "user_member_since": reg_date,
            "user_city": "",
            "user_location": "",
            "user_interests": "",
            "user_biography": "",
            "user_project_1": "",
            "user_project_2": "",
            "user_project_3": "",
            "events_attending": [],
            "events_organised": [],
            "groups_member_of": [],
            "groups_created": [],
            "following": [],
            "followers": ""
        }

        if existing_user:
            flash("This email is already linked to an account. Please try a different one or log-in.")
            return redirect(url_for("sign_up"))
        else:
            try:
                mongo.db.users.insert_one(register_user)
                flash("Registration successful, welcome aboard! You can now log in.")
                return redirect(url_for("log_in"))
            except Exception as e:
                print(e)

    return render_template("sign-up.html", page_title="Sign up")


# Render the log in page
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        # Check if user email exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("email").lower()
                return redirect(url_for("welcome", first_name=session["user"]))
            else:
                flash("Email and/or password incorrect")
                return redirect(url_for("log_in"))
        else:
            flash("No account exists with this email")
            return redirect(url_for("log_in"))

    return render_template("log-in.html", page_title="Log in")


# Render 'reset password' modal
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    flash("Password reset link sent! Please check your inbox (and junk!)")
    return render_template("log-in.html", page_title="Log in")


# Render the welcome page
@app.route("/welcome/<first_name>", methods=["GET", "POST"])
def welcome(first_name):
    # Get user's first name from the DB
    first_name = mongo.db.users.find_one(
        {"email": session["user"]})["first_name"]

    if session["user"]:
        return render_template(
            "welcome.html", page_title="Welcome back", first_name=first_name)

    return redirect(url_for("log_in"))


# Render the user profile
@app.route("/get_profile", methods=["GET", "POST"])
def get_profile():

    # Get user id to generate 'member since'
    user_id = mongo.db.users.find_one(
        {"email": session["user"]})["_id"]

    # Check to see user in session's email
    user = mongo.db.users.find_one(
        {"email": session["user"]})["email"].lower()
        
    # Get user details to populate profile
    first_name = mongo.db.users.find_one(
        {"email": session["user"]})["first_name"]
    last_name = mongo.db.users.find_one(
        {"email": session["user"]})["last_name"]
    email = mongo.db.users.find_one(
        {"email": session["user"]})["email"]
    city = mongo.db.users.find_one({
        "email": session["user"]})["user_city"]
    location = mongo.db.users.find_one({
        "email": session["user"]})["user_location"]
    interests = mongo.db.users.find_one({
        "email": session["user"]})["user_interests"]
    project_1 = mongo.db.users.find_one({
        "email": session["user"]})["user_project_1"]
    project_2 = mongo.db.users.find_one({
        "email": session["user"]})["user_project_2"]
    project_3 = mongo.db.users.find_one({
        "email": session["user"]})["user_project_3"]
    bio = mongo.db.users.find_one({
        "email": session["user"]})["user_biography"]
    profile_pic = mongo.db.users.find_one({
        "email": session["user"]})["profile_pic_url"]
    banner = mongo.db.users.find_one({
        "email": session["user"]})["user_banner_url"]
    nickname = mongo.db.users.find_one({
        "email": session["user"]})["nickname"]

    # Render page if user is in session
    if session["user"]:
        return render_template("profile.html", page_title="My profile", 
                                user_id=user_id, user=user, 
                                first_name=first_name,
                                last_name=last_name, email=email,
                                city=city, location=location,
                                interests=interests,
                                project_1=project_1,
                                project_2=project_2,
                                project_3=project_3, bio=bio,
                                profile_pic=profile_pic, banner=banner,
                                nickname=nickname)


# Render settings page
@app.route("/settings/<user_id>", methods=["GET", "POST"])
def settings(user_id):

    # Get user ID
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Get user email to display 'current email'
    email = mongo.db.users.find_one({"_id": ObjectId(user_id)})["email"]

    return render_template("profile-settings.html", page_title="Profile settings", user=user, email=email)


# Render the 'change email' form
@app.route("/edit_email/<user_id>", methods=["GET", "POST"])
def edit_email(user_id):

    # Get user ID
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Get user email to update Flask session
    email = mongo.db.users.find_one({"_id": ObjectId(user_id)})["email"]

    # Check to see if new email and confirmation match
    if request.form.get("new-email") == request.form.get("confirm-email"):
        if request.method == "POST":

            # Update new email to DB
            update_email = {"$set": {"email": request.form.get("new-email")}}

            # Set new email in Flask session
            new_email = request.form.get("new-email")

            try:
                mongo.db.users.update({"_id": ObjectId(user_id)}, update_email)
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


# Render the change password form
@app.route("/edit_password/<user_id>", methods=["GET", "POST"])
def edit_password(user_id):

    # Get user ID
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Check to see if password input matches
    if request.form.get("new-password") == request.form.get("confirm-password"):
        # Check to see if password matches confirmation
        if request.method == "POST":

            # Update new password to DB
            update_password = {"$set": {"password": generate_password_hash(request.form.get("new-password"))}}

            # Get new password for settings page
            new_password = request.form.get("new-password")

            try:
                mongo.db.users.update({"_id": ObjectId(user_id)}, update_password)
                flash("Password successfully updated!")
                return render_template("profile-settings.html", page_title="Profile settings", user=user)
            except Exception as e:
                print(e)

    else:
        flash("Passwords do not match! Please try entering them again.")
        return render_template("profile-settings.html", page_title="Profile settings", user=user)


# Render the 'delete account' form
@app.route("/delete_account/<user_id>")
def delete_account(user_id):

    # Remove email from session cookie
    session.pop("email", None)
    session.pop("user")

    # Remove user from DB
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})

    flash("We're sorry to see you go! Please do come back and join the adventure again soon.")
    return redirect(url_for("sign_up"))


# Render 'edit account' form
@app.route("/edit_account/<user_id>", methods=["POST", "GET"])
def edit_account(user_id):

    # Get user ID
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    # Get user details to display in form
    first_name = mongo.db.users.find_one({"_id": ObjectId(user_id)})["first_name"]
    last_name = mongo.db.users.find_one({"_id": ObjectId(user_id)})["last_name"]

    if request.method == "POST":
        update_names = {"$set": {
            "first_name": request.form.get("new-fname"),
            "last_name": request.form.get("new-lname")
        }}

        new_first_name = request.form.get("new-fname")
        new_last_name = request.form.get("new-lname")

        try: 
            mongo.db.users.update({"_id": ObjectId(user_id)}, update_names)
            flash("Account details successfully updated!")
            return render_template("profile-settings.html", page_title="Profile settings", user=user,
                                    first_name=new_first_name,
                                    last_name=new_last_name)
        except Exception as e:
            print(e)
    else:
        flash("Sorry, account could not be updated right now.")
        return render_template("profile-settings.html", page_title="Profile settings", user=user)


# Render the edit profile page
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):

    # Get user ID
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if request.method == "POST":

        # Create details dict to be added to DB
        user_info = {"$set": {
            "user_city": request.form.get("city"),
            "user_location": request.form.get("country"),
            "nickname": request.form.get("nickname"),
            "user_interests": request.form.get("interests"),
            "user_project_1": request.form.get("link-1"),
            "user_project_2": request.form.get("link-2"),
            "user_project_3": request.form.get("link-3"),
            "user_biography": request.form.get("bio"),
            "profile_pic_url": request.form.get("profile_pic"),
            "user_banner_url": request.form.get("banner")
        }
        }

        try:
            mongo.db.users.update({"_id": ObjectId(user_id)}, user_info)
            flash("Profile updated!")
            return redirect(url_for("get_profile", page_title="My profile", user=user))
        except Exception as e:
            print(e)

    return render_template("edit-profile.html", page_title="Edit profile", user=user)


# Browse all events page
@app.route("/all_events_groups")
def all_events_groups():

    events = list(mongo.db.events.find())
    event_type = list(mongo.db.event_type.find())
    groups = list(mongo.db.groups.find())
    group_type = list(mongo.db.group_type.find())
    users = list(mongo.db.users.find())

    return render_template("all-events-groups.html", 
                            page_title="Browse all events and groups",
                            events=events, event_type=event_type,
                            groups=groups, group_type=group_type, users=users)


# Render the create group page
#@app.route("/create_group", methods=["GET", "POST"])
#def create_group():

#    user = mongo.db.users.find_one({"email": session["user"]})["email"]

#    new_group = {
#        "group_name": request.form.get("group-name"),
#        "group_location": request.form.get("group-location"),
#        "group_description": request.form.get("group-description"),
#        "group_cover_img_url": request.form.get("group-banner"),
#        "group_admin": mongo.db.users.find_one({"email": session["user"]})["_id"]
#    }

#    if request.method == "POST":
#        mongo.db.groups.insert_one(new_group)
#        return render_template("group.html", page_title="{{ group.group_name }}", group=group)

#    return render_template("create-group.html", page_title="Create a group",
#                            user=user)


# Render group page
@app.route("/group/<group_id>")
def group(group_id):

    members = list(mongo.db.groups.find({"_id": {"$in": ["members"]}}))
    group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})

    return render_template("group.html", page_title="{{ group.group_name }}",
                            members=members, group=group)


# Render the logout function
@app.route("/log_out")
def log_out():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("log_in"))


# Set up port & IP environment variables
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
