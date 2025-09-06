from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import apology, login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@app.route('/home')
def index():
    # check user account amount
    # current_user = session["user_id"]
    # print(current_user)

    return render_template('index.html')

db = sqlite3.connect('database.db')
db.execute(
    'CREATE TABLE IF NOT EXISTS PARTICIPANTS (username TEXT, \
        email TEXT, city TEXT, state TEXT, country TEXT, password TEXT)')

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
        return render_template("index.html")
    else:
        return render_template('join.html')



# ColoradoBatman
# Batman

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

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )
        db.close()
        # with sqlite3.connect("database.db") as users:
        #     cursor = users.cursor()
        #     cursor.execute("SELECT * FROM participants WHERE username = ?", request.form.get(
        #                    "username"))
        #     rows = cursor.fetchall()
        #     print(rows)


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/participants')
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