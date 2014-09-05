# -*- coding: utf-8 -*-
from .osid_errors import NotFound
from .settings import LANGUAGETYPE, SCRIPTTYPE, FORMATTYPE

class Language:
        
    def get_type_data(self, name):
        if name == 'DEFAULT':
            return LANGUAGETYPE
        else:
            raise NotFound('DEFAULT Language Type')

class Script:

    def get_type_data(self, name):
        if name == 'DEFAULT':
            return SCRIPTTYPE
        else:
            raise NotFound('DEFAULT Script Type')


class Format:

    def get_type_data(self, name):
        if name == 'DEFAULT':
            return FORMATTYPE
        else:
            raise NotFound('DEFAULT Format Type')

