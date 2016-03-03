"""Mongo osid metadata configurations for logging service."""

import datetime

from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data('DEFAULT'))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data('DEFAULT'))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data('DEFAULT'))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data('DEFAULT'))

DEFAULT_DATETIME = {
    'year': datetime.datetime.min.year,
    'month': datetime.datetime.min.month,
    'day': datetime.datetime.min.day,
    'hour': datetime.datetime.min.hour,
    'minute': datetime.datetime.min.minute,
    'second': datetime.datetime.min.second,
    'microsecond': datetime.datetime.min.microsecond,
}

LOG_ENTRY_PRIORITY = {
    'element_label': 'logging priority type',
    'instructions': 'accepts an osid.type.Type object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_type_values': [str(DEFAULT_GENUS_TYPE)],
    'syntax': 'TYPE',
    'type_set': [],
}

LOG_ENTRY_TIMESTAMP = {
    'element_label': 'Log Entry Timestamp',
    'instructions': 'enter a valid datetime object.',
    'required': True,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_date_time_values': [DEFAULT_DATETIME],
    'syntax': 'DATETIME',
    'date_time_set': [],
}

LOG_ENTRY_AGENT = {
    'element_label': 'agent',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}