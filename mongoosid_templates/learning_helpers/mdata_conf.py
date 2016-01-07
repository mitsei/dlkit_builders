"""Mongo osid metadata configurations for grading service."""


from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data('DEFAULT'))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data('DEFAULT'))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data('DEFAULT'))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data('DEFAULT'))

PROFICIENCY_LEVEL = {
    'element_label': 'level',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

PROFICIENCY_COMPLETION = {
    'element_label': 'percentage complete',
    'instructions': 'enter a decimal value.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_decimal_values': [None],
    'syntax': 'DECIMAL',
    'decimal_scale': None,
    'minimum_decimal': None,
    'maximum_decimal': None,
    'decimal_set': [],
}