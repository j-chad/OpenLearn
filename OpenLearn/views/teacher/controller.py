# -*- coding: utf-8 -*-
"""The controller for all views related to teachers"""
from flask import (
    Blueprint,
    redirect, url_for)
from flask_login import login_required, logout_user

blueprint = Blueprint("teacher", __name__, static_folder="../static", template_folder="../templates/teacher")


@blueprint.route("/dashboard")
@login_required
def dashboard():
    return "You are logged in"


@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.login"))
