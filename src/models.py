"""Models for Personal app"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """
    Connect to database
    """
    db.app = app
    db.init_app(app)


class Feedback(db.Model):
    """
    Feedback
    """

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """A better readable representation of the instance"""
        return f"<Feedback id={self.id} email={self.email} \
            title={self.title} content={self.content}>"


class Admin(db.Model):
    """
    Admin Access
    """

    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd):
        """
        - Sign up admin
        - Hash password & secret question
        - Add admin to database
        """
        hashed_pwd = bcrypt.generate_password_hash(pwd)

        admin = cls(
            username=username,
            password=hashed_pwd,
        )
        db.session.add(admin)

        return admin

    @classmethod
    def authenticate(cls, username, pwd):
        """
        Validate that admin exists and password is correct.
        Return user if valid, else return false
        """

        u = Admin.query.filter_by(username=username).first()
        print("UUUUUUU ====> " + str(u))
        print("UUUU...PASSWORD ======> " + pwd)

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False

    @classmethod
    def hash_pwd(cls, raw_pwd):
        """
        Hashes password and returns it
        """
        hashed = bcrypt.generate_password_hash(raw_pwd).decode("utf8")
        return hashed
