import os
if os.path.exists("env.py"):
    import env


class Config:
    """
    Set environment variables so app runs
    """
    # Flask Mail
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TSL = os.environ.get("MAIL_USE_TSL")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    # MongoDB
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
    MONGO_URI = os.environ.get("MONGO_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
