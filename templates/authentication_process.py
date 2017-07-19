
class Authentication:

    import_statements = [
        'from ..primitives import Id',
        'from dlkit.abstract_osid.osid import errors',
        'from ..authentication.objects import Agent'
    ]

    init = """
    def __init__(self):
        self._django_user = None
        self._credential = None
"""

    get_agent_id = """
        if self._django_user is not None:
            return Id(identifier=self._django_user.get_username(),
                      namespace='osid.agent.Agent',
                      authority='MIT-OEIT')
        else:
            return Id(identifier='MC3GUE$T@MIT.EDU',
                      namespace='osid.agent.Agent',
                      authority='MIT-OEIT')"""

    get_agent = """
        raise errors.Unimplemented"""

    is_valid = """
        if self._django_user is not None:
            return self._django_user.is_authenticated()
        else:
            return False"""

    has_expiration = """
        return False"""

    get_expiration = """
        if not self.has_expiration():
            raise errors.IllegalState()
        else:
            raise errors.Unimplemented()"""

    has_credential = """
        if self._credential is None:
            return False
        else:
            return True"""

    get_credential = """
        if self.has_credential():
            return self._credential
        else:
            raise errors.IllegalState()"""

    get_authentication_record = """
        raise errors.Unsupported()

    def set_django_user(self, django_user):
        \"\"\"Special method that excepts a django user. Should be a record.\"\"\"
        self._django_user = django_user"""
