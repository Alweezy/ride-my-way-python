import os
from datetime import datetime, timedelta

import jwt
from flask_bcrypt import Bcrypt
from flask import current_app

from api.app import db


class Base(db.Model):

    __abstract__ = True

    """creates the base class from which all models inherit
    """
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def save(self):

        """Save an entry into the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete an entry
        """
        db.session.delete(self)
        db.session.commit()


class User(Base):
    """Creates a user model
    """
    __tablename__ = "users"

    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    questions = db.relationship('Question', backref="users", order_by="Question.id",
                                cascade="all,delete-orphan")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def verify_password(self, password):
        """Compares stored password to password at login
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def create_token(user_id):
        """Creates the access token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm='HS256'
            )

            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the token passed in the header
        """
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(token, key)
            return payload["sub"]

        except jwt.ExpiredSignatureError:
            return "Token has expired, Login to generate a new one."

        except jwt.InvalidTokenError:
            return "Token is invalid, Sign up or Login"


class Question(Base):
    """Creates a model for the Question
    """

    __tablename__ = "questions"

    title = db.Column(db.String(255))
    asked_by = db.Column(db.Integer, db.ForeignKey(User.id))
    answers = db.relationship('Answer', order_by="Answer.id",
                              backref="questions",
                              cascade="all,delete-orphan")
    translations = db.relationship("QuestionsTranslation", order_by="QuestionsTranslation.id",
                                   backref="questions",
                                   cascade="all,delete-orphan")

    def __init__(self, title, asked_by):
        self.title = title
        self.asked_by = asked_by


class QuestionsTranslation(Base):
    """Stores different translations
    """
    __tablename__ = "translations"

    language = db.Column(db.String(20))
    translated_title = db.Column(db.String(255))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))

    def __init__(self, language, translated_title, question_id):
        self.language = language
        self.translated_title = translated_title
        self.question_id = question_id


class Answer(Base):

    __tablename__ = "answers"

    answer_body = db.Column(db.String(255))
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))

    def __init__(self, answer_body, question_id):
        self.answer_body = answer_body
        self.question_id = question_id



