"""mongo utilities.py"""
from .osid.osid_errors import NullArgument


def arguments_not_none(func):
    """decorator, to check if any arguments are None; raise exception if so"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise NullArgument()
        for arg, val in kwargs:
            if val is None:
                raise NullArgument()
        return func(*args, **kwargs)

    return wrapper