
from my_app.exceptions.custom_exception import KeysNotPresentException, InvalidRequestException

countries = None


def validate_required_keys(dict_object, required_keys):
    """
    validate required keys
    """
    if dict_object is None:
        dict_object = {}

    missing_keys = set(required_keys) - set(dict_object.keys())
    if missing_keys:
        raise KeysNotPresentException('keys: {missing_keys} not present'.format
                                      (missing_keys=', '.join(missing_keys)))


def validate_for_null_and_empty(dict_object, keys):
    """
    validate for null and empty values of keys
    :param dict_object:
    :param keys:
    :return:
    """
    for key in keys:
        value = dict_object.get(key)

        if value and isinstance(value, str):
            value = value.strip()

        if value is None or value == '':
            raise InvalidRequestException(f'The value for key `{key}` is mandatory')
