# -*- coding: utf-8 -*-
"""The controller for all views related to students"""
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify)

from .forms import JoinRoomForm

blueprint = Blueprint("student", __name__, static_folder="../../static", template_folder="../../templates/student")


@blueprint.route("/join", methods=["GET", "POST"])
def join_room():
    form = JoinRoomForm()
    if request.method == "GET":
        return render_template("join.html", form=form)
    else:
        exists = False
        message = ""
        if form.validate():
            exists = True
        else:
            message = list(form.errors)[0][0]

        return jsonify({
            "roomCode": form.room_code.data,
            "exists": exists,
            "message": message
        }), 200
