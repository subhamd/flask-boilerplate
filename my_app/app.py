import logging
import os
import socket
import uuid

from flask.logging import default_handler
from flask_cors import CORS
from flask_log_request_id import RequestIDLogFilter, RequestID, current_request_id
from requests import codes as http_status_codes

from my_app import settings
from my_app.modules.series.api.v1.routes import bp as series_bp
from my_app.config import Config
from my_app.constants import Constants
from my_app.exceptions import error_codes
from my_app.exceptions.custom_exception import CustomException, URLNotFoundException
from my_app.extensions import db
from flask import current_app, Flask, jsonify


class MachineInfoLogFilter(logging.Filter):
    """
    class: Machine info log
    """

    def filter(self, log_record):
        """
        append machine ip and env
        """
        log_record.machine_ip = socket.gethostname()
        log_record.env = os.getenv('ENV', 'dev')
        return log_record


def configure_logging(flask_app):
    """
    logging configuration
    """
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            ('%(asctime)s [%(levelname)s] %(machine_ip)s %(env)s '
             '%(request_id)s %(name)s %(funcName)s:%(lineno)d %(message)s')
        )
    )
    handler.setLevel(getattr(logging, flask_app.config["LOG_LEVEL"]))
    handler.addFilter(RequestIDLogFilter())
    handler.addFilter(MachineInfoLogFilter())

    flask_app.logger.removeHandler(default_handler)
    flask_app.logger.addHandler(handler)


def register_extensions(flask_app):
    """
    Register extensions
    """
    db.init_app(flask_app)


def register_blueprints(flask_app):
    """
    Register blueprint
    """
    flask_app.register_blueprint(series_bp, url_prefix="/sports-ops/api/v1/series")


def create_app():
    """
    flask app creation method
    """
    environment = os.getenv('ENV', 'dev')

    flask_app = Flask(__name__)
    RequestID(flask_app, request_id_generator=lambda: 'event_rid%s' % uuid.uuid4().hex)
    flask_app.config.from_object(Config)

    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = (
        settings.POSTGRES_URI
    )

    if environment.upper() == 'LOCAL':
        flask_app.config['SQLALCHEMY_ECHO'] = True

    # register extensions
    register_extensions(flask_app)

    # register blueprints
    register_blueprints(flask_app)

    # configure logging
    configure_logging(flask_app)

    # enable cors
    CORS(flask_app)

    return flask_app


app = create_app()


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    health check
    """
    return 'OK', 200


@app.after_request
def append_request_id(response):
    """
    post process append request id
    """
    response.headers.add('X-REQUEST-ID', current_request_id())
    return response


@app.errorhandler(http_status_codes.NOT_FOUND)
def handle_page_not_found(e):
    ex = URLNotFoundException()
    return _generate_response_for_exception(ex)


@app.errorhandler(CustomException)
def handle_custom_exception(e):
    response = _generate_response_for_exception(e)
    current_app.logger.error(f'SportsOpsException raised | {response.json["error"]}')
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.error('Exception raised', exc_info=e)

    se = CustomException(error_code=error_codes.DEFAULT_ERROR)
    extra_data = {'developer_message': e.__str__()}
    return _generate_response_for_exception(se, extra_data)


def _generate_response_for_exception(ex, extra_data=None):
    response = jsonify(
        {
            'status': Constants.STATUS_ERROR,
            'data': None,
            'error': {
                'err_code': ex.err_code,
                'err_str': ex.err_str,
                'err_msg': (ex.developer_message if isinstance(ex.developer_message, str) else
                            ex.developer_message.__str__()) if ex.developer_message else ex.err_msg
            },
            'extra_data': extra_data
        }
    )
    response.status_code = ex.status_code
    return response
