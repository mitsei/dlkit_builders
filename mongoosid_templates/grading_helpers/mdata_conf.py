"""Mongo osid metadata configurations for grading service."""


from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data('DEFAULT'))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data('DEFAULT'))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data('DEFAULT'))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data('DEFAULT'))


GRADE_OUTPUT_SCORE = {
    'element_label': 'output score',
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

GRADE_GRADE_SYSTEM = {
    'element_label': 'grade system',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

GRADE_INPUT_SCORE_END_RANGE = {
    'element_label': 'input score end range',
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

GRADE_INPUT_SCORE_START_RANGE = {
    'element_label': 'input score start range',
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


GRADE_SYSTEM_NUMERIC_SCORE_INCREMENT = {
    'element_label': 'numeric score increment',
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

GRADE_SYSTEM_LOWEST_NUMERIC_SCORE = {
    'element_label': 'lowest numeric score',
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

GRADE_SYSTEM_BASED_ON_GRADES = {
    'element_label': 'based on grades',
    'instructions': 'enter either true or false.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'syntax': 'BOOLEAN',
    }

GRADE_SYSTEM_HIGHEST_NUMERIC_SCORE = {
    'element_label': 'highest numeric score',
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


GRADE_ENTRY_RESOURCE = {
    'element_label': 'resource',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

GRADE_ENTRY_GRADE = {
    'element_label': 'grade',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

GRADE_ENTRY_IGNORED_FOR_CALCULATIONS = {
    'element_label': 'ignored for calculations',
    'instructions': 'enter either true or false.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'syntax': 'BOOLEAN',
}

GRADE_ENTRY_SCORE = {
    'element_label': 'score',
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

GRADE_ENTRY_GRADEBOOK_COLUMN = {
    'element_label': 'gradebook column',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}


GRADEBOOK_COLUMN_GRADE_SYSTEM = {
    'element_label': 'grade system',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}


GRADEBOOK_COLUMN_SUMMARY_GRADEBOOK_COLUMN = {
    'element_label': 'gradebook column',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}




