from flask import redirect, render_template, session
from functools import wraps

import sqlite3


# Error message template
def error(message):
    """Render error message to user."""
    return render_template("error.html", message=message)


# SQL Connection function
def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect("grocery.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# The following login_required function is adapted from CS50 Finance problem set
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
