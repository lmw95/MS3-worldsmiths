from app import mongo
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId


class User():
    """
    Creates an instance of User
    """
    def __init__(self, first_name, last_name, email,
                password, user_member_since, nickname=None, 
                profile_pic_url=None, user_banner_url=None, user_city=None, 
                user_location=None, user_interests=None, user_biography=None,
                user_project_1=None, user_project_2=None, user_project_3=None,
                groups_member_of=None, groups_created=None, following=None,
                followers=None, _id=None):
        """
        Initialise User
        """
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.nickname = nickname if isinstance(nickname, str) else str("")
        self.profile_pic_url = profile_pic_url if isinstance(profile_pic_url, str) else str("/static/imgs/profile-avatar.png")
        self.user_banner_url = user_banner_url if isinstance(user_banner_url, str) else str("/static/icons/book.png")
        self.user_member_since = user_member_since
        self.user_city = user_city if isinstance(user_city, str) else str("")
        self.user_location = user_location if isinstance(user_location, str) else str("")
        self.user_interests = user_interests if isinstance(user_interests, str) else str("")
        self.user_biography = user_biography if isinstance(user_biography, str) else str("")
        self.user_project_1 = user_project_1 if isinstance(user_project_1, str) else str("")
        self.user_project_2 = user_project_2 if isinstance(user_project_2, str) else str("")
        self.user_project_3 = user_project_3 if isinstance(user_project_3, str) else str("")
        self.groups_member_of = groups_member_of if isinstance(groups_member_of, list) else []
        self.groups_created = groups_created if isinstance(groups_created, list) else []
        self.followers = followers if isinstance(followers, list) else []
        self.following = following if isinstance(following, list) else []

    
    # Gets all possible info about User
    def user_info(self):
        user_info = {
            "first_name": self.first_name.lower(),
            "last_name": self.last_name.lower(),
            "email": self.email.lower(),
            "password": self.password,
            "nickname": self.nickname,
            "profile_pic_url": self.profile_pic_url,
            "user_banner_url": self.user_banner_url,
            "user_member_since": self.user_member_since,
            "user_city": self.user_city.capitalize(),
            "user_location": self.user_location.upper(),
            "user_interests": self.user_interests,
            "user_biography": self.user_biography,
            "user_project_1": self.user_project_1,
            "user_project_2": self.user_project_2,
            "user_project_3": self.user_project_3,
            "groups_member_of": self.groups_member_of,
            "groups_created": self.groups_created,
            "followers": self.followers,
            "following": self.following
        }

        return user_info


    # Add a user to MongoDB
    def add_to_db(self):
        mongo.db.users.insert_one(self.user_info())

    
    # Finds a user's id using email
    @staticmethod
    def get_user_id(email):
        user_id = mongo.db.users.find_one({"email": email})["_id"]
        return user_id

    
    # Finds a user by their id
    @staticmethod
    def get_user_by_id(user_id):
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return user


    # Finds all users
    @staticmethod
    def get_all_users():
        users = list(mongo.db.users.find())
        return users


    # Finds items within an array in user collection
    @staticmethod
    def find_users_in_array(collection):
        all_users = mongo.db.users.find({"_id": {"$in": collection}})
        return all_users


    # Checks if user already exists
    @staticmethod
    def check_user_exists(email):
        existing_user = mongo.db.users.find_one({"email": email})
        return existing_user


    # Edit a user and updates DB
    @staticmethod
    def edit_user(user_id, user_info):
        mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                  {"$set": user_info})


    # Adds to an array/list in user
    @staticmethod
    def add_to_list(user_id, field, value):
        mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                  {"$push": {field: ObjectId(value)}})


    # Removes from array/list in user
    @staticmethod
    def remove_from_list(user_id, field, value):
        mongo.db.users.update_one({"_id": ObjectId(user_id)},
                                   {"$pull": {field: ObjectId(value)}})


    # Deletes a user from DB
    @staticmethod
    def delete_user(user_id):
        mongo.db.users.delete_one({"_id": ObjectId(user_id)})
