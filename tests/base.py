import unittest
import json

from api.app import create_app, db


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.question = json.dumps(dict({"title": "Which instance is this?"}))
        self.user = json.dumps(dict({"username": "alvin",
                                     "email": "me@example.com",
                                     "password": "password"}))

        self.new_user = json.dumps(dict({"username": "alex",
                                        "email": "alex@example.com",
                                         "password": "password"}))

        # binding app to the current context
        with self.app.app_context():
            db.create_all()

    def user_credentials(self):
        self.sign_up_result = self.client().post("/auth/register",
                                                 data=self.user,
                                                 content_type="application/json")
        self.login_result = self.client().post("auth/login",
                                               data=self.user,
                                               content_type="application/json")

        self.access_token = json.loads(self.login_result.data.decode())

        return self.access_token["access_token"]

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
