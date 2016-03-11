"""Mongo osid metadata configurations for assessment service."""

from .. import types
from ..primitives import Type
DEFAULT_LANGUAGE_TYPE = Type(**types.Language().get_type_data("DEFAULT"))
DEFAULT_SCRIPT_TYPE = Type(**types.Script().get_type_data("DEFAULT"))
DEFAULT_FORMAT_TYPE = Type(**types.Format().get_type_data("DEFAULT"))
DEFAULT_GENUS_TYPE = Type(**types.Genus().get_type_data("DEFAULT"))



QUESTION_ITEM = {
    'element_label': 'item',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}




ANSWER_ITEM = {
    'element_label': 'item',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}




ITEM_LEARNING_OBJECTIVES = {
    'element_label': 'learning objectives',
    'instructions': 'accepts an osid.id.Id[] object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': True,
    'default_id_values': [],
    'syntax': 'ID',
    'id_set': [],
}




ASSESSMENT_RUBRIC = {
    'element_label': 'rubric',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

ASSESSMENT_LEVEL = {
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




ASSESSMENT_OFFERED_LEVEL = {
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

ASSESSMENT_OFFERED_START_TIME = {
    'element_label': 'start time',
    'instructions': 'enter a valid datetime object.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_date_time_values': [None],
    'syntax': 'DATETIME',
    'date_time_set': [],
}

ASSESSMENT_OFFERED_GRADE_SYSTEM = {
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

ASSESSMENT_OFFERED_ITEMS_SHUFFLED = {
    'element_label': 'items shuffled',
    'instructions': 'enter either true or false.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'syntax': 'BOOLEAN',
}

ASSESSMENT_OFFERED_SCORE_SYSTEM = {
    'element_label': 'score system',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

ASSESSMENT_OFFERED_DEADLINE = {
    'element_label': 'deadline',
    'instructions': 'enter a valid datetime object.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_date_time_values': [None],
    'syntax': 'DATETIME',
    'date_time_set': [],
}

ASSESSMENT_OFFERED_DURATION = {
    'element_label': 'duration',
    'instructions': 'enter a valid duration object.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_duration_values': [None],
    'syntax': 'DURATION',
    'date_time_set': [],
}

ASSESSMENT_OFFERED_ASSESSMENT = {
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

ASSESSMENT_OFFERED_ITEMS_SEQUENTIAL = {
    'element_label': 'items sequential',
    'instructions': 'enter either true or false.',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'syntax': 'BOOLEAN',
}




ASSESSMENT_TAKEN_ASSESSMENT_OFFERED = {
    'element_label': 'assessment offered',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}

ASSESSMENT_TAKEN_TAKER = {
    'element_label': 'taker',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}




ASSESSMENT_SECTION_ASSESSMENT_TAKEN = {
    'element_label': 'assessment taken',
    'instructions': 'accepts an osid.id.Id object',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_id_values': [''],
    'syntax': 'ID',
    'id_set': [],
}


