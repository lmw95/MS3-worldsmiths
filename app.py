import os
from flask import (Flask, render_template)
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

# Create an instance of Flask
app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Create an instance of PyMongo
mongo = PyMongo(app)

# Test function to render data.html test page
@app.route("/")
@app.route("/get_groups")
def get_groups():
    groups = mongo.db.groups.find()
    return render_template("data.html", groups=groups)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)