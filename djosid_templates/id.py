
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

