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
            "profile_pic_url": "",
            "user_banner_url": "",
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
                                project_3=project_3, bio=bio)


# Render the settings page
@app.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("settings.html", page_title="Settings")


# Render the edit profile page
@app.route("/edit_profile/<user_id>", methods=["GET", "POST"])
def edit_profile(user_id):

    if request.method == "POST":

        user_info = {"$set": {
            "user_city": request.form.get("city"),
            "user_location": request.form.get("country"),
            "nickname": request.form.get("nickname"),
            "user_interests": request.form.get("interests"),
            "user_project_1": request.form.get("link-1"),
            "user_project_2": request.form.get("link-2"),
            "user_project_3": request.form.get("link-3"),
            "user_biography": request.form.get("bio")
        }
        }

        try:
            mongo.db.users.update({"_id": ObjectId(user_id)}, user_info)
            flash("Information updated")
            return redirect(url_for("get_profile", page_title="My profile", user=user))
        except Exception as e:
            print(e)

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("edit_profile.html", page_title="Edit profile", user=user)


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
