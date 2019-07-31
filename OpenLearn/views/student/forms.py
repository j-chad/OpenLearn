# -*- coding: utf-8 -*-
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length, Regexp

from OpenLearn.database import Room


class JoinRoomForm(FlaskForm):
    room_code = StringField("Room Code", validators=[
        InputRequired(message="Malformed Room Code"),
        Length(min=9, max=9, message="Malformed Room Code"),
        Regexp("([A-Z0-9]){4}-([A-Z0-9]){4}", message="Malformed Room Code")
    ])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super().__init__(*args, **kwargs)
        self.room: Optional[Room] = None

    def validate(self):
        initial_validation = super().validate()
        if not initial_validation:
            return False

        # TODO: Room Logic
        self.room_code.errors.append("Invalid Code")
        return False
