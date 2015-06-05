"""mongo utilities.py"""
from .osid.osid_errors import NullArgument


def arguments_not_none(func):
    """decorator, to check if any arguments are None; raise exception if so"""
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise NullArgument()
        for arg, val in kwargs.iteritems():
            if val is None:
                raise NullArgument()
        try:
            return func(*args, **kwargs)
        except TypeError as ex:
            if 'takes exactly' in ex.args[0]:
                raise NullArgument('Not all arguments provided: ' + str(ex.args[0]))
            else:
                raise TypeError(ex.args[0])

    return wrapper