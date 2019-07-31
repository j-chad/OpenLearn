# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""

import logging
import sys

from flask import Flask, render_template

from OpenLearn import extensions, database, commands
from . import views
from . import settings


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    """
    app = Flask(__name__.split(".")[0], instance_relative_config=True)

    settings.configure_app(app)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    extensions.db.init_app(app)
    extensions.bcrypt.init_app(app)
    extensions.login_manager.init_app(app)

    # Flask Login
    @extensions.login_manager.user_loader
    def load_user(user_id):
        return database.User.query.get(int(user_id))


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(views.public.blueprint)
    app.register_blueprint(views.student.blueprint)
    app.register_blueprint(views.teacher.blueprint)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in []:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": extensions.db,
            "User": database.User,
            "Quiz": database.Quiz,
            "Question": database.Question,
            "NumericQuestion": database.NumericQuestion,
            "TextQuestion": database.TextQuestion,
            "QuestionType": database.QuestionType,
            "Room": database.Room
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.rebuild_database)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
