class Agent:

    init = """
    _authority = 'Django_user_service'
    _namespace = 'authentication.Agent'

    def __init__(self, user):
        self.my_user = user

    ##
    # Override get_id method to return an id related to Django'
    # native user model
    def get_id(self):
        from django.contrib.auth.models import AnonymousUser
#        identifier = self.my_user.username # Which one should we use?
        identifier = self.my_user.id       # Which one should we use?
        if isinstance(self.my_user, AnonymousUser):
            identifier = long(0)
            try:
                from ..id.primitives import Id
            except:
                from ..osid.common import Id
        return Id(identifier = identifier,
                  namespace = self._namespace,
                  authority = self._authority)

    ##
    # Override get_display_name method to return username
    def get_display_name(self):
        from django.contrib.auth.models import AnonymousUser
        from ..locale.primitives import DisplayText
        if isinstance(self.my_user, AnonymousUser):
            return DisplayText('anonymous_user')
        else:
            return DisplayText(self.my_user.username)

    ##
    # Override get_description method to return something
    def get_description(self):
        from ..locale.primitives import DisplayText
        return DisplayText('the agent Id for ' + self.get_display_name().get_text())"""
