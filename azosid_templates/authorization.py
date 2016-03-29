class AuthorizationAdminSession:
    get_authorization_form_for_create_for_agent = """
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_authorization_form_for_create_for_agent(agent_id,
                                                                                      function_id,
                                                                                      qualifier_id,
                                                                                      authorization_record_types)"""