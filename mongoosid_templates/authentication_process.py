
class Authentication:

    import_statements = [
        'from ..primitives import *',
        'from ..osid.osid_errors import *',
        'from ..authentication.objects import Agent'
    ]

    init = """
    def __init__(self):
        _django_user = None
        _credential = None
"""

    get_agent_id = """
        if self._django_user is not None:
            return Id(identifier = self._django_user.get_username(),
                      namespace = 'osid.agent.Agent',
                      authority = 'MIT-OEIT')
        else:
            return Id(identifier = 'MC3GUE$T@MIT.EDU',
                      namespace = 'osid.agent.Agent',
                      authority = 'MIT-OEIT')"""

    get_agent = """
        raise Unimplemented"""

    is_valid = """
        if self._django_user is not None:
            return self._django_user.is_authenticated()
        else:
            return False"""

    has_expiration = """
        return False"""

    get_expiration = """
        if not self.has_expiration():
            raise IllegalState()
        else:
            raise Unimplemented()"""

    has_credential = """
        if self._credential is None:
            return False
        else:
            return True"""

    get_credential = """
        if self.has_credential():
            return self._credential
        else:
            raise IllegalState()"""

    get_authentication_record = """
        raise Unsupported()

    def set_django_user(self, django_user):
        self._django_user = django_user"""
