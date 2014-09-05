# -*- coding: utf-8 -*-

class Generic:

    generic_types = {
        'DEFAULT': 'Default',
        'UNKNOWN': 'Unkown'
        }

    def __init__(self):
        type_set = {
            'GT': generic_types
            }

    def get_type_data(self, name):
        return {
            'authority': 'birdland.mit.edu',
            'namespace': 'Genus Types',
            'identifier': name,
            'domain': 'Generic Types',
            'display_name': self.generic_types[name] + ' Generic Type',
            'display_label': self.generic_types[name],
            'description': ('The ' +  self.generic_types[name] + 
                                ' Type. This type has no symantic meaning.')
            }
