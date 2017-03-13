"""mongo utilities.py"""
from .osid.osid_errors import NullArgument


def arguments_not_none(arg_list):
    """check if any arguments are None; raise exception if so"""
    for arg in arg_list:
        if arg is None:
            raise NullArgument()