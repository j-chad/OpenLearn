# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, EqualTo, InputRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(message="You must enter your username"),
        Length(min=3, max=25, message="Username does not exist")
    ])
    password = PasswordField("Password", validators=[
        InputRequired(message="You must enter your username")
    ])


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
