# -*- coding: utf-8 -*-
"""The controller for all views related to students"""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify)

blueprint = Blueprint("student", __name__, static_folder="../../static", template_folder="../../templates/student")


@blueprint.route("/join", methods=["GET", "POST"])
def join_room():
    if request.method == "GET":
        return render_template("join.html")
    else:
        code = request.form["room-code"]

        return jsonify({
            "roomCode": code,
            "exists": False
        }), 200
