import os
from flask import Flask, render_template, redirect, session, g, abort
from flask_mail import Mail, Message

from models import db, connect_db, Feedback, Admin
from forms import LoginForm, ContactForm, RegisterForm

app = Flask(__name__, static_url_path == "/", static_folder="public")

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "secretkey")
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PWD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("EMAIL")

CURR_USER_KEY = os.environ.get("CURR_USER_KEY")

connect_db(app)

mail = Mail(app)


##################
# Global Methods ##########################################
##################


# def do_login(admin):
#     """
#     Log in Admin
#     """
#     session[CURR_USER_KEY] = admin.username


# def do_logout():
#     """
#     Logout Admin
#     """
#     if "user_id" in session:
#         del session[CURR_USER_KEY]


###################
# Before Requests #########################################
###################


# @app.before_request
# def add_admin_to_g():
#     """
#     If we're logged in, add curr user to Flask global.
#     """
#     if CURR_USER_KEY in session:
#         g.user = Admin.query.get(session["user_id"])
#     else:
#         g.user = None


####################
# Main Page Routes ########################################
####################


@app.route("/")
def homepage():
    """
    GET ROUTE:
    - Redirect to construction page
    """
    form = ContactForm()
    return render_template("/main/index.html", form=form)


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
    form = ContactForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        feedback = Feedback(name=name, email=email, message=message)
        try:
            db.session.add(feedback)
            db.session.commit()

            msg = Message("New Feedback", recipients=[os.environ.get("EMAIL_TO")])
            msg.html = render_template(
                "/mail/feedback.html", name=name, email=email, message=message
            )
            mail.send(msg)
            return redirect("/thanks")
        except:
            form.name.errors = ["Unable to save message"]

    return render_template("/main/index.html", form=form)


@app.route("/thanks")
def show_thanks():
    """
    GET ROUTE:
    -Display feedback accepted message
    """
    return render_template("/main/thanks.html")


################
# Admin Routes ############################################
################


# @app.route("/admin")
# def admin_page():
#     """
#     GET ROUTE:
#     -Show feedback and logout link
#     """
#     if not g.user:
#         abort(403)
#     else:
#         feedback = Feedback.query.all()
#         return render_template("/admin/admin.html", feedback=feedback)


# @app.route("/admin/reg", methods=["GET", "POST"])
# def admin_registration():
#     """
#     GET ROUTE:
#     -Display admin register form
#     """
#     form = RegisterForm()

#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         secret = form.secret.data

#         if secret != os.environ.get("SECRET"):
#             abort(403)

#         # try:
#         admin = Admin.register(username=username, pwd=password)

#         db.session.commit()
#         # except:
#         #     form.username.errors = ["Unable to add admin"]
#         return redirect("/admin/login")

#     return render_template("/admin/register.html", form=form)


# @app.route("/admin/login", methods=["GET", "POST"])
# def admin_login():
#     """
#     GET ROUTE:
#     -Show login form
#     --------------------
#     POST ROUTE:
#     -Authenticate login
#     -Redirect to '/admin'
#     """
#     form = LoginForm()

#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data

#         admin = Admin.authenticate(username, password)

#         if admin:
#             do_login(admin)
#             return redirect("/admin")
#         else:
#             form.username.errors = ["Invalid username/password"]

#     return render_template("/admin/login.html", form=form)


# @app.route("/logout")
# def logout_admin():
#     """
#     GET ROUTE:
#     - Log the user out
#     """
#     do_logout()
#     return redirect("/")


####################
# Open Graph Route #################
####################


@app.route("/ogimg/ogimg.png")
def return_og_img():
    """
    GET ROUTE:
    - Returns the image for the Open Graph Image Meta
    """
    return "<img src='/static/images/og_img.png' />"


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
