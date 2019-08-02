from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional


class CreateQuizForm(FlaskForm):
    title = StringField("Quiz Title", validators=[
        InputRequired(message="You must provide a title for your quiz"),
        Length(min=3, max=30, message="Title must have between 3 and 30 characters"),
    ])
    description = TextAreaField("Description", validators=[
        Optional(),
        Length(min=3, max=110, message="Description must have between 3 and 110 characters")
    ])

    public = BooleanField(default=False)
    statistics_enabled = BooleanField(default=True)
    shuffle_questions = BooleanField(default=True)
