# Import operating system
import os
# Import Flask
from flask import (Flask, render_template, request, flash, url_for, redirect)
# Import Flask-Mail 
from flask_mail import Mail, Message
# Import PyMongo
from flask_pymongo import PyMongo
# Import Werkzeug security helpers
from werkzeug.security import generate_password_hash, check_password_hash
# Import Regex
import re
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


# Render the contact form template and implement Flask Mail - https://pythonbasics.org/flask-mail/
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

                msg = Message(recipients=[recipient], body=message, subject=subject)

                conn.send(msg)

            flash("Thanks {}, we have recieved your message".format(request.form.get("full-name")))
            return redirect(url_for('contact'))

    return render_template("contact.html", page_title="Contact us")


# Render the sign up page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # Check if user exists
        existing_user = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        register_user = {
            "first_name": request.form.get("fname").lower(),
            "last_name": request.form.get("lname").lower(),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        
        if existing_user:
            flash("This email is already linked to an account. Please try a different one or log-in.")
            return redirect(url_for("sign_up"))
        else:
            try:
                mongo.db.users.insert_one(register_user)
                flash("Welcome aboard! You may now log-in and start exploring.")
            except Exception as e:
                print(e)

    return render_template("sign-up.html", page_title="Sign up")


# Set up port & IP environment variables
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)