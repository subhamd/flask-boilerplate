def get(key):
    return __code.get(key, __code[DEFAULT_ERROR])


__code = dict()

DEFAULT_ERROR = 10000
__code[DEFAULT_ERROR] = {
    'code': DEFAULT_ERROR,
    'str': 'E_INTERNAL_ERROR',
    'msg': 'Oops! Something went wrong. Please retry after sometime'
}

###########################
# Some sample Error codes #
###########################

SERVICE_NOT_FOUND = 10001
__code[SERVICE_NOT_FOUND] = {
    'code': SERVICE_NOT_FOUND,
    'str': 'E_SERVICE_NOT_FOUND',
    'msg': 'Service not found'
}

INVALID_REQUEST = 10002
__code[INVALID_REQUEST] = {
    'code': INVALID_REQUEST,
    'str': 'E_INVALID_REQUEST',
    'msg': 'Invalid request'
}

KEYS_NOT_PRESENT = 10003
__code[KEYS_NOT_PRESENT] = {
    'code': KEYS_NOT_PRESENT,
    'str': 'E_KEYS_NOT_PRESENT',
    'msg': 'Keys not present'
}

EXCEPTION_IN_API_CALL = 10004
__code[EXCEPTION_IN_API_CALL] = {
    'code': EXCEPTION_IN_API_CALL,
    'str': 'E_EXCEPTION_IN_API_CALL',
    'msg': 'Exception in API call'
}

UNSUPPORTED_OPERATION = 10005
__code[UNSUPPORTED_OPERATION] = {
    'code': UNSUPPORTED_OPERATION,
    'str': 'E_UNSUPPORTED_OPERATION',
    'msg': 'Unsupported operation'
}

URL_NOT_FOUND = 10006
__code[URL_NOT_FOUND] = {
    'code': URL_NOT_FOUND,
    'str': 'E_URL_NOT_FOUND',
    'msg': 'The requested URL was not found on the server'
}

# Error codes for error raised while performing a DB operation
# Notice that error codes starts from a different series (20000)
RECORD_NOT_FOUND_IN_DB_ERROR = 20000
__code[RECORD_NOT_FOUND_IN_DB_ERROR] = {
    'code': RECORD_NOT_FOUND_IN_DB_ERROR,
    'str': 'E_RECORD_NOT_FOUND_IN_DB_ERROR',
    'msg': 'Record not found in database'
}

RECORD_ALREADY_EXIST_IN_DB_ERROR = 20001
__code[RECORD_ALREADY_EXIST_IN_DB_ERROR] = {
    'code': RECORD_ALREADY_EXIST_IN_DB_ERROR,
    'str': 'E_RECORD_ALREADY_EXIST_IN_DB_ERROR',
    'msg': 'Record already exists in database'
}

# Error codes for error raised while performing an operation in Redis cache
# Notice that error codes starts from a different series (30000)
FAILED_TO_SAVE_IN_CACHE = 30000
__code[FAILED_TO_SAVE_IN_CACHE] = {
    'code': FAILED_TO_SAVE_IN_CACHE,
    'str': 'E_FAILED_TO_SAVE_IN_CACHE',
    'msg': 'Error while saving in Cache'
}

FAILED_TO_FETCH_FROM_CACHE = 30001
__code[FAILED_TO_FETCH_FROM_CACHE] = {
    'code': FAILED_TO_FETCH_FROM_CACHE,
    'str': 'E_FAILED_TO_FETCH_FROM_CACHE',
    'msg': 'Error while fetching from Cache'
}

FAILED_TO_DELETE_FROM_CACHE = 30002
__code[FAILED_TO_DELETE_FROM_CACHE] = {
    'code': FAILED_TO_DELETE_FROM_CACHE,
    'str': 'E_FAILED_TO_DELETE_FROM_CACHE',
    'msg': 'Error while deleting from Cache'
}

