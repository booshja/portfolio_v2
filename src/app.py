import os
from flask import Flask, render_template, redirect, session, g, jsonify, abort

from models import db, connect_db, Feedback, Admin
from forms import FeedbackForm, LoginForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///portfolio_test"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secretkey")

CURR_USER_KEY = os.environ.get("CURR_USER_KEY")

connect_db(app)


##################
# Global Methods ##########################################
##################


def do_login(admin):
    """
    Log in Admin
    """
    session[CURR_USER_KEY] = admin.username


def do_logout():
    """
    Logout Admin
    """
    if "user_id" in session:
        del session[CURR_USER_KEY]


###################
# Before Requests #########################################
###################


@app.before_request
def add_admin_to_g():
    """
    If we're logged in, add curr user to Flask global.
    """
    if CURR_USER_KEY in session:
        g.user = Admin.query.get(session["user_id"])
    else:
        g.user = None


####################
# Main Page Routes ########################################
####################


@app.route("/")
def homepage():
    """
    GET ROUTE:
    - Redirect to construction page
    """
    form = FeedbackForm()
    return render_template("index.html", form=form)


@app.route("/construction")
def construction_page():
    """
    GET ROUTE:
    - Construction landing page
    """
    return render_template("construction.html")


@app.route("/contact", methods=["POST"])
def process_feedback():
    """
    GET ROUTE:
    -Display form for feedback
    --------------------
    POST ROUTE:
    -Log info into database
    -Redirect to '/feedback/thanks'
    """
    form = FeedbackForm()

    if form.validate.on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"error": "Error saving to database."})

        resp = {"status": "accepted"}
        return jsonify(resp)

    abort(403)


################
# Admin Routes ############################################
################


@app.route("/admin/<username>")
def admin_page(username):
    """
    GET ROUTE:
    -Show feedback and logout link
    """
    # if not g.user:
    #     abort(403)
    # else:
    admin = Admin.query.get_or_404(username)
    feedback = Feedback.query.all()
    return render_template("admin.html", admin=admin, feedback=feedback)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """
    GET ROUTE:
    -Show login form
    --------------------
    POST ROUTE:
    -Authenticate login
    -Redirect to '/admin'
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.authenticate(username, password)

        if admin:
            do_login(admin)
            return redirect(f"/admin/{admin.username}")
        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("/admin/login.html", form=form)


@app.route("/admin/logout")
def logout_admin():
    """
    GET ROUTE:
    - Log the user out
    """
    do_logout()
    return redirect("/")


##########################
# Open Graph Image Route #####################################
##########################


@app.route("/ogimg/ogimg.png")
def return_og_img():
    """
    GET ROUTE:
    - Returns the image for the Open Graph Image Meta
    """
    return "<img src='../static/images/og_img.png' />"


#######################
# Custom Error Routes #####################################
#######################


@app.errorhandler(403)
def unauthorized(e):
    """
    Unauthorized Access Error
    """
    print("403 ERROR =====> ", e)
    return render_template("error.html", error="403 - Unauthorized Access")


@app.errorhandler(404)
def page_not_found(e):
    """
    Page Not Found Error
    """
    print("404 ERROR =====> ", e)
    return render_template("error.html", error="404 - Not Found")


@app.errorhandler(500)
def server_error(e):
    """
    Internal Error
    """
    print("500 ERROR =====> " + e)
    return render_template("error.html", error="500 - Server Error")
