from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
from cachelib.file import FileSystemCache
from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
# You may also want a dedicated endpoint that just returns JSON
from flask import jsonify

import sqlite3
import os

from helpers import apology, login_required, lookup, add, delete_item_from_db, is_text_only

app = Flask(__name__)

# Load API key from environment variable for security
app.config['GOOGLE_MAPS_API_KEY'] = os.environ.get('GOOGLE_MAPS_API_KEY')

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_TYPE"] = "cachelib"
app.config["SESSION_CACHELIB"] = FileSystemCache(cache_dir="flask_session", threshold=500)
Session(app)

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

# Enable foreign key support
cursor.execute('PRAGMA foreign_keys = ON;')

connect.execute(
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, \
        email TEXT, city TEXT, state TEXT, country TEXT, password TEXT)')

connect.execute(
    'CREATE TABLE IF NOT EXISTS bucket_lists ( \
    id INTEGER PRIMARY KEY AUTOINCREMENT, \
    user_id INTEGER, \
    name TEXT NOT NULL, \
    description TEXT, \
    url TEXT, \
    latitude DOUBLE PRECISION NOT NULL, \
    longitude DOUBLE PRECISION NOT NULL, \
    FOREIGN KEY (user_id) REFERENCES participants (id) ON DELETE CASCADE)')

connect.execute(
    'CREATE TABLE IF NOT EXISTS journal ( \
    id INTEGER PRIMARY KEY AUTOINCREMENT, \
    bucket_list_id INTEGER NOT NULL, \
    journal_text TEXT NOT NULL, \
    visited_date DATE, \
    FOREIGN KEY (bucket_list_id) REFERENCES bucket_lists (id) ON DELETE CASCADE)')


# Assume this function gets the raw data from your database
def rows_to_dicts(cursor):
    """Convert cursor results to a list of dictionaries."""
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# def get_bucket_lists_for_user(user_id):
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, user_id, name, description, url, latitude, longitude FROM bucket_lists WHERE user_id = ?", (user_id,))
#     # Call the conversion function here
#     bucket_lists = rows_to_dicts(cursor)
#     conn.close()
#     return bucket_lists

def get_bucket_lists_data(user_id):
    """Fetches bucket list items and checks for existing journal entries."""
    with sqlite3.connect("database.db") as bucket:
        cursor = bucket.cursor()
        cursor.execute("""
            SELECT 
                bl.id, 
                bl.name, 
                bl.description, 
                bl.url, 
                bl.latitude, 
                bl.longitude, 
                COUNT(j.id) > 0 AS has_journal
            FROM bucket_lists bl
            LEFT JOIN journal j ON bl.id = j.bucket_list_id
            WHERE bl.user_id = ?
            GROUP BY bl.id
        """, (user_id,))
        
        column_names = [description[0] for description in cursor.description]
        return [dict(zip(column_names, row)) for row in cursor.fetchall()]


@app.route('/')
@app.route('/list')
@login_required
def index():
    # check user account amount
    current_user = session["user_id"]

    bucket_lists_data = get_bucket_lists_data(current_user)

    return render_template('list.html', bucket_lists=bucket_lists_data)


@app.route('/my-lists/<int:user_id>')
def show_user_lists(user_id):
    bucket_lists_data = get_bucket_lists_data(user_id)
    return render_template('my_lists.html', bucket_lists=bucket_lists_data)


@app.route('/api/user-lists/<int:user_id>')
def get_user_lists_api(user_id):
    bucket_lists_data = get_bucket_lists_data(user_id)
    return jsonify(bucket_lists_data)


@app.route("/api/journal/<int:item_id>")
def get_journal_entries(item_id):
    """API endpoint to get all journal entries for a given item_id."""
    with sqlite3.connect("database.db") as bucket:
        cursor = bucket.cursor()
        cursor.execute("SELECT visited_date, journal_text FROM journal WHERE bucket_list_id = ? ORDER BY visited_date DESC", (item_id,))
        column_names = [description[0] for description in cursor.description]
        journal_entries = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    
    return jsonify(journal_entries)


@app.route('/search', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        user_input = request.form.get('searchterm')
      
        # Ensure user entered text
        if not is_text_only(user_input):
            print(f'cleansed user input: {user_input}')
            return apology("please provide text only", 400)

        try:
            searchResults = lookup(request.form.get("searchterm"))
            print(searchResults)
            return render_template("search.html", searchResults=searchResults)
        except IndexError:
            # Generic ValueError handler, though DataProcessingError is more specific
            flash(f"Invalid response. Try again!")
            return redirect("/search")
        
        
        

    else:
        return render_template("search.html")

@app.route("/map")
def map_page():
    # check user account amount
    current_user = session["user_id"]
    bucket_lists = get_bucket_lists_data(current_user)
    return render_template(
        "map.html",
        bucket_lists=bucket_lists,
        GOOGLE_MAPS_API_KEY=app.config['GOOGLE_MAPS_API_KEY']
    )


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure the passwords match
        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("the password and confirmation don't match", 400)

        username = request.form['username']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        password = generate_password_hash(request.form.get("password")) # request.form['password']
        try:
            with sqlite3.connect("database.db") as users:
                cursor = users.cursor()
                cursor.execute("INSERT INTO PARTICIPANTS \
                (username,email,city,state,country,password) VALUES (?,?,?,?,?,?)",
                            (username, email, city, state, country, password))
                users.commit()
        except BaseException as e:
            print('User already exists')
            return apology("username already exists", 400)
        
        return redirect("/")
    else:
        return render_template('join.html')


# Test Creds
# Username: Curtis
# Password: Batman
# Jack / Batman
# Ruby / Robin


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            # print(request.form.get("username"))
            cursor.execute("SELECT * FROM participants WHERE username = ?", [request.form.get(
                           "username")])
            rows = cursor.fetchall()
        # print(rows)


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][6], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Route is currently unused but would be implemented for admins in
# a real world project
@app.route('/participants')
@login_required
def participants():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM PARTICIPANTS')

    data = cursor.fetchall()
    return render_template("participants.html", data=data)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == 'POST':
        try:
            bucketItemData = add(request.form)
            print(bucketItemData)
        except ValueError as e:
            # Generic ValueError handler, though DataProcessingError is more specific
            flash(f"Error processing data: {e}")
            return redirect("/search")
        
        return redirect("/")
    else:
        return render_template("search.html")


@app.route("/delete-item", methods=["POST"])
def delete_item():
    item_id = request.form.get("item_id")
    print(f'item_id: {item_id}')
    if delete_item_from_db(item_id):
        flash("Item was successfully deleted.")
    else:
        flash("Failed to delete item.")
    return redirect("/list")


@app.route("/record-visit", methods=["POST"])
def record_visit():
    item_id = request.form.get("item_id")
    visited_date = request.form.get("visited_date")
    journal_text = request.form.get("journal_text")

    if not all([item_id, visited_date, journal_text]):
        flash("Error: Missing required journal information.", "warning")
        # item_id isn't getting passed here. :(
        print(f'journal info: {item_id}, {visited_date}, {journal_text}')
        return redirect("/list")

    try:
        with sqlite3.connect("database.db") as bucket:
            cursor = bucket.cursor()
            cursor.execute("INSERT INTO journal (bucket_list_id, journal_text, visited_date) VALUES (?, ?, ?)",
                            (item_id, journal_text, visited_date))
            bucket.commit()
        flash("Journal entry successfully recorded!", "success")
    except sqlite3.Error as e:
        flash(f"Database error: {e}", "danger")
    
    return redirect("/list")


if __name__ == '__main__':
    app.run(debug=False)