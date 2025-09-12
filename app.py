from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import json

from helpers import apology, login_required, lookup

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@app.route('/list')
@login_required
def index():
    # check user account amount
    current_user = session["user_id"]
    # print(current_user)

    return render_template('list.html')

connect = sqlite3.connect('database.db')
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
    FOREIGN KEY (user_id) REFERENCES participants (id) ON DELETE CASCADE)')


@app.route('/search', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':

        searchResults = lookup(request.form.get("searchterm"))
        # print(searchResults)
        return render_template("search.html", searchResults=searchResults)

    else:
        return render_template("search.html")

@app.route('/map')
def map():
    return render_template("map.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        password = generate_password_hash(request.form.get("password")) # request.form['password']
        with sqlite3.connect("database.db") as users:
            cursor = users.cursor()
            cursor.execute("INSERT INTO PARTICIPANTS \
            (username,email,city,state,country,password) VALUES (?,?,?,?,?,?)",
                           (username, email, city, state, country, password))
            users.commit()
        return render_template("list.html")
    else:
        return render_template('join.html')

# @app.route('/add', methods=['POST'])
# def add():
#     if request.method == 'POST':


# Test Creds
# Username: Curtis
# Password: Batman


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
            print(request.form.get("username"))
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


if __name__ == '__main__':
    app.run(debug=False)