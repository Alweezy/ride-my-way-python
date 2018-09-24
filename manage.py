import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api.app import create_app, db


env = os.getenv("ENV")

app = create_app(config_name=env)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)


@manager.command
def create_db():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    manager.run()
    db.create_all()