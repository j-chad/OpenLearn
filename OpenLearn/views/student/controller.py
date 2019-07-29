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
)

blueprint = Blueprint("student", __name__, static_folder="../static")