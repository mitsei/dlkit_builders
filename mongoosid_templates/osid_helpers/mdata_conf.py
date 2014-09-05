from .. import types
from ..primitives import Type
default_language_type = Type(**types.Language().get_type_data('DEFAULT'))
default_script_type = Type(**types.Script().get_type_data('DEFAULT'))
default_format_type = Type(**types.Format().get_type_data('DEFAULT'))
default_genus_type = Type(**types.Genus().get_type_data('DEFAULT'))

journal_comment = {
    'element_label': 'Journal Comment',
    'instructions': 'Optional form submission journal comment, 255 character maximum',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_string_values': [{
        'text': '',
        'languageTypeId': str(default_language_type),
        'scriptTypeId': str(default_script_type),
        'formatTypeId': str(default_format_type),
        }],
    'syntax': 'STRING',
    'minimum_string_length': 0, 
    'maximum_string_length': 256, 
    'string_set': []
    }

display_name = {
    'element_label': 'Display Name',
    'instructions': 'Required, 255 character maximum',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_string_values': [{
        'text': '',
        'languageTypeId': str(default_language_type),
        'scriptTypeId': str(default_script_type),
        'formatTypeId': str(default_format_type),
        }],
    'syntax': 'STRING',
    'minimum_string_length': 0, 
    'maximum_string_length': 256, 
    'string_set': []
    }
    
description = {
    'element_label': 'Description',
    'instructions': 'Optional',
    'required': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_string_values': [{
        'text': '',
        'languageTypeId': str(default_language_type),
        'scriptTypeId': str(default_script_type),
        'formatTypeId': str(default_format_type),
        }],
    'syntax': 'STRING',
    'minimum_string_length': 0, 
    'maximum_string_length': 1024, 
    'string_set': []
    }

genus_type = {
    'element_label': 'Genus Type',
    'instructions': 'Required genus Type of type osid.type.Type',
    'required': True,
    'value': False,
    'read_only': False,
    'linked': False,
    'array': False,
    'default_type_values': [str(default_genus_type)],
    'syntax': 'TYPE',
    'type_set': []
    }
