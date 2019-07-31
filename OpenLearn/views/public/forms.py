# -*- coding: utf-8 -*-
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired

from OpenLearn.database import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(message="You must enter your username"),
        Length(min=3, max=25, message="Username does not exist")
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="You must enter your username")
    ])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.user: Optional[User] = None

    def validate(self):
        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(),
        Length(min=3, max=25, message="Username must be between 3-25 characters")
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="You must provide a password"),
        Length(min=6, message="Password must be at least 6 characters")
    ])
    confirm_password = PasswordField("Repeat Password", validators=[
        EqualTo('password', message="Passwords must match")
    ])
