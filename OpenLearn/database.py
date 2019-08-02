# -*- coding: utf-8 -*-
import datetime
import enum
import random
import string
from decimal import Decimal
from typing import Union, List

from flask_login import UserMixin
from sqlalchemy import func

from .extensions import db, bcrypt

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship

# Type Declarations
MString = Union[str, db.Column]
MInteger = Union[int, db.Column]
MDecimal = Union[Decimal, db.Column]
MBoolean = Union[bool, db.Column]
MDateTime = Union[datetime.datetime, db.Column]
MDate = Union[datetime.date, db.Column]


class QuestionType(enum.Enum):
    Numeric = 0
    Text = 1

    @property
    def type(self):
        return {
            QuestionType.Numeric: NumericQuestion,
            QuestionType.Text: TextQuestion
        }[self]


class User(db.Model, UserMixin):
    id: MInteger = db.Column(db.Integer, primary_key=True)
    username: MString = db.Column(db.String(25), unique=True, nullable=False)
    __password = db.Column("password", db.Binary(60), nullable=False)

    quizzes: List["Quiz"] = relationship("Quiz", back_populates="owner")

    created_on: MDateTime = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        pw_hash = bcrypt.generate_password_hash(value)
        self.__password = pw_hash

    def check_password(self, candidate) -> bool:
        return bcrypt.check_password_hash(self.__password, candidate)


class Quiz(db.Model):
    id: MInteger = db.Column(db.Integer, primary_key=True)
    title: MString = db.Column(db.String(30), unique=True, nullable=False)
    description: MString = db.Column(db.Text, unique=False, nullable=True)

    questions: List[Union["Question", "QuestionABC"]] = db.relationship('Question', back_populates="quiz",
                                                                        order_by="Question.sort_index")

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship("User", back_populates="quizzes")

    created_on: MDateTime = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())


class Question(db.Model):
    __mapper_args__ = {'polymorphic_on': "type"}

    id: MInteger = db.Column(db.Integer, primary_key=True)
    text: MString = db.Column(db.Text, nullable=False)
    sort_index = db.Column(db.Integer, nullable=False)

    type: QuestionType = db.Column(db.Enum(QuestionType), nullable=False)

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz: Quiz = db.relationship('Quiz', back_populates="questions")

    def __init__(self, *args, **kwargs):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError


class NumericQuestion(Question):
    __tablename__ = "numericQuestion"
    __mapper_args__ = {'polymorphic_identity': QuestionType.Numeric}

    id = Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.Numeric(precision=12, scale=5))  # 0000000.00000

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        return other == self.answer


class TextQuestion(Question):
    __tablename__ = "textQuestion"
    __mapper_args__ = {'polymorphic_identity': QuestionType.Text}

    id = Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    answer = db.Column(db.Text)

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        return other == self.answer


class Room(db.Model):
    id: MInteger = db.Column(db.Integer, primary_key=True)
    active: MBoolean = db.Column(db.Boolean, default=False)
    key: MString = db.Column(db.String(8), default=lambda: Room.generate_key())

    controller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    controller = db.relationship("User")

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    quiz: Quiz = db.relationship('Quiz')

    created_on: MDateTime = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    @staticmethod
    def generate_key():
        while True:
            temp_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not db.session.query(db.exists().where(Room.active, Room.key == temp_key)).scalar():
                return temp_key
