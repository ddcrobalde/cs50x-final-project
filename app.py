from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

from helpers import error, get_connection, login_required

import sqlite3

# Configure application
app = Flask(__name__)

# The session configuration and after_request function are adapted from CS50 Finance problem set
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Redirect with the selected sort option
def redirect_sorted():
    valid_sorts = {"alphabetical", "quantity_asc", "quantity_desc", "status", "date"}
    sort_by = request.form.get("sort", "date")
    if sort_by not in valid_sorts:
        sort_by = "date"
    return redirect(f"/?sort={sort_by}")


@app.route("/")
@login_required
def index():
    # Show the grocery list
    sort_by = request.args.get("sort", "date")
    conn = get_connection()
    db = conn.cursor()

    # Sort the grocery list based on the selected criteria
    user_id = session["user_id"]
    if sort_by == "alphabetical":
        rows = db.execute(
            "SELECT * FROM lists WHERE user_id = ? ORDER BY item COLLATE NOCASE ASC",
            (user_id,),
        ).fetchall()
    elif sort_by == "quantity_asc":
        rows = db.execute(
            "SELECT * FROM lists WHERE user_id = ? ORDER BY quantity ASC", (user_id,)
        ).fetchall()
    elif sort_by == "quantity_desc":
        rows = db.execute(
            "SELECT * FROM lists WHERE user_id = ? ORDER BY quantity DESC", (user_id,)
        ).fetchall()
    elif sort_by == "status":
        rows = db.execute(
            "SELECT * FROM lists WHERE user_id = ? ORDER BY purchased ASC", (user_id,)
        ).fetchall()
    else:
        # Default sorting by date and time added
        rows = db.execute(
            "SELECT * FROM lists WHERE user_id = ? ORDER BY date_time ASC", (user_id,)
        ).fetchall()

    conn.close()
    return render_template("index.html", rows=rows)


@app.route("/add", methods=["POST"])
@login_required
def add():
    # Get the item
    item = request.form.get("item")
    if not item or not item.strip():
        return error("Please provide an item name")
    item = item.strip().title()

    # Get the quantity
    try:
        quantity = int(request.form.get("quantity"))
    except (TypeError, ValueError):
        return error("Please provide a valid quantity")
    if quantity < 1:
        return error("Please provide a valid quantity")

    # Insert the new item into the grocery list, or if existing, add to its quantity
    user_id = session["user_id"]
    conn = get_connection()
    db = conn.cursor()
    # Check if item exists
    existing = db.execute(
        "SELECT id, quantity FROM lists WHERE item = ? AND user_id = ?",
        (
            item,
            user_id,
        ),
    ).fetchone()
    if existing:
        # Add to existing quantity
        new_quantity = existing[1] + quantity
        db.execute(
            "UPDATE lists SET quantity = ? WHERE id = ? AND user_id = ?",
            (
                new_quantity,
                existing[0],
                user_id,
            ),
        )
    else:
        # Insert new item
        db.execute(
            "INSERT INTO lists (item, quantity, user_id) VALUES (?, ?, ?)",
            (
                item,
                quantity,
                user_id,
            ),
        )
    conn.commit()
    conn.close()
    return redirect_sorted()


@app.route("/clear", methods=["POST"])
@login_required
def clear():
    # Clear the entire grocery list
    user_id = session["user_id"]
    conn = get_connection()
    db = conn.cursor()
    db.execute("DELETE FROM lists WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect_sorted()


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    # Edit the quantity of an item in the grocery list
    try:
        item_id = int(request.form.get("item_id"))
    except (TypeError, ValueError):
        return error("Invalid item selected")

    try:
        new_quantity = int(request.form.get("new_quantity"))
    except (TypeError, ValueError):
        return error("Please provide a valid quantity")
    if new_quantity < 1:
        return error("Please provide a valid quantity")

    # Update the quantity in the database
    user_id = session["user_id"]
    conn = get_connection()
    db = conn.cursor()
    db.execute(
        "UPDATE lists SET quantity = ? WHERE id = ? AND user_id = ?",
        (
            new_quantity,
            item_id,
            user_id,
        ),
    )
    conn.commit()
    conn.close()
    return redirect_sorted()


# The following login function is adapted from CS50 Finance problem set
@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear user_id
    session.clear()

    # If POST (submit login form)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password")

        # Query database for username (modified to not use CS50 Library)
        conn = get_connection()
        db = conn.cursor()
        row = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),)
        ).fetchone()
        conn.close()

        # Ensure username exists and password is correct
        if row is None or not check_password_hash(
            row["hash"], request.form.get("password")
        ):
            return error("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = row["id"]

        # Redirect user to home page
        return redirect("/")

    # If GET (login page)
    else:
        return render_template("login.html")


# The following logout function is adapted from CS50 Finance problem set
@app.route("/logout")
def logout():
    # Clear user_id
    session.clear()
    # Redirect to login page
    return redirect("/login")


# The following register function is adapted from my own solution in the CS50 Finance problem set
@app.route("/register", methods=["GET", "POST"])
def register():
    # If POST (submit registration)
    if request.method == "POST":

        # Store username and password hash in variables
        username = request.form.get("username").strip().lower()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username is blank
        if not username:
            return error("Please type in a username")

        # Username length check
        if len(username) < 3:
            return error("Username must be at least 3 characters long")

        # Check if password is blank
        if not password:
            return error("Please type in a password")

        # Password length check
        if len(password) < 6:
            return error("Password must be at least 6 characters long")

        # Check if confirmation matches
        if password != confirmation:
            return error("Password confirmation does not match")

        # Create hash of password
        password_hash = generate_password_hash(password)

        # Insert new user into users table in finance database (modified to not use CS50 Library)
        conn = get_connection()
        db = conn.cursor()
        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (
                    username,
                    password_hash,
                ),
            )
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.close()
            return error("Username already exists")

        # Redirect user to login page
        return redirect("/login")

    # If GET (display registration form)
    else:
        return render_template("register.html")


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    # Remove an item from the grocery list
    try:
        item_id = int(request.form.get("item_id"))
    except (TypeError, ValueError):
        return error("Select item to remove")

    # Remove the item from the database
    user_id = session["user_id"]
    conn = get_connection()
    db = conn.cursor()
    db.execute(
        "DELETE FROM lists WHERE id = ? AND user_id = ?",
        (
            item_id,
            user_id,
        ),
    )
    conn.commit()
    conn.close()
    return redirect_sorted()


@app.route("/toggle", methods=["POST"])
@login_required
def toggle():
    # Toggle the status of an item in the grocery list
    try:
        item_id = int(request.form.get("item_id"))
    except (TypeError, ValueError):
        return error("Invalid item selected")

    # Toggle the status in the database
    user_id = session["user_id"]
    conn = get_connection()
    db = conn.cursor()
    db.execute(
        "UPDATE lists SET purchased = 1 - purchased WHERE id = ? AND user_id = ?",
        (
            item_id,
            user_id,
        ),
    )
    conn.commit()
    conn.close()
    return redirect_sorted()
