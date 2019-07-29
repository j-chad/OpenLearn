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
)

blueprint = Blueprint("public", __name__, static_folder="../static")