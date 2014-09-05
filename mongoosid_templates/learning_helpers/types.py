# -*- coding: utf-8 -*-

### THIS STILL NEEDS LOTS OF WORK AND PERSONAL REFLECTION ###
#from osid_kit.dj_osid.types import GenusType as OsidGenusType
from ..osid.osid_errors import NotFound

class GenusType(): ## perhaps inherit from the root types?

    resource_types = {
        'TOPIC': 'Topic',
        'LO': 'Learning Outcome'
    }

    def __init__(self):
        super.__init__(self)
        type_set['RT'] = resource_types

    def get_type_data(self, name):
        try:
            return {
                'authority': 'birdland.mit.edu',
                'namespace': 'Genus Types',
                'identifier': name,
                'domain': 'Generic Types',
                'display_name': self.generic_types[name] + ' Genus Type',
                'display_label': self.generic_types[name],
                'description': ('The ' +  self.generic_types[name] + 
                                    ' Genus Type.')
                }
        except IndexError:
            raise NotFound('Genus Type: ' + name)
