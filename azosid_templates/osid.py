# osid templates for az_osid


class OsidProfile:

    import_statements = [
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'FEDERATED = 0',
        'ISOLATED = 1',
    ]

    init = """
    def __init__(self):
        self._provider_manager = None
        self._my_runtime = None

    def initialize(self, runtime):
        if runtime is None:
            raise NullArgument()
        if self._my_runtime is not None:
            raise IllegalState('this manager has already been initialized.')
        self._my_runtime = runtime

    def _get_authz_manager(self):
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:authzAuthorityImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        return self._my_runtime.get_manager('AUTHORIZATION', provider_impl)  # need to add version argument

    def _get_vault_lookup_session(self):
        return self._get_authz_manager().get_vault_lookup_session()

    def _get_authz_session(self):
        \"\"\"Gets the AuthorizationSession for the default (bootstrap) typed Vault

        Assumes only one vault of this Type, but it can have children depending on underlying impl.

        \"\"\"
        from ..utilities import BOOTSTRAP_VAULT_TYPE
        try:
            vaults = self._get_vault_lookup_session().get_vaults_by_genus_type(BOOTSTRAP_VAULT_TYPE)
        except Unimplemented:
            return self._get_authz_manager().get_authorization_session()
        if vaults.available():
            vault = vaults.next()
            return self._get_authz_manager().get_authorization_session_for_vault(vault.get_id())
        else:
            return self._get_authz_manager().get_authorization_session()

    def _get_override_lookup_session(self):
        \"\"\"Gets the AuthorizationLookupSession for the override typed Vault

        Assumes only one

        \"\"\"
        from ..utilities import OVERRIDE_VAULT_TYPE
        try:
            override_vaults = self._get_vault_lookup_session().get_vaults_by_genus_type(OVERRIDE_VAULT_TYPE)
        except Unimplemented:
            return None
        if override_vaults.available():
            vault = override_vaults.next()
        else:
            return None
        session = self._get_authz_manager().get_authorization_lookup_session_for_vault(vault.get_id())
        session.use_isolated_vault_view()
        return session"""

    get_id = """
        pass"""

    get_display_name = """
        pass"""

    get_description = """
        pass"""

    get_version = """
        pass"""

    get_release_date = """
        pass"""

    supports_osid_version = """
        pass"""

    get_locales = """
        pass"""

    supports_journal_rollback = """
        pass"""

    supports_journal_branching = """
        pass"""

    get_branch_id = """
        pass"""

    get_branch = """
        pass"""

    get_proxy_record_types = """
        pass"""

    supports_proxy_record_type = """
        pass"""


class OsidManager:

    init = """
    def __init__(self):
        OsidProfile.__init__(self)"""

    initialize = """
        OsidProfile.initialize(self, runtime)"""


class OsidProxyManager:

    init = """
    def __init__(self):
        OsidProfile.__init__(self)"""

    initialize = """
        OsidProfile.initialize(self, runtime)"""


class Identifiable:

    get_id = """
        pass"""

    is_current = """
        pass"""


class Extensible:

    has_record_type = """
        pass"""

    get_record_types = """
        pass"""


class Operable:

    is_active = """
        pass"""

    is_enabled = """
        pass"""

    is_disabled = """
        pass"""

    is_operational = """
        pass"""


