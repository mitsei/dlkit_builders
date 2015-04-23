# -*- coding: utf-8 -*-
from .osid.osid_errors import NotFound

class NoneType:

    none_types = {
        'NONE': 'None',
        'NULL': 'Null',
        }

    def __init__(self):
        self.type_set = {
            'None': self.none_types
            }

    def get_type_data(self, name):
        try:
            return {
                'authority': 'dlkit.mit.edu',
                'namespace': 'NoneType',
                'identifier': name,
                'domain': 'Generic Types',
                'display_name': self.none_types[name] + ' Type',
                'display_label': self.none_types[name],
                'description': ('The ' +  self.none_types[name] + 
                                    ' Type. This type indicates that no type is specified.')
                }
        except IndexError:
            raise NotFound ('NoneType: ' + none)

class Genus:

    generic_types = {
        'DEFAULT': 'Default',
        'UNKNOWN': 'Unkown'
        }

    def __init__(self):
        self.type_set = {
            'Gen': self.generic_types
            }

    def get_type_data(self, name):
        try:
            return {
                'authority': 'dlkit.mit.edu',
                'namespace': 'GenusType',
                'identifier': name,
                'domain': 'Generic Types',
                'display_name': self.generic_types[name] + ' Generic Type',
                'display_label': self.generic_types[name],
                'description': ('The ' +  self.generic_types[name] + 
                                    ' Type. This type has no symantic meaning.')
                }
        except IndexError:
            raise NotFound ('GenusType: ' + none)

class Language:
        
    def get_type_data(self, name):
        if name == 'DEFAULT':
            from .osid.profile import LANGUAGETYPE
            return LANGUAGETYPE
        else:
            raise NotFound('DEFAULT Language Type')

class Script:

    def get_type_data(self, name):
        if name == 'DEFAULT':
            from .osid.profile import SCRIPTTYPE
            return SCRIPTTYPE
        else:
            raise NotFound('DEFAULT Script Type')


class Format:

    def get_type_data(self, name):
        if name == 'DEFAULT':
            from .osid.profile import FORMATTYPE
            return FORMATTYPE
        else:
            raise NotFound('DEFAULT Format Type')

