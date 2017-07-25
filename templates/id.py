
class Id:

    init = {
        'python': {
            'json': """
    def __init__(self, authority, namespace, identifier):
        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier"""
        }
    }

    get_authority = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return self._authority"""
        }
    }

    get_identifier_namespace = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return self._namespace"""
        }
    }

    get_identifier = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        return self._identifier"""
        }
    }


class IdList:

    import_statements = {
        'python': {
            'json': [
                'from dlkit.abstract_osid.osid import errors',
                'from ..primitives import Id',
            ]
        }
    }

    get_next_id = {
        'python': {
            'json': """
    def ${method_name}(self):
        ${doc_string}
        next_item = next(self)
        return next_item

    def next(self):
        return self._get_next_object(Id)

    __next__ = next"""
        }
    }
