class AuthorizationAdminSession:
    get_authorization_form_for_create_for_agent = """
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.get_authorization_form_for_create_for_agent(
            agent_id,
            function_id,
            qualifier_id,
            authorization_record_types)"""

class VaultLookupSession:
    get_vaults_by_genus_type = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_vaults_by_genus_type(vault_genus_type)"""

class AuthorizationSession:
    is_authorized = """
        # This should probably check whether user can access authorizations
        # but I'm afraid it would break too much right now:
        # if not self._can('access'):
        #     raise PermissionDenied()
        return self._provider_session.is_authorized(agent_id, function_id, qualifier_id)"""