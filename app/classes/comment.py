from app import mongo
from bson.objectid import ObjectId

class Comment():
    """
    Creates instance of a comment
    """
    def __init__(self, comment, commenter,
                time_date_posted, group_id, _id=None):

        self._id = _id
        self.comment = comment
        self.commenter = commenter
        self.time_date_posted = time_date_posted
        self.group_id = group_id

        
    def comment_info(self):
        comment_info = {
            "comment": self.comment,
            "commenter": self.commenter,
            "time_date_posted": self.time_date_posted,
            "group_id": self.group_id,
        }

        return comment_info


    # Add comment to db
    # Generate id for commnent
    def add_to_db(self):
        comment_id = mongo.db.comments.insert_one(self.comment_info())
        return comment_id


    # Update comment/reply
    @staticmethod
    def update_comment(comment_id, comment_info):
        mongo.db.comments.update_one({"_id": ObjectId(comment_id)},
                                     {"$set": comment_info})


    # Gets one comment by ID
    @staticmethod
    def get_comment(comment_id):
        comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
        return comment

    
    # Gets all comments in a group
    @staticmethod
    def get_all_comments(group_id):
        all_comments = list(mongo.db.comments.find(
                                 {"group_id": ObjectId(group_id)}).sort("time_date_posted", -1))
        return all_comments


    # Delete comment
    @staticmethod
    def delete_comment(comment_id):
        mongo.db.comments.delete_one({"_id": ObjectId(comment_id)})
