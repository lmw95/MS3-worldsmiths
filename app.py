# Operating system
import os
# Flask
from flask import (Flask, render_template, request, flash, url_for, redirect, session)
from app import run_app
if os.path.exists("env.py"):
    import env


app = run_app()


# Error handling
@app.errorhandler(403)
def forbidden(e):
    """
    403 error
    """
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(e):
    """
    404 error
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    500 error
    """
    return render_template("errors/500.html"), 500


# Environment settings
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False)
