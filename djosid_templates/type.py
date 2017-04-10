
class Type:

    init = """
    def __init__(self, authority,
                       namespace,
                       identifier,
                       display_name = '',
                       display_label = '',
                       description = '',
                       domain = ''):

        self._authority = authority
        self._namespace = namespace
        self._identifier = identifier
        self._display_name = display_name
        self._display_label = display_label
        self._description = description
        self._domain = domain
"""

    get_authority = """
        return self._authority"""

    get_identifier_namespace = """
        return self._namespace"""

    get_identifier = """
        return self._identifier"""

    get_description = """
        from ..locale.primitives import DisplayText
        return DisplayText(self._description)"""

    get_display_label = """
        from ..locale.primitives import DisplayText
        return DisplayText(self._display_label)"""

    get_display_name = """
        from ..locale.primitives import DisplayText
        return DisplayText(self._display_name)"""

    get_domain = """
        from ..locale.primitives import DisplayText
        return DisplayText(self._domain)"""
