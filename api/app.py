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

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
