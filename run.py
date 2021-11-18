# Operating system
import os
# Flask
from flask import (Flask, render_template, request, flash, url_for, redirect, session)
from app import run_app
if os.path.exists("env.py"):
    import env


app = run_app()


# Environment settings
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
