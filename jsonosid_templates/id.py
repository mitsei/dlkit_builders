
class Id:

    init = """
    def __init__(self, authority, namespace, identifier):
        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier"""

    get_authority = """
        return self._authority"""

    get_identifier_namespace = """
        return self._namespace"""

    get_identifier = """
        return self._identifier"""


class IdList:

    import_statements = [
        'from dlkit.abstract_osid.osid import errors',
        'from ..primitives import Id',
    ]

    get_next_id = """
        next_item = self.next()
        return next_item

    def next(self):
        return self._get_next_object(Id)"""
