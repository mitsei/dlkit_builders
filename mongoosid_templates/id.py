
class Id:
    
    init = """
    def __init__(self, authority, namespace, identifier):
        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier
"""

    get_authority = """
        return self._authority"""

    get_identifier_namespace = """
        return self._namespace"""

    get_identifier = """
        return self._identifier"""

class IdList:

    import_statements = [
    'from ..osid.osid_errors import Unimplemented, OperationFailed, IllegalState',
    'from ..primitives import Id',
    ]

    get_next_id = """
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item

    def next(self):
        try:
            next_item = osid_objects.OsidList.next(self)
        except:
            raise
        if isinstance(next_item, str) or isinstance(next_item, unicode):
            next_item = Id(next_item)
        return next_item"""
