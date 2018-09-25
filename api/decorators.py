from functools import wraps

from flask import request, jsonify, make_response

from database.models import User


def requires_authentication(func):
    @wraps(func)
    def auth_wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")
        if header:
            access_token = header.split(" ")[1]
            if access_token:
                user_id = User.decode_token(access_token)

                if isinstance(user_id, str):
                    response = {
                        "message": user_id
                    }

                    return make_response(jsonify(response)), 401

                else:
                    return func(user_id, *args, **kwargs)

            else:
                response = {
                    "message": "Register or login to access this resource"
                }

                return make_response(jsonify(response)), 401

        else:
            response = {
                "message": "Register or login to access this resource"
            }

            return make_response(jsonify(response)), 401

    return auth_wrapper

