from functools import wraps

from flask import make_response, request, current_app
from flask.json import jsonify
from requests import codes as http_status_codes
from werkzeug.exceptions import BadRequest

from my_app.constants import Constants
from my_app.extensions import begin_transaction, commit_transaction, rollback_transaction, db
from my_app.exceptions.custom_exception import InvalidRequestException


def transactional():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                begin_transaction()
                response = func(*args, **kwargs)
                commit_transaction()
                return response
            except Exception as e:
                rollback_transaction()
                raise e

        return wrapper

    return decorator


def generate_response():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data, status_code = func(*args, **kwargs)
            status_code = status_code if status_code else http_status_codes.OK

            response = {
                'status': Constants.STATUS_SUCCESS,
                'data': data,
                'error': None,
                'extra_data': None
            }

            return make_response(jsonify(response), status_code)

        return wrapper

    return decorator


def validate_api_request_json():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request.get_json()
            except BadRequest as e:
                raise InvalidRequestException('Malformed JSON in request body')

            return func(*args, **kwargs)

        return wrapper
    return decorator


def add_app_context_if_not_available():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_app:
                with db.app.app_context():
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
    return decorator
