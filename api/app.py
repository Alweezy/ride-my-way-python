from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy


from instance.config import app_config

# initializing SQLAlchemy
db = SQLAlchemy()


def create_app(config_name):
    from database.models import User, Question, Answer
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    return app