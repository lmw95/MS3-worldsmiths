# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Classes
from app.classes.user import User
from app.classes.group import Group


# Groups blueprint
groups = Blueprint("groups", __name__)


# Create group
@groups.route("/create_group", methods=["GET", "POST"])
def create_group():
    """
    Get user in sessiond
    Renders 'create-group.html'
    Creates dictionary of new group info
    Creates new document in MongoDB
    Adds ObjectId of group to user collection
    """

    user = User.check_user_exists(session["user"])

    if request.method == "POST":
        new = Group(
            group_name=request.form.get("group-name"),
            group_location=request.form.get("group-location"),
            group_description=request.form.get("group-description"),
            group_cover_img_url=request.form.get("group-banner"),
            group_admin=user["_id"])

        try:
            new_created = new.add_to_db()
            User.add_to_list(user["_id"], "groups_created", new_created.inserted_id)
            flash("Group created! See Groups section on your profile.")
            return redirect(url_for('users.get_profile'))
        except Exception as e:
            print(e)
    
    return render_template("create-group.html", page_title="Create a group",
                            user=user)


# Group page
@groups.route("/group_page/<group_id>")
def group_page(group_id):
    """
    Gets group id
    Renders group page with group info
    """

    user = User.check_user_exists(session["user"])["_id"]

    if user:
        group = Group.get_group(group_id)

        members_of = User.get_user_by_id(user)["groups_member_of"]
        members = list(User.find_users_in_array(group["members"]))

        print(members)

        admin = Group.get_group(group_id)["group_admin"]
        admin_fname = User.get_user_by_id(admin)["first_name"]
        admin_lname = User.get_user_by_id(admin)["last_name"]

        return render_template("group.html", page_title="{{ group.group_name }}",
                                group=group, admin=admin, user=user,
                                admin_fname=admin_fname, admin_lname=admin_lname,
                                members_of=members_of, members=members)
