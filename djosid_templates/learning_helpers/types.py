# -*- coding: utf-8 -*-

### THIS STILL NEEDS LOTS OF WORK AND PERSONAL REFLECTION ###
from osid_kit.dj_osid.types import GenusType as OsidGenusType

class GenusType(OsidGenusType):

    resource_types = {
        'TOPIC': 'Topic',
        'LO': 'Learning Outcome'
    }

    def __init__(self):
        super.__init__(self)
        type_set['RT'] = resource_types

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
