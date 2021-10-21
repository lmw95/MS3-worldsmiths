# Import operating system
import os
# Import Flask
from flask import (Flask, render_template)
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

@app.route("/statements")
def statements():
    return render_template("statements.html", page_title="Our statements")

@app.route("/faqs")
def faqs():
    return render_template("faqs.html", page_title="FAQs")

@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact us")

# Set up port & IP environment variables
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)