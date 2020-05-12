import json

from requests import codes as http_status_codes

from my_app.exceptions import error_codes


class CustomException(Exception):
    def __init__(self, error_code, developer_message=None, *args, **kwargs):
        error = error_codes.get(error_code)
        self.err_msg = error.get('msg')
        self.err_code = error.get('code')
        self.err_str = error.get('str')
        self.developer_message = developer_message
        self.status_code = http_status_codes.INTERNAL_SERVER_ERROR

        error_obj_str = json.dumps({
            'err_code': self.err_code,
            'err_str': self.err_str,
            'err_msg': (self.developer_message if isinstance(self.developer_message, str) else
                        self.developer_message.__str__()) if self.developer_message else self.err_msg
        })
        super(CustomException, self).__init__(error_obj_str, *args)

    def to_dict(self):
        """
        return json object
        """
        return {
            'err_code': self.err_code,
            'err_str': self.err_str,
            'err_msg': self.err_msg,
            'developer_message': self.developer_message,
            'http_status_code': self.status_code
        }


################################
# Some sample Custom exception #
################################

class ServiceNotFoundException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(ServiceNotFoundException, self).__init__(
            error_codes.SERVICE_NOT_FOUND, developer_message, *args, **kwargs)


class InvalidRequestException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(InvalidRequestException, self).__init__(
            error_codes.INVALID_REQUEST, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class KeysNotPresentException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(KeysNotPresentException, self).__init__(
            error_codes.KEYS_NOT_PRESENT, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class APICallingException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(APICallingException, self).__init__(
            error_codes.EXCEPTION_IN_API_CALL, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class UnsupportedOperationException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(UnsupportedOperationException, self).__init__(
            error_codes.UNSUPPORTED_OPERATION, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class URLNotFoundException(CustomException):
    def __init__(self, developer_message=None, *args, **kwargs):
        super(URLNotFoundException, self).__init__(error_codes.URL_NOT_FOUND, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.NOT_FOUND


class RecordNotFoundInDBException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(RecordNotFoundInDBException, self).__init__(
            error_codes.RECORD_NOT_FOUND_IN_DB_ERROR, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class RecordAlreadyExistInDBException(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(RecordAlreadyExistInDBException, self).__init__(
            error_codes.RECORD_ALREADY_EXIST_IN_DB_ERROR, developer_message, *args, **kwargs)
        self.status_code = http_status_codes.BAD_REQUEST


class SavingInCacheFailed(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(SavingInCacheFailed, self).__init__(
            error_codes.FAILED_TO_SAVE_IN_CACHE, developer_message, *args, **kwargs)


class FetchingFromCacheFailed(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(FetchingFromCacheFailed, self).__init__(
            error_codes.FAILED_TO_FETCH_FROM_CACHE, developer_message, *args, **kwargs)


class DeletingFromCacheFailed(CustomException):
    def __init__(self, developer_message, *args, **kwargs):
        super(DeletingFromCacheFailed, self).__init__(
            error_codes.FAILED_TO_DELETE_FROM_CACHE, developer_message, *args, **kwargs)
