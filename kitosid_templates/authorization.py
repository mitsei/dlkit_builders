
class AuthorizationSession:

    is_authorized = """
        \"\"\"Pass through to provider AuthorizationSession.is_authorized\"\"\"
        return self._get_provider_session('authorization_session').is_authorized(*args, **kwargs)"""


class AuthorizationAdminSession:

    get_authorization_form_for_create_for_agent = """
        \"\"\"Pass through to provider AuthorizationAdminSession.get_authorization_form_for_create_for_agent\"\"\"
        return self._get_provider_session('authorization_admin_session').get_authorization_form_for_create_for_agent(*args, **kwargs)"""

    get_authorization_form_for_create_for_resource = """
        \"\"\"Pass through to provider AuthorizationAdminSession.get_authorization_form_for_create_for_resource\"\"\"
        return self._get_provider_session('authorization_admin_session').get_authorization_form_for_create_for_resource(*args, **kwargs)"""
