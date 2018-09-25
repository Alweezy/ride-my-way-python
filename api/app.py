from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, make_response

from instance.config import app_config

# initializing SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    from database.models import User, Question, Answer
    from api.decorators import requires_authentication

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)

    @app.route("/api/v1/questions", methods=["GET", "POST"])
    @requires_authentication
    def questions(user_id, *args, **kwargs):
        """Post a question or get all questions
        """
        if request.method == "POST":
            all_questions = [question.title for question in Question.query.all()]
            title = request.data.get("title", "")
            if title not in all_questions:
                question = Question(title=title, asked_by=user_id)
                question.save()
                response = {
                    "id": question.id,
                    "date_created": question.date_created,
                    "date_modified": question.date_modified,
                    "asked_by": user_id
                }

                return make_response(jsonify(response)), 201
            elif title in all_questions:
                response = {
                    "message": "Question already exists"
                }
                return make_response(jsonify(response)), 409
        elif request.method == "GET":
            all_questions = Question.query.all()
            results = []
            for question in all_questions:

                question_object = {
                    "id": question.id,
                    "title": question.title,
                    "date_created": question.date_created,
                    "date_modified": question.date_modified,
                    "asked_by": question.asked_by
                }

                results.append(question_object)
            return make_response(jsonify(results)), 200

    @requires_authentication
    @app.route("/api/v1/questions/<int:id>", methods=["GET", "PUT", "DELETE"])
    def question_manipulations(id,  *args, **kwargs):
        """Gets, edits and deletes a particular question using the id.
        """
        question = Question.query.filter_by(id=id).first()

        if not question:
            response = {
                "message": "Question not found"
            }
            return make_response(jsonify(response)), 404
        if request.method == "DELETE":
            if question:
                question.delete()
                response = {
                    "message": "Question deleted successfully"
                }

                return make_response(jsonify(response)), 200
            else:
                response = {
                    "message": "You are not the owner of this question"
                }

                return make_response(jsonify(response)), 403

        elif request.method == "PUT":
            all_questions = [question.title for question in Question.query.all()]
            title = request.data.get("title", "")
            if title not in all_questions:
                question.title = title
                question.save()

                question_object = {
                    "id": question.id,
                    "title": question.title,
                    "date_created": question.date_created,
                    "date_modified": question.date_modified,
                    "asked_by": question.asked_by
                }

                return make_response(jsonify(question_object)), 202
            else:
                response = {
                    "message": "A question with this title exists"
                }

                return make_response(jsonify(response)), 409

        else:
            question_object = {
                "id": question.id,
                "title": question.title,
                "date_created": question.date_created,
                "date_modified": question.date_modified,
                "asked_by": question.asked_by
            }

        return make_response(jsonify(question_object)), 200

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
