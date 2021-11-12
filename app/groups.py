# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
# Classes
from app.classes.user import User
from app.classes.group import Group
from app import mongo


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

        admin = Group.get_group(group_id)["group_admin"]
        admin_fname = User.get_user_by_id(admin)["first_name"]
        admin_lname = User.get_user_by_id(admin)["last_name"]

        return render_template("group.html", page_title="{{ group.group_name }}",
                                group=group, admin=admin, user=user,
                                admin_fname=admin_fname, admin_lname=admin_lname,
                                members_of=members_of, members=members)

# Edit group
@groups.route("/edit_group/<group_id>", methods=["GET", "POST"])
def edit_group(group_id):
    """
    Renders 'edit-group.html
    Gets group id
    Upon submission, adds updated info to a dictionary
    Updates MongoDB
    Redirects user to group page
    """

    group = Group.get_group(group_id)

    if request.method == "POST":
        updated_info = {
            "group_name": request.form.get("name"),
            "group_location": request.form.get("location"),
            "group_description": request.form.get("description"),
            "group_cover_img_url": request.form.get("banner")
        }

        try:
            Group.edit_group(group_id, updated_info)
            flash("Group infomation updated!")
            return redirect(url_for("groups.group_page", group_id=group_id))
        except Exception as e:
            print(e)

    return render_template("edit-group.html", group_id=group_id, group=group)

# Join group
@groups.route("/join_group/<group_id>", methods=["GET", "POST"])
def join_group(group_id):
    """
    Gets session user id
    Gets's group id
    Adds group to 'groups_member_of' in user collection
    Adds user to 'members' in group collection

    """
    user = User.get_user_id(session["user"])
    user_id = user

    group = Group.get_group(group_id)["_id"]
    group_id = group

    if user:
        User.add_to_list(user_id, "groups_member_of", group_id)
        Group.add_to_list(group_id, "members", user_id)

    return redirect(url_for('groups.group_page', group_id=group_id)) 

# Delete group
@groups.route("/delete_group/<group_id>")
def delete_group(group_id):
    """
    Triggers confirmation modal
    Gets group id, group admin and user
    Removes group from members' lists
    Removes group from admin's list
    Removes group from MongoDB
    Flashes user to confirm deletion
    Redirects user to their profile page
    """
    user = User.check_user_exists(session["user"])
    group = Group.get_group(group_id)
    admin = Group.get_group(group_id)["group_admin"]

    members = mongo.db.users.distinct("_id")
    for member in members:
        User.remove_from_list(member, "groups_member_of", group_id)

    User.remove_from_list(admin, "groups_created", group_id)
    Group.delete_group(group_id)

    flash("Group successfully deleted!")
    return redirect(url_for('users.get_profile', user_id=admin))