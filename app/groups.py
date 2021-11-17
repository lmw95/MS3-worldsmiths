# Flask
from flask import (Flask, render_template, request,
                   flash, url_for, redirect, session, Blueprint)
from datetime import datetime
# Classes
from bson.objectid import ObjectId
from app.classes.user import User
from app.classes.group import Group
from app.classes.comment import Comment
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
    check_user = User.check_user_exists(session["user"])
    print(check_user)
    user_following = User.check_user_exists(session["user"].lower())

    if user:
        group = Group.get_group(group_id)

        # Gets all users in db
        users = list(User.get_all_users())

        # Gets members of the group
        members_of = User.get_user_by_id(user)["groups_member_of"]
        members = list(User.find_users_in_array(group["members"]))

        following = list(User.find_users_in_array(user_following["following"]))

        comments = list(Comment.get_all_comments(group_id))

        admin = Group.get_group(group_id)["group_admin"]
        admin_fname = User.get_user_by_id(admin)["first_name"]
        admin_lname = User.get_user_by_id(admin)["last_name"]

        return render_template("group.html", page_title="{{ group.group_name }}",
                                group=group, admin=admin, user=user,
                                admin_fname=admin_fname, admin_lname=admin_lname,
                                members_of=members_of, members=members, comments=comments,
                                users=users, following=following, check_user=check_user)

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
        flash("You are now a member")

    return redirect(url_for('groups.group_page', group_id=group_id))


# Leave group
@groups.route("/leave_group/<group_id>")
def leave_group(group_id):
    """
    Gets session user id
    Gets's group id
    Removes group to 'groups_member_of' in user collection
    Removes user to 'members' in group collection
    """

    user = User.get_user_id(session["user"])
    user_id = user

    group = Group.get_group(group_id)["_id"]
    group_id = group

    if user:
        try:
            User.remove_from_list(user_id, "groups_member_of", group_id)
            Group.remove_from_list(group_id, "members", user_id)
            flash("You have left the group")
        except Exception as e:
            print(e)

    return redirect(url_for('groups.group_page', group_id=group_id))


# Add comment
@groups.route("/add_comment/<group_id>", methods=["GET", "POST"])
def add_comment(group_id):
    """
    Gets group id
    Gets poster id (user in session)
    Adds comment to Mongo DB
    Renders comment on group page
    """
    if request.method == "POST":
        user = User.check_user_exists(session["user"])
        group = Group.get_group(group_id)["_id"]

        # https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
        time = datetime.now().strftime("%H:%M")
        date = datetime.now().strftime("%d %b %Y")

        new_comment = Comment(comment=request.form.get("comment"),
                            commenter=user["_id"],
                            group_id=ObjectId(group_id),
                            time_posted=time,
                            date_posted=date, 
                            reply=False,
                            reply_to=None,
                            reply_user=None)

        try:
            new_comment.add_to_db()
            flash("Comment added!")
            return redirect(url_for('groups.group_page', group_id=group_id))
        except Exception as e:
            print(e)

    return redirect(url_for('groups.group_page', group_id=group_id))


# Delete comment
@groups.route("/delete_comment/<group_id>/<comment_id>", methods=["GET", "POST"])
def delete_comment(group_id, comment_id):
    """
    Gets group id
    Gets poster id (user in session)
    Adds comment to Mongo DB
    Renders comment on group page
    """
    if request.method == "POST":
        
        group = Group.get_group(group_id)["_id"]
        print(group)

        comment = Comment.get_comment(comment_id)
        print(comment_id)

        Comment.delete_comment(comment_id)
        flash("Comment deleted")

    return redirect(url_for('groups.group_page', group_id=group_id))
    

# Reply to a comment
@groups.route("/reply/<group_id>/<comment_id>", methods=["GET", "POST"])
def reply(group_id, comment_id):
    """
    Gets group id
    Gets poster id (user in session)
    Adds comment to Mongo DB
    Renders comment on group page
    """

    if request.method == "POST":
        user = User.check_user_exists(session["user"])
        group = Group.get_group(group_id)["_id"]

        comment = Comment.get_comment(comment_id)["_id"]
        print(comment)
        commenter = Comment.get_comment(comment_id)["commenter"]
        print(commenter)

        # https://thispointer.com/python-how-to-get-current-date-and-time-or-timestamp/
        time = datetime.now().strftime("%H:%M")
        date = datetime.now().strftime("%d %b %Y")

        new_reply = Comment(comment=request.form.get("reply"),
                                commenter=user["_id"],
                                group_id=ObjectId(group_id),
                                time_posted=time,
                                date_posted=date,
                                reply=True,
                                reply_to=ObjectId(comment_id),
                                reply_user=ObjectId(commenter))

        try:
            new_reply.add_to_db()
            flash("Reply added!")
            return redirect(url_for('groups.group_page', group_id=group_id))
        except Exception as e:
            print(e)

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

    User.remove_from_list(user["_id"], "group_member_of", group_id)
    User.remove_from_list(admin, "groups_created", group_id)
    Group.delete_group(group_id)

    flash("Group successfully deleted!")
    return redirect(url_for('users.get_profile', user_id=admin))