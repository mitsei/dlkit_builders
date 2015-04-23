from .primitives import Type

AWS_ASSET_CONTENT_RECORD_TYPE = Type(**{
        'authority': 'odl.mit.edu',
        'namespace': 'asset_content_record_type',
        'identifier': 'amazon-web-services'
    })

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

