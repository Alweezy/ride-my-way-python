import re
from flask.views import MethodView
from flask import jsonify, make_response, request

from . import auth_blueprint
from database.models import User


class SignUpView(MethodView):
    """Template for registration of a new user
    """
    def post(self):
        """Method to register a new user
        """
        if request.data["username"].strip(" ") and len(request.data["password"]) >= 8:
            user = User.query.filter_by(
                username=request.data["username"]).first()

            email = User.query.filter_by(
                email=request.data["email"]).first()

            email_regex = re.search(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
                                    request.data["email"])

            if not user and not email and email_regex:
                try:
                    username = request.data["username"]
                    email = request.data["email"]
                    password = request.data["password"]

                    user = User(username=username, email=email, password=password)
                    user.save()

                    response = {
                        "message": "Registration successful"
                    }

                    return make_response(jsonify(response)), 201
                except Exception as e:
                    response = {
                        "message": str(e)
                    }

                    return make_response(jsonify(response)), 401

            elif not user and not email_regex:
                response = {
                    "message": "Invalid email"
                }

                return make_response(jsonify(response)), 400

            elif not user and email:
                response = {
                    "message": "Email is already in use, try a new email address"
                }

                return make_response(jsonify(response)), 400

            else:
                response = {
                    "message": "User already exists"
                }

                return make_response(jsonify(response), 409)
        elif request.data["username"].strip(" ")and 0 < len(request.data["email"]) < 8:
            response = {
                "message": "Email cannot be less than 8 characters"
            }

            return make_response(jsonify(response)), 400

        else:
            response = {
                "message": "The username or password cannot be empty"
            }
            return make_response(jsonify(response)), 400


class SigninView(MethodView):
    """Template for the login of a user
    """
    def post(self):
        """Method to login a signed up user
        """
        try:
            if request.data["username"].strip(" ") and request.data["password"]:
                user = User.query.filter_by(username=request.data["username"]).first()
                password = request.data["password"]
                if user and user.verify_password(password):
                    token = user.create_token(user.id)
                    if token:
                        response = {
                            "access_token": token.decode(),
                            "message": "Login successful"
                        }

                        return make_response(jsonify(response)), 200
                    else:
                        response = {
                            "message": "Invalid username or password"
                        }

                        return make_response(jsonify(response)), 401
                else:
                    response = {
                        "message": "user not available, register user first"
                    }

                    return make_response(jsonify(response), 401)
            else:
                response = {
                    "message": "The password or username cannot be empty"
                }

                return make_response(jsonify(response)), 400

        except Exception as e:
            response = {
                "error": str(e)
            }

            return make_response(jsonify(response)), 500


sign_up_view = SignUpView.as_view("register_view")
sign_in_view = SigninView.as_view("signin_view")

auth_blueprint.add_url_rule("/auth/register", view_func=sign_up_view, methods=["POST"])
auth_blueprint.add_url_rule("/auth/login", view_func=sign_in_view, methods=["POST"])

