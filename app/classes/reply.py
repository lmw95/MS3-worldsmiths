from app import mongo
from bson.objectid import ObjectId

class Reply():
    """
    Creates instance of a reply
    """
    def __init__(self, reply, reply_from,
                time_date_posted,
                group_id, _id=None):

        self._id = _id
        self.reply = reply
        self.reply_from = reply_from
        self.time_date_posted = time_date_posted
        self.group_id = group_id

        
    def reply_info(self):
        reply_info = {
            "reply": self.reply,
            "reply_from": self.reply_from,
            "time_date_posted": self.time_date_posted,
            "group_id": self.group_id,
        }

        return reply_info


    # Add reply to db
    # Generate id for reply
    def add_to_db(self):
        reply_id = mongo.db.replies.insert_one(self.reply_info())
        return reply_id


    # Update reply
    @staticmethod
    def update_reply(reply_id, reply_info):
        mongo.db.replies.update_one({"_id": ObjectId(reply_id)},
                                     {"$set": reply_info})

    
    # Gets all replies in a group
    @staticmethod
    def get_all_replies(group_id):
        all_replies = list(mongo.db.replies.find(
                                 {"group_id": ObjectId(group_id)}).sort("time_date_posted", -1))
        return all_replies
        

    # Delete reply
    @staticmethod
    def delete_reply(reply_id):
        mongo.db.replies.delete_one({"_id": ObjectId(reply_id)})

    