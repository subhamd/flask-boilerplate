import urllib.parse

import requests
from requests import RequestException, Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from my_app.exceptions.custom_exception import APICallingException, UnsupportedOperationException


def make_api_call(url, method='GET', params=None, data=None, headers=None, timeout=None):
    try:
        if method == 'GET':
            response = requests.get(
                url, params=params, data=data, headers=headers, timeout=timeout)
        elif method == 'POST':
            response = requests.post(
                url, params=params, data=data, headers=headers, timeout=timeout)
        else:
            raise UnsupportedOperationException(
                'method: {method} is not supported'.format(method=method))
    except RequestException as e:
        url = urllib.parse.quote(url)
        raise APICallingException(f'RequestException while performing {method} on URL: {url}') from e
    return response


def make_api_call_in_session(url, session: Session, method='GET', params=None, data=None, headers=None, timeout=None):
    try:
        if method in ['GET', 'POST', 'PUT']:
            response = session.request(
                method, url, params=params, data=data, headers=headers, timeout=timeout)
        else:
            raise UnsupportedOperationException(
                'method: {method} is not supported'.format(method=method))
    except RequestException as e:
        url = urllib.parse.quote(url)
        raise APICallingException(f'RequestException while performing {method} on URL: {url}') from e

    return response


def retry_session(retry_count, session=None, backoff_factor=0.1, status_forcelist=(500, 502, 503, 504)):
    """
    :param retry_count:
    :param session:
    :param backoff_factor:
    :param status_forcelist:
    :return:
    """
    session = session or requests.Session()
    retry = Retry(
        total=retry_count,
        read=retry_count,
        connect=retry_count,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session