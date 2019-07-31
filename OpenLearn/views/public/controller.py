# -*- coding: utf-8 -*-
"""The controller for all landing pages and anything that you shouldn't be logged in for"""
from flask import (
    Blueprint,
    current_app,
    render_template,
    abort, redirect)

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


@blueprint.route("/sign-in")
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/success")
    return render_template("sign-in.html", form=form)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect("/success")
    return render_template("register.html", form=form)
