# Import operating system
import os
# Import Flask
from flask import (Flask, render_template, request, flash)
# Import PyMongo
from flask_pymongo import PyMongo
# Set up environment variables
if os.path.exists("env.py"):
    import env


# Create an instance of Flask
app = Flask(__name__)


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


#Render the frequently asked questions template
@app.route("/faqs")
def faqs():
    return render_template("faqs.html", page_title="FAQs")


# Render the contact form template and implement Flask Mail - https://pythonbasics.org/flask-mail/
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thanks {}, we have recieved your message".format(
        request.form.get("full-name")))
    return render_template("contact.html", page_title="Contact us")


# Render the sign up page
@app.route("/sign_up")
def sign_up():
    return render_template("sign-up.html", page_title="Sign up")


# Set up port & IP environment variables
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)