# -*- coding: utf-8 -*-
"""The controller for all views related to teachers"""
from flask import (
    Blueprint,
    render_template, redirect, url_for, abort)
from flask_login import login_required, current_user

from OpenLearn.database import Quiz
from OpenLearn.extensions import db
from .forms import CreateQuizForm

blueprint = Blueprint("teacher", __name__, static_folder="../../static", template_folder="../../templates/teacher")


@blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")  # Todo: Actually make it pretty + usable


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreateQuizForm()
    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            owner=current_user
        )
        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for("teacher.edit_quiz", quiz_id=quiz.id))
    return render_template("create.html", form=form)


@blueprint.route("/edit/<int:quiz_id>")
@login_required
def edit_quiz(quiz_id):
    quiz: Quiz = Quiz.query.get(quiz_id)
    if quiz is None:
        return abort(404)

    return f"Editing Quiz: {quiz.title}"
