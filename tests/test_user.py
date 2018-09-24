import json
from .base import BaseTest


class UserTestCases(BaseTest):
    """Test cases for user
    """

    def test_register_user_successful(self):
        """Test for the signup of a new user
        """
        result = self.client().post("/auth/register", data=self.user, content_type="application/json")
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "Registration successful")
        self.assertEqual(result.status_code, 201)

    def test_double_registration(self):
        """Test against registering an existent user
        """
        result = self.client().post("/auth/register", data=self.user, content_type="application/json")
        self.assertEqual(result.status_code, 201)

        new_result = self.client().post("/auth/register", data=self.user, content_type="application/json")
        self.assertEqual(new_result.status_code, 409)
        data = json.loads(new_result.data.decode())
        self.assertEqual(data["message"], "User already exists")

    def test_registration_missing_username(self):
        """Test against registration of a user with no username
        """
        no_username = json.dumps(dict({"username": "",
                                       "email": "me@example.com",
                                       "password": "password"}))
        result = self.client().post("/auth/register", data=no_username, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "The username or password cannot be empty")

    def test_registration_missing_password(self):
        """Test against registration of a user with no username
        """
        no_password = json.dumps(dict({"username": "alvin",
                                       "email": "me@example.com",
                                       "password": ""}))
        result = self.client().post("/auth/register", data=no_password, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "The username or password cannot be empty")

    def test_user_login_successful(self):
        """Test for successful sign in of a registered user
        """
        reg_result = self.client().post("/auth/register", data=self.user, content_type="application/json")
        self.assertEqual(reg_result.status_code, 201)
        login_result = self.client().post("/auth/login", data=self.user, content_type="application/json")
        self.assertEqual(login_result.status_code, 200)
        data = json.loads(login_result.data.decode())
        self.assertEqual(data["message"], "Login successful")

    def test_login_foreign_user(self):
        """Test against login of an unregistered user
        """
        foreign_user = json.dumps(dict({"username": "alex",
                                       "email": "me@example.com",
                                        "password": "new_password"}))

        result = self.client().post("/auth/login", data=foreign_user, content_type="application/json")
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "user not available, register user first")

    def test_login_no_password(self):
        """Test against sign in with no password
        """
        no_password = json.dumps(dict({"username": "alvin",
                                       "email": "me@example.com",
                                       "password": ""}))
        result = self.client().post("/auth/login", data=no_password, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "The password or username cannot be empty")

    def test_login_no_username(self):
        """Test against sign in with no username
        """
        no_password = json.dumps(dict({"username": "",
                                       "email": "me@example.com",
                                       "password": "password"}))
        result = self.client().post("/auth/login", data=no_password, content_type="application/json")
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data.decode())
        self.assertEqual(data["message"], "The password or username cannot be empty")