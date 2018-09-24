from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request, make_response

from instance.config import app_config

# initializing SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    from database.models import User, Question, Answer

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False

    db.init_app(app)

    @app.route("/api/v1/questions/", methods=["POST"])
    def get_questions():
        if request.method == "POST":
            title = str(request.data.get("title", ""))
            asked_by = request.data.get("user_id")
            question = Question(title=title, asked_by=asked_by)
            question.save()
            # all_questions = [question.name for question in
            #                  Question.query.filter_by(created_by=user_id)]
            response = jsonify({
                "id": question.id,
                "title": question.title,
                "date_created": question.date_created,
                "date_modified": question.date_modified,
                "asked_by": question.asked_by
            })
            return make_response(response), 201

    @app.route("/api/v1/users", methods=["POST"])
    def create_users():
        username = str(request.data.get("username"))
        email = str(request.data.get("email"))
        password = str(request.data.get("password"))
        user = User(username=username, email=email, password=password)
        user.save()
        return make_response(jsonify({"message": "user created"})), 201

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
