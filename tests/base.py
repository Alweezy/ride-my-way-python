import unittest
import json

from api.app import create_app, db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.question = json.dumps(dict({"title": "Which instance is this?",
                                         "user_id": 1}))
        self.user = json.dumps(dict({"username": "alvin",
                                     "email": "me@example.com",
                                     "password": "password"}))

        # binding app to the current context
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()