from api.app import db


class User(db.model):
    """Creates a user model
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    questions = db.relationship('Question', order_by="Question.id", cascade="all, delete-orphan")


class Question(db.Model):
    """Creates a model for the Question
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    asked_by = db.Column(db.Integer, db.ForeignKey(User.id))
    answers = db.relationship('Answer', order_by="Answer.id", cascade="all, delete-orphan")


class Answer(db.Model):

    __tablename__ = "answers"

    id = db.Column(db.Integer, primary=True)
    answer_body = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    question_id = db.column(db.Integer, db.ForeignKey(Question.id))