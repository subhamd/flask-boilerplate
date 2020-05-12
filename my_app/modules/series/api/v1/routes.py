from flask import Blueprint, request
from requests import codes as http_status_codes

from my_app.constants import Constants
from my_app.decorators import generate_response, validate_api_request_json
from my_app.models import jsonify_models
from my_app.modules.service_factory import service_factory

bp = Blueprint('series', __name__)
series_service = service_factory.get_service(Constants.SERIES_SERVICE)


@bp.route('', methods=['POST'])
@generate_response()
@validate_api_request_json()
def add_series():
    request_data = request.get_json()  # get data attribute as JSON
    series = series_service.add_series(request_data)
    return jsonify_models(series), http_status_codes.CREATED


@bp.route('', methods=['GET'])
@generate_response()
def get_series():
    # Query params in path can be fetched by the following way
    query_params = request.args
    series_name = query_params.get('name')

    if series_name:
        series = series_service.get_series_by_name(series_name)
    else:
        series = series_service.get_all_series()

    return jsonify_models(series), http_status_codes.OK


@bp.route('/<int:series_id>', methods=['GET'])
@generate_response()
def get_series_by_id(series_id):
    series = series_service.get_series_by_id(series_id)
    return jsonify_models(series), http_status_codes.OK


@bp.route('/<int:series_id>', methods=['DELETE'])
@generate_response()
def delete_series_by_id(series_id):
    series_service.delete_series_by_id(series_id)
    return None, http_status_codes.OK


@bp.route('/<int:series_id>', methods=['PUT'])
@generate_response()
@validate_api_request_json()
def update_series_by_id(series_id):
    request_data = request.get_json()
    series = series_service.update_series(series_id, request_data)
    return jsonify_models(series), http_status_codes.OK

