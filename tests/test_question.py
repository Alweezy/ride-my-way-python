import json
from .base import BaseTest


class QuestionTestCases(BaseTest):
    """Test cases for questions
    """
    def test_create_question(self):
        """Test for posting a question successfully
        """
        self.token = self.user_credentials()
        results = self.client().post("/api/v1/questions",
                                     data=self.question,
                                     headers={"Authorization": "Bearer " + self.token},
                                     content_type="application/json")
        self.assertEqual(results.status_code, 201)

    def test_get_all_questions(self):
        """Test for fetching all questions successfully """

        self.token = self.user_credentials()
        results = self.client().post("/api/v1/questions",
                                     data=self.question,
                                     headers={"Authorization": "Bearer " + self.token},
                                     content_type="application/json")
        self.assertEqual(results.status_code, 201)
        retrieve = self.client().get("/api/v1/questions",
                                     data=json.dumps(self.question),
                                     headers={"Authorization": "Bearer " + self.token},
                                     content_type="application/json")

        self.assertEqual(retrieve.status_code, 200)
        self.assertIn("Which instance is this?", json.loads(retrieve.data)[0]['title'])

    # def test_get_question_by_id(self):
    #     """Test for getting a particular question by id
    #     """
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions/",
    #                                  data=json.dumps(self.question),
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #     results_json = json.loads(
    #         results.data.decode("utf-8").replace(" ", "\""))
    #     retrieve = self.client().get("/api/v1/questions/{}/".format(results_json["id"]))
    #
    #     self.assertEqual(retrieve.status_code, 200)
    #     self.assertIn("Which instance is this?", str(retrieve.data))

    # def test_edit_question(self):
    #     """Test for the successful update of a question with an id
    #     """
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions",
    #                                  data=json.dumps(self.question),
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #
    #     updates = self.client().put("/api/v1/questions/1",
    #                                 data={"title": "Is this the same question?"},
    #                                 headers={"Authorization": "Bearer " + self.token},
    #                                 content_type="application/json")
    #
    #     self.assertEqual(updates.status_code, 202)
    #     self.assertIn("Is this the same question?", str(updates.data))

    def test_delete_question(self):
        self.token = self.user_credentials()
        results = self.client().post("/api/v1/questions",
                                     data=self.question,
                                     headers={"Authorization": "Bearer " + self.token},
                                     content_type="application/json")
        self.assertEqual(results.status_code, 201)

        deletes = self.client().delete("/api/v1/questions/1",
                                       headers={"Authorization": "Bearer " + self.token})
        self.assertEqual(deletes.status_code, 200)

    # def test_create_question_no_auth(self):
    #     results = self.client().post("/api/v1/questions",
    #                                  data=self.question,
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 401)
    #     self.assertIn("Register or login to access this resource",
    #                   str(results.data))

    # def test_test_edit_question_no_auth(self):
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions",
    #                                  data=json.dumps(self.question),
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #
    #     updates = self.client().put("/api/v1/questions/1",
    #                                 data={"title": "Is this the same question?"},
    #                                 content_type="application/json")
    #
    #     self.assertEqual(updates.status_code, 401)
    #     self.assertIn("Register or login to access this resource",
    #                   str(results.data))
    #
    # def test_delete_question_no_auth(self):
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions",
    #                                  data=self.question,
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #     deletes = self.client().delete("/api/v1/questions/1")
    #
    #     self.assertEqual(deletes.status_code, 401)
    #     self.assertIn("Register or login to access this resource",
    #                   str(results.data))

    # def test_edit_question_different_user(self):
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions",
    #                                  data=json.dumps(self.question),
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #
    #     self.reg_result = self.client().post("/auth/register",
    #                                          data=self.user,
    #                                          content_type="application/json")
    #     self.sign_in_result = self.client().post("auth/login",
    #                                              data=self.new_user,
    #                                              content_type="application/json")
    #
    #     self.new_token = json.loads(self.sign_in_result.data.decode())["access_token"]
    #
    #     updates = self.client().put("/api/v1/questions/1",
    #                                 data={"title": "Is this the same question?"},
    #                                 headers={"Authorization": "Bearer " + self.new_token},
    #                                 content_type="application/json")
    #
    #     self.assertEqual(updates.status_code, 401)
    #     self.assertIn("You can only edit your content", str(updates.data))
    #
    # def test_delete_question_different_user(self):
    #     self.token = self.user_credentials()
    #     results = self.client().post("/api/v1/questions",
    #                                  data=json.dumps(self.question),
    #                                  headers={"Authorization": "Bearer " + self.token},
    #                                  content_type="application/json")
    #     self.assertEqual(results.status_code, 201)
    #
    #     self.reg_result = self.client().post("/auth/register",
    #                                          data=self.user,
    #                                          content_type="application/json")
    #     self.sign_in_result = self.client().post("auth/login",
    #                                              data=self.new_user,
    #                                              content_type="application/json")
    #
    #     self.new_token = json.loads(self.sign_in_result.data.decode())["access_token"]
    #
    #     deletes = self.client().delete("/api/v1/questions/1",
    #                                    data={"title": "Is this the same question?"},
    #                                    headers={"Authorization": "Bearer " + self.new_token},
    #                                    content_type="application/json")
    #
    #     self.assertEqual(deletes.status_code, 401)
    #     self.assertIn("You can only edit your content", str(deletes.data))
