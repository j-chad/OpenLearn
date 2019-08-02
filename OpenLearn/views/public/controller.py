# -*- coding: utf-8 -*-
"""The controller for all landing pages and anything that you shouldn't be logged in for"""
from flask import (
    Blueprint,
    current_app,
    render_template,
    abort, redirect, url_for)
from flask_login import login_user, logout_user, current_user

from OpenLearn.database import User
from OpenLearn.extensions import db
from .forms import RegisterForm, LoginForm

blueprint = Blueprint("public", __name__, static_folder="../../static", template_folder="../../templates/public")


@blueprint.route("/ping")
def ping():
    if current_app.debug or current_app.testing:
        return "pong"
    else:
        abort(404)


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.login"))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("teacher.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(url_for("teacher.dashboard"))
    return render_template("login.html", form=form)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("teacher.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("teacher.dashboard"))
    return render_template("register.html", form=form)
