from redis import RedisError

from my_app.exceptions.custom_exception import (
    FetchingFromCacheFailed, DeletingFromCacheFailed, SavingInCacheFailed
)
from my_app.extensions import redis_client


def save_in_cache(key, value, invalidate_seconds=None,
                  set_only_if_new=False, set_only_if_exist=False):
    """
    Save in cache
    :param key: Key
    :param value: Value
    :param invalidate_seconds: Optional
    :param set_only_if_new: Optional. If set to True, set the value at key
    ``key`` to ``value`` only if it does not exist.
    :param set_only_if_exist: Optional. if set to True, set the value at key
    ``key`` to ``value`` only if it already exists.
    :return: True|None
    """
    try:
        return redis_client.set(
            name=key,
            value=value,
            ex=invalidate_seconds,
            nx=set_only_if_new,
            xx=set_only_if_exist
        )
    except RedisError as e:
        raise SavingInCacheFailed('') from e


def get_from_cache(key):
    """
    Returns the value at ``key``, or None if the key doesn't exist
    :param key: key
    :return: Value|None
    """
    try:
        return redis_client.get(key)
    except RedisError as e:
        raise FetchingFromCacheFailed('') from e


def delete_from_cache(key_name):
    """
    Delete key specified by ``key_name``
    :param key_name:
    :return:
    """
    try:
        return redis_client.delete(key_name)
    except RedisError as e:
        raise DeletingFromCacheFailed('') from e
