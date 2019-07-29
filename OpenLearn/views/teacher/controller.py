# -*- coding: utf-8 -*-
"""The controller for all views related to teachers"""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

blueprint = Blueprint("teacher", __name__, static_folder="../static", template_folder="../templates/teacher")
