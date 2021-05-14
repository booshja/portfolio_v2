from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Optional
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """
    Form for Admin registration
    """

    username = StringField(
        "Username", validators=[InputRequired(message="Username is required")]
    )
    password = PasswordField(
        "Password", validators=[InputRequired("Password is required")]
    )
    secret = PasswordField("Secret", validators=[InputRequired("Secret is MANDATORY")])


class LoginForm(FlaskForm):
    """
    Form for Admin Login
    """

    username = StringField(
        "Username", validators=[InputRequired(message="Username is required")]
    )
    password = PasswordField(
        "Password", validators=[InputRequired("Password is required")]
    )


class ContactForm(FlaskForm):
    """
    Form for User Feedback
    """

    name = StringField("Name", validators=[InputRequired(message="Name is required")])
    email = StringField("Email (Optional)", validators=[Optional()])
    message = TextAreaField(
        "Message", validators=[InputRequired(message="Message is required")]
    )
