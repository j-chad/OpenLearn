# -*- coding: utf-8 -*-
"""The controller for all landing pages and anything that you shouldn't be logged in for"""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort)

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
    return render_template("sign-in.html")
