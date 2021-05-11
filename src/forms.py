from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


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
