from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///auxilium.db")


@app.route("/")
@login_required
def index():
    """Show catered resources"""
    resources = {}
    # Query database for resource results
    results = db.execute("""SELECT gender, age, ethnicity1, ethnicity2, ethnicity3, ethnicity4, ethnicity5, ethnicity6, ethnicity7, ethnicity8, ethnicity9, ethnicity10, immigrant, translator, income, homeless, transition, utility, food, \
                        disability, deaf, clothes, children, child_age, baby, elementary, college, child_dis, bch, child_ins, uninsured, \
                        state_ins, ins_app, meds, drugs, mental, violence, law, job, edu FROM users WHERE id = :user_id""", \
                        user_id=session["user_id"])

    resources = db.execute("""SELECT name, address, number, website, description FROM resources WHERE sex = 'any' OR sex = :gender AND ages = 'any'
                            OR type = :ethnicity2 OR type = :ethnicity3 OR type = :ethnicity4 OR type = :ethnicity5 OR
                            type = :ethnicity6 OR type = :ethnicity7 OR type = :ethnicity8 OR type = :ethnicity9 AND translators = :translator
                            AND income = 'any' OR income = :income AND homeless = 'no' OR homeless = :homeless OR type = :transition OR
                            type = :utility OR type = :food OR disabled = :disability OR type = :clothes OR type = :children OR type = :elementary
                            OR type = :child_age OR type = :college OR disabled = :child_dis OR type = :uninsured OR type = :meds OR type = :drugs
                            OR type = :mental OR type = :violence OR type = :law OR type = :job OR type = :edu""",
                            gender=results[0]['gender'], ethnicity2=results[0]['ethnicity2'],
                            ethnicity3=results[0]['ethnicity3'], ethnicity4=results[0]['ethnicity4'], ethnicity5=results[0]['ethnicity5'],
                            ethnicity6=results[0]['ethnicity6'], ethnicity7=results[0]['ethnicity7'], ethnicity8=results[0]['ethnicity8'],
                            ethnicity9=results[0]['ethnicity9'], translator=results[0]['translator'], income=results[0]['income'],
                            homeless=results[0]['homeless'], transition=results[0]['transition'], utility=results[0]['utility'], food=results[0]['food'],
                            disability=results[0]['disability'], clothes=results[0]['clothes'], children=results[0]['children'],
                            elementary=results[0]['elementary'], child_age=results[0]['child_age'], college=results[0]['college'], child_dis=results[0]['child_dis'],
                            uninsured=results[0]['uninsured'], meds=results[0]['meds'], drugs=results[0]['drugs'], mental=results[0]['mental'],
                            violence=results[0]['violence'], law=results[0]['law'], job=results[0]['job'], edu=results[0]['edu'])

    return render_template("index.html", resources=resources)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Show profile questions"""

    if request.method == "POST":

        # Query database for posts
        db.execute("""UPDATE users SET gender = :gender, age = :age, ethnicity1 = :ethnicity1, ethnicity2 = :ethnicity2, ethnicity3 = :ethnicity3, ethnicity4 = :ethnicity4, ethnicity5 = :ethnicity5, ethnicity6 = :ethnicity6, ethnicity7 = :ethnicity7, \
                        ethnicity8 = :ethnicity8, ethnicity9 = :ethnicity9, ethnicity10 = :ethnicity10, immigrant = :immigrant, translator = :translator, income = :income, homeless = :homeless, transition = :transition, utility = :utility, food = :food, \
                        disability = :disability, deaf = :deaf, clothes = :clothes, children = :children, child_age = :child_age, baby = :baby, elementary = :elementary, college = :college, child_dis = :child_dis, bch = :bch, child_ins = :child_ins, uninsured = :uninsured, \
                        state_ins = :state_ins, ins_app = :ins_app, meds = :meds, drugs = :drugs, mental = :mental, violence = :violence, law = :law, job = :job, edu = :edu WHERE id = :user_id""", gender=request.form.get("gender"), age=request.form.get("age"), \
                        ethnicity1=request.form.get("ethnicity1"), ethnicity2=request.form.get("ethnicity2"), ethnicity3=request.form.get("ethnicity3"),  ethnicity4=request.form.get("ethnicity4"), ethnicity5=request.form.get("ethnicity5"), ethnicity6=request.form.get("ethnicity6"), ethnicity7=request.form.get("ethnicity7"), ethnicity8=request.form.get("ethnicity8"), ethnicity9=request.form.get("ethnicity9"), ethnicity10=request.form.get("ethnicity10"), immigrant=request.form.get("immigrant"), translator=request.form.get("translator"), \
                        income=request.form.get("income"), homeless=request.form.get("homeless"), transition=request.form.get("transition"), \
                        utility=request.form.get("utility"), food=request.form.get("food"), disability=request.form.get("disability"), \
                        deaf=request.form.get("deaf"), clothes=request.form.get("clothes"), children=request.form.get("children"), \
                        child_age=request.form.get("child_age"), baby=request.form.get("baby"), elementary=request.form.get("elementary"), \
                        college=request.form.get("college"), child_dis=request.form.get("child_dis"), bch=request.form.get("child_dis"), \
                        child_ins=request.form.get("child_ins"), uninsured=request.form.get("uninsured"), state_ins=request.form.get("state_ins"), \
                        ins_app=request.form.get("ins_app"), meds=request.form.get("meds"), drugs=request.form.get("drugs"), \
                        mental=request.form.get("mental"), violence=request.form.get("mental"), law=request.form.get("law"), job=request.form.get("job"), \
                        edu=request.form.get("edu"), user_id=session["user_id"])

        return redirect("/")

    else:
        return render_template("profile.html")


@app.route("/discussion")
@login_required
def discussion():
    """Show discussion board"""

    # Query database for posts
    posts = db.execute("SELECT post_id, topic, date_time FROM posts ORDER BY date_time DESC")

    return render_template("discussion.html", posts=posts)


# https://stackoverflow.com/questions/7478366/create-dynamic-urls-in-flask-with-url-for
@app.route("/thread/<int:post_id>/", methods=["GET", "POST"])
@login_required
def thread(post_id):
    """Show comment input"""

    if request.method == "POST":
        db.execute("INSERT INTO comments (content, post_id) VALUES (:content, :post_id)", content=request.form.get("response"), post_id=post_id)
        results = db.execute("SELECT topic, question FROM posts WHERE post_id = :post_id", post_id = post_id)
        comments = db.execute("SELECT content, comment_time FROM comments WHERE post_id = :post_id ORDER BY comment_time DESC", post_id = post_id)
        return render_template("thread.html", results=results, comments=comments, post_id=post_id)

    else:
        results = db.execute("SELECT topic, question FROM posts WHERE post_id = :post_id", post_id = post_id)
        comments = db.execute("SELECT content, comment_time FROM comments WHERE post_id = :post_id ORDER BY comment_time DESC", post_id = post_id)
        return render_template("thread.html", results=results, comments=comments, post_id=post_id)


@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """Show post input"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure topic was submitted
        if not request.form.get("topic"):
            return apology("must provide topic", 403)

        # Ensure question was submitted
        elif not request.form.get("question"):
            return apology("must provide question or concern", 403)

        # Store their information into the users database
        db.execute("INSERT INTO posts (topic, question) VALUES (:topic, :question)", topic=request.form.get("topic"), question=request.form.get("question"))

        # Redirect user to home page
        return redirect("/discussion")

    else:
        return render_template("post.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # If the request method is post, run this section that stores the information they input
    if request.method == "POST":
        # Check that each field was filled
        if not request.form.get("username"):
            return apology("Missing username!", 400)
        elif not request.form.get("password"):
            return apology("Missing password!", 400)
        elif not request.form.get("confirmation"):
            return apology("Missing password confirmation!", 400)

        # Check that the password and the confirmation password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation password do not match!", 400)

        # Store their information into the users database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get(
                            "username"), hash=generate_password_hash(request.form.get("password")))

        # If db.execute fails, then the username already exists
        if not result:
            return apology("Username already exists!", 400)

        # Automatically log them in and save their session
        session["user_id"] = result

        # Redirect user to homepage
        return redirect("/profile")

    # If the request method is get, just load the template for the /register page
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