class OsidSession:
    import_statements = [
        'from ..osid.osid_errors import PermissionDenied',
        'COMPARATIVE = 0',
        'PLENARY = 1',
        'FEDERATED = 0',
        'ISOLATED = 1',
    ]

    init = """
    def __init__(self, provider_session, authz_session, override_lookup_session=None, proxy=None, **kwargs):
        self._provider_session = provider_session
        self._authz_session = authz_session
        self._override_lookup_session = override_lookup_session
        self._proxy = proxy
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None
        self._object_catalog_session = None
        self._id_namespace = None
        self._qualifier_id = None
        self._authz_cache = dict()  # Does this want to be a real cache???
        self._overriding_catalog_ids = None
        self._object_view = COMPARATIVE
        self._catalog_view = FEDERATED

    def _get_function_id(self, func_name):
        return Id(
            identifier=func_name,
            namespace=self._id_namespace,
            authority='ODL.MIT.EDU')

    def _can(self, func_name, qualifier_id=None):
        \"\"\"Tests if the named function is authorized with agent and qualifier.

        Also, caches authz's in a dict.  It is expected that this will not grow to big, as
        there are typically only a small number of qualifier + function combinations to
        store for the agent.  However, if this becomes an issue, we can switch to something
        like cachetools.

        \"\"\"
        function_id = self._get_function_id(func_name)
        if qualifier_id is None:
            qualifier_id = self._qualifier_id
        agent_id = self.get_effective_agent_id()
        try:
            return self._authz_cache[str(agent_id) + str(function_id) + str(qualifier_id)]
        except KeyError:
            authz = self._authz_session.is_authorized(agent_id=agent_id,
                                                      function_id=function_id,
                                                      qualifier_id=qualifier_id)
            self._authz_cache[str(agent_id) + str(function_id) + str(qualifier_id)] = authz
            return authz

    def _can_for_object(self, func_name, object_id, method_name):
        \"\"\"Checks if agent can perform function for object\"\"\"
        can_for_session = self._can(func_name)
        if (can_for_session or
                self._object_catalog_session is None or
                self._override_lookup_session is None):
            return can_for_session

        override_auths = self._override_lookup_session.get_authorizations_for_agent_and_function(
            self.get_effective_agent_id(),
            self._get_function_id(func_name))
        if not override_auths.available():
            return False

        if self._object_catalog_session is not None:
            catalog_ids = list(getattr(self._object_catalog_session, method_name)(object_id))
            for auth in override_auths:
                if auth.get_qualifier_id() in catalog_ids:
                    return True
        return False

    def _get_overriding_catalog_ids(self, func_name):
        if self._overriding_catalog_ids is None and self._override_lookup_session is not None:
            cat_id_list = []
            function_id = Id(
                identifier=func_name,
                namespace=self._id_namespace,
                authority='ODL.MIT.EDU')
            auths = self._override_lookup_session.get_authorizations_for_agent_and_function(
                self.get_effective_agent_id(),
                function_id)
            for auth in auths:
                cat_id_list.append(auth.get_qualifier_id())
            self._overriding_catalog_ids = cat_id_list
        return self._overriding_catalog_ids

    def _check_lookup_conditions(self):
        if ((self._is_plenary_object_view() or self._is_isolated_catalog_view() or self._query_session is None) and
                not self._get_overriding_catalog_ids('lookup')):
            raise PermissionDenied()

    def _check_search_conditions(self):
        if (self._is_federated_catalog_view() and
                self._get_overriding_catalog_ids('search')):
            return
        raise PermissionDenied()

    def _use_comparative_object_view(self):
        self._object_view = COMPARATIVE

    def _use_plenary_object_view(self):
        self._object_view = PLENARY

    def _is_comparative_object_view(self):
        return not bool(self._object_view)

    def _is_plenary_object_view(self):
        return bool(self._object_view)

    def _use_federated_catalog_view(self):
        self._catalog_view = FEDERATED

    def _use_isolated_catalog_view(self):
        self._catalog_view = ISOLATED

    def _is_federated_catalog_view(self):
        return not bool(self._catalog_view)

    def _is_isolated_catalog_view(self):
        return bool(self._catalog_view)
"""

    get_locale = """
        pass"""

    is_authenticated = """
        if self._proxy is None:
            return False
        elif self._proxy.has_authentication():
            return self._proxy.get_authentication().is_valid()
        else:
            return False"""

    get_authenticated_agent_id = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent_id()
        else:
            raise IllegalState()"""

    get_authenticated_agent = """
        if self.is_authenticated():
            return self._proxy.get_authentication().get_agent()
        else:
            raise IllegalState()"""

    get_effective_agent_id = """
        if self.is_authenticated():
            if self._proxy.has_effective_agent():
                return self._proxy.get_effective_agent_id()
            else:
                return self._proxy.get_authentication().get_agent_id()
        else:
            return Id(
                identifier='MC3GUE$T@MIT.EDU',
                namespace='agent.Agent',
                authority='MIT-OEIT')"""

    get_effective_agent = """
        # effective_agent_id = self.get_effective_agent_id()
        # This may want to be extended to get the Agent directly from the Authentication
        # if available and if not effective agent is available in the proxy
        # return Agent(
        #    identifier=effective_agent_id.get_identifier(),
        #    namespace=effective_agent_id.get_namespace(),
        #    authority=effective_agent_id.get_authority())
        raise Unimplemented()"""

    supports_transactions = """
        raise Unimplemented()"""

    startTransaction = """
        raise Unimplemented()"""


class OsidObject:

    get_display_name = """
        pass"""

    get_description = """
        pass"""


class OsidRule:

    has_rule = """
        pass"""

    get_rule_id = """
        pass"""

    get_rule = """
        pass"""


class OsidForm:

    is_for_update = """
        pass"""

    get_default_locale = """
        pass"""

    get_locales = """
        pass"""

    set_locale = """
        pass"""

    get_comment_metadata = """
        pass"""

    set_comment = """
        pass"""

    is_valid = """
        pass"""

    get_validation_messages = """
        pass"""

    get_invalid_metadata = """
        pass"""


class OsidObjectForm:

    get_display_name_metadata = """
        pass"""

    set_display_name = """
        pass"""

    clear_display_name = """
        pass"""

    get_description_metadata = """
        pass"""

    set_description = """
        pass"""

    clear_description = """
        pass"""


class OsidList:

    has_next = """
        pass"""

    available = """
        pass"""


class Metadata:

    get_element_id_template = """
        pass"""

    get_minimum_cardinal_template = """
        pass"""

    supports_coordinate_type_template = """
        pass"""
