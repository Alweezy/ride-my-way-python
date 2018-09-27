from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, make_response

from instance.config import app_config

# initializing SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    from database.models import Question, QuestionsTranslation
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
                    "title": question.title,
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

    @app.route("/api/v1/translations", methods=["GET", "POST"])
    @requires_authentication
    def translations(*args, **kwargs):
        """Method to access translations
        """
        translated_title = [translation.translated_title for translation in QuestionsTranslation.query.all()]
        if request.method == "POST":
            data = request.data
            if data["translated_title"] in translated_title:
                response = {
                    "message": "Translation already exists"
                }

                return make_response(jsonify(response)), 409
            else:
                translation = QuestionsTranslation(translated_title=data["translated_title"],
                                                   language=data["language"],
                                                   question_id=data["question_id"])
                translation.save()
                translated_response = {
                    "translation_id": translation.id,
                    "question_id": translation.question_id,
                    "translated_title": translation.translated_title
                }

                return make_response(jsonify(translated_response)), 201

        else:
            try:
                question_translations = QuestionsTranslation.query.all()
                translations_list = []
                for question_translation in question_translations:
                    translated_response = {
                        "translation_id": question_translation.id,
                        "question_id": question_translation.question_id,
                        "translated_title": question_translation.translated_title,
                        "language": question_translation.language
                    }

                    translations_list.append(translated_response)

                return make_response(jsonify(translations_list)), 200
            except Exception as e:
                response = {
                    "message": str(e)
                }
                make_response(jsonify(response)), 500

    @app.route("/api/v1/translations/<int:question_id>", methods=["PUT", "GET", "DELETE", "PATCH"])
    @requires_authentication
    def translation_manipulations(id, question_id, *args, **kwargs):
        """Manipulate the translations.
        """
        target_translation = QuestionsTranslation.query.filter_by(question_id=question_id).first()
        if target_translation:
            if request.method == "DELETE":
                target_translation.delete()
                response = {
                    "message": "Translation deleted successfully"
                }

                return make_response(jsonify(response)), 200
            elif request.method == "GET":
                response = {
                    "translation_id": target_translation.id,
                    "translation_title": target_translation.translated_title,
                    "language": target_translation.language,
                    "question_id": target_translation.question_id
                }
                return make_response(jsonify(response)), 200
            else:
                data = request.data
                translation = QuestionsTranslation(translated_title=data["translated_title"],
                                                   language=data["language"],
                                                   question_id=data["question_id"])
                translation.save()
                translated_response = {
                    "translation_id": translation.id,
                    "question_id": translation.question_id,
                    "translated_title": translation.translated_title,
                    "language": translation.language
                }

                return make_response(jsonify(translated_response)), 202
        else:
            response = {
                "message": "The translation with that id does not exist"
            }
            return make_response(jsonify(response)), 404

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
