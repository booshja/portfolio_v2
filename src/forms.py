from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm


class FeedbackForm(FlaskForm):
    """
    Form for feedback
    """

    email = StringField(
        "Name",
        validators=[
            InputRequired(message="Email cannot be left blank"),
            Email(message="Email must be in example@email.com format"),
        ],
    )
    title = StringField(
        "Email", validators=[InputRequired(message="Subject cannot be left blank")]
    )
    content = TextAreaField(
        "Message", validators=[InputRequired(message="Message cannot be left blank")]
    )


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
