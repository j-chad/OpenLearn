# -*- coding: utf-8 -*-
import random

import click
import flask
from flask.cli import with_appcontext

from OpenLearn.extensions import db
from OpenLearn.settings import ConfigType


@click.command()
@with_appcontext
def rebuild_database() -> None:
    """Builds the database."""
    if flask.current_app.debug is False:
        click.secho("You are in production mode", bold=True, fg="white", bg="red")
        click.confirm("Are you sure about this?", abort=True, default=False)
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        click.echo(f"Confirm by using the code: {click.style(code, fg='red', bold=True)}")
        u_code = click.prompt("Code", confirmation_prompt=True)
        if code != u_code:
            raise click.Abort

    db.session.commit()
    db.drop_all()
    click.secho("Dropped All Tables", fg="red", bold=True)
    db.create_all()
    click.secho("Created All Tables", fg="green", bold=True)


@click.command()
@with_appcontext
def current_config() -> None:
    click.echo(repr(ConfigType.Auto.config))
