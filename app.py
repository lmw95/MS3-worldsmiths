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
