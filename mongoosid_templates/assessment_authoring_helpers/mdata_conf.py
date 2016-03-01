"""Mongo osid metadata configurations for assessment.authoring service."""

from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data("DEFAULT"))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data("DEFAULT"))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data("DEFAULT"))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data("DEFAULT"))



ASSESSMENT_PART_ASSESSMENT_PART = {
    'element_label': 'assessment part',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

ASSESSMENT_PART_ASSESSMENT = {
    'element_label': 'assessment',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}


ASSESSMENT_PART_ALLOCATED_TIME = {
    'element_label': 'allocated time',
    'instructions': 'enter a valid duration object.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_duration_values': [None],
    'syntax': 'DURATION',
    'date_time_set': [],
}




SEQUENCE_RULE_NEXT_ASSESSMENT_PART = {
    'element_label': 'next assessment part',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

SEQUENCE_RULE_CUMULATIVE = {
    'element_label': 'cumulative',
    'instructions': 'enter either true or false.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'syntax': 'BOOLEAN',
}

SEQUENCE_RULE_ASSESSMENT_PART = {
    'element_label': 'assessment part',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}




