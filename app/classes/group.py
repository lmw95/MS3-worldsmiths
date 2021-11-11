from flask import Flask
from bson.objectid import ObjectId
from app import mongo


class Group():
    """
    Create an instance of Group
    """
    def __init__(self, group_name, group_cover_img_url,
                group_admin, group_location,
                group_description, members=None, _id=None):

        """
        Initialise Group
        """
        self._id = _id
        self.group_name = group_name
        self.group_cover_img_url = group_cover_img_url
        self.group_admin = group_admin
        self.group_location = group_location
        self.group_description = group_description
        self.members = members if isinstance(members, list) else []


    # Gets all possible info about Group
    def all_group_info(self):
        group_info = {
            "group_name": self.group_name,
            "group_cover_img_url": self.group_cover_img_url,
            "group_admin": self.group_admin,
            "group_location": self.group_location,
            "group_description": self.group_description,
            "members": self.members
        }

        return group_info


    # Adds a group to MongoDB and get group_id
    def add_to_db(self):
        group_id = mongo.db.groups.insert_one(self.all_group_info())
        return group_id


    # Finds a group by ID
    @staticmethod
    def get_group(group_id):
        group = mongo.db.groups.find_one({"_id": ObjectId(group_id)})
        return group

    
    # Finds all groups 
    @staticmethod
    def get_all_groups():
        groups = list(mongo.db.groups.find())
        return groups


    # Finds groups by collection in array/list
    @staticmethod
    def find_groups_by_id(collection):
        group_list = mongo.db.groups.find({"_id": {"$in": collection}})
        return group_list
    
    # Adds to array/list in group
    @staticmethod
    def add_to_list(group_id, field, value):
        mongo.db.groups.update_one({"_id": ObjectId(group_id)},
                                   {"$push": {field: ObjectId(value)}})


    # Removes from array/list in group
    @staticmethod
    def remove_from_list(group_id, field, value):
        mongo.db.groups.remove_one({"_id": ObjectId(group_id)},
                                   {"$pull": {field: ObjectId(value)}})

    # Delete group
    @staticmethod
    def delete_group(group_id):
        mongo.db.groups.delete_one({"_id": ObjectId(group_id)})

