import os
from datetime import datetime, timedelta

import jwt
from flask_bcrypt import Bcrypt
from flask import current_app

from api.app import db


class User(db.Model):
    """Creates a user model
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    questions = db.relationship('Question', order_by="Question.id",
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
                os.getenv("SECRET_KEY"),
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
            key = current_app.config("SECRET_KEY")
            payload = jwt.decode(token, key)
            return payload["sub"]

        except jwt.ExpiredSignatureError:
            return "Token has expired, Login to generate a new one."

        except jwt.InvalidTokenError:
            return "Token is invalid, Sign up or Login"

    def save(self):
        """Save a user into the database
        """
        db.session.add(self)
        db.session.commit()


class Question(db.Model):
    """Creates a model for the Question
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    asked_by = db.Column(db.Integer, db.ForeignKey(User.id))
    answers = db.relationship('Answer', order_by="Answer.id", cascade="all,delete-orphan")

    def __init__(self, title, asked_by):
        self.title = title
        self.asked_by = asked_by

    def save(self):
        """Save a question to the database
        """
        db.session.add(self)
        db.session.commit()


class Answer(db.Model):

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    answer_body = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    question_id = db.Column(db.Integer, db.ForeignKey(Question.id))

    def __init__(self, answer_body, question_id):
        self.answer_body = answer_body
        self.question_id = question_id

    def save(self):
        """Add an answer to a question
        """
        db.session(self)
        db.session.commit()
