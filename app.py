# Operating system
import os
# Flask
from flask import (Flask, render_template, request, flash, url_for, redirect, session)
# Import app
from app import run


app = run()


# Set up port & IP environment variables
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)

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
#@app.route("/group/<group_id>")
#def group(group_id):

    #members = list(mongo.db.groups.find({"_id": {"$in": ["members"]}}))
  #  group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})

   # return render_template("group.html", page_title="{{ group.group_name }}",
     #                       members=members, group=group)