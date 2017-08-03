# resource templates for az_osid


class ResourceProfile:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unimplemented"
    ]

    init_template = """
    def __init__(self):
        osid_managers.OsidProfile.__init__(self)

    def _get_hierarchy_session(self, proxy=None):
        if proxy is not None:
            try:
                return self._provider_manager.get_${cat_name_under}_hierarchy_session(proxy)
            except errors.Unimplemented:
                return None
        try:
            return self._provider_manager.get_${cat_name_under}_hierarchy_session()
        except errors.Unimplemented:
            return None
"""

    supports_visible_federation_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}()"""

    supports_resource_lookup_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}()"""

    get_resource_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
        return self._provider_manager.${method_name}()"""


class ResourceManager:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unimplemented"
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_replaced_caps}Profile.__init__(self)

    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager('${pkg_name_replaced_upper}', provider_impl)
        # need to add version argument
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session()
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            hierarchy_session=self._get_hierarchy_session(),
            query_session=query_session)"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session_for_${cat_name_under}(${arg0_name})
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            hierarchy_session=self._get_hierarchy_session(),
            query_session=query_session)"""

    get_resource_admin_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_admin_session_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""

    get_resource_admin_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""

    get_resource_notification_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""

    get_resource_notification_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_for_bin_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, ${arg1_name}),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager)"""


class ResourceProxyManager:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unimplemented"
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_replaced_caps}Profile.__init__(self)

    def initialize(self, runtime):
        osid_managers.OsidProxyManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_proxy_manager('${pkg_name_replaced_upper}', provider_impl)
        # need to add version argument
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session(proxy)
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            proxy=proxy,
            hierarchy_session=self._get_hierarchy_session(proxy),
            query_session=query_session)"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session_for_${cat_name_under}(${arg0_name}, proxy)
            query_session.use_federated_${cat_name_under}_view()
        except Unimplemented:
            query_session = None
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            proxy=proxy,
            hierarchy_session=self._get_hierarchy_session(proxy),
            query_session=query_session)"""

    get_resource_admin_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_admin_session_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager,
            proxy=proxy)"""

    get_resource_admin_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager,
            proxy=proxy)"""

    get_resource_notification_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager,
            proxy=proxy)"""

    get_resource_notification_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_for_bin_template
        return getattr(sessions, '${return_type}')(
            provider_session=self._provider_manager.${method_name}(${arg0_name}, ${arg1_name}, proxy),
            authz_session=self._get_authz_session(),
            override_lookup_session=self._get_override_lookup_session(),
            provider_manager=self._provider_manager,
            proxy=proxy)"""


class ResourceLookupSession:
    import_statements_pattern = [
        "from ..osid.osid_errors import NotFound"
    ]

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name_replaced}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self.use_comparative_${object_name_under}_view()
        self._auth_${cat_name_under}_ids = None
        self._unauth_${cat_name_under}_ids = None
    #     self._overriding_${cat_name_under}_ids = None
    #
    # def _get_overriding_${cat_name_under}_ids(self):
    #     if self._overriding_${cat_name_under}_ids is None:
    #         self._overriding_${cat_name_under}_ids = self._get_overriding_catalog_ids('lookup')
    #     return self._overriding_${cat_name_under}_ids

    def _try_overriding_${cat_name_under_plural}(self, query):
        if self._get_overriding_catalog_ids('lookup') is not None:
            for catalog_id in self._get_overriding_catalog_ids('lookup'):
                query.match_${cat_name_under}_id(catalog_id, match=True)
        return self._query_session.get_${object_name_under_plural}_by_query(query), query

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('lookup', ${cat_name_under}_id):
            return []  # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        results, query = self._try_overriding_${cat_name_under_plural}(query)
        if self._is_isolated_catalog_view():
            if results.available() or self._is_comparative_object_view():
                return results
        if self._is_plenary_object_view():
            return results
        if self._hierarchy_session is None or self._query_session is None:
            return results
        if self._unauth_${cat_name_under}_ids is None:
            self._unauth_${cat_name_under}_ids = self._get_unauth_${cat_name_under}_ids(self._qualifier_id)
        for ${cat_name_under}_id in self._unauth_${cat_name_under}_ids:
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)"""

    get_bin_id_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_bin_id_template
        return self._provider_session.${method_name}()"""

    get_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_bin_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    can_lookup_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return (self._can('${func_name}') or
                bool(self._get_overriding_catalog_ids('${func_name}')))"""

    use_comparative_resource_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_comparative_resource_view_template
        self._use_comparative_object_view()
        self._provider_session.${method_name}()"""

    use_plenary_resource_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_plenary_resource_view_template
        self._use_plenary_object_view()
        self._provider_session.${method_name}()"""

    use_federated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_federated_bin_view_template
        self._use_federated_catalog_view()
        self._provider_session.${method_name}()
        if self._query_session:
            self._query_session.${method_name}()"""

    use_isolated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_isolated_bin_view_template
        self._use_isolated_catalog_view()
        self._provider_session.${method_name}()
        if self._query_session:
            self._query_session.${method_name}()"""

    get_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_id(${arg0_name}, match=True)
        results = self._try_harder(query)
        if results.available():
            return results.next()
        raise NotFound()"""

    get_resources_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        for ${object_name_under}_id in (${arg0_name}):
            query.match_id(${object_name_under}_id, match=True)
        return self._try_harder(query)"""

    get_resources_by_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_genus_type(${arg0_name}, match=True)
        return self._try_harder(query)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_parent_genus_type(${arg0_name}, match=True)
        return self._try_harder(query)"""

    get_resources_by_record_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_record_type(${arg0_name}, match=True)
        return self._try_harder(query)"""

    get_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        if self._can('lookup'):
            return self._provider_session.${method_name}()
        self._check_lookup_conditions()  # raises PermissionDenied
        query = self._query_session.get_${object_name_under}_query()
        query.match_any(match=True)
        return self._try_harder(query)"""


class ResourceQuerySession:
    import_statements_pattern = [
        'from ..utilities import QueryWrapper',
        'from ..osid.osid_errors import Unsupported'
    ]

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name_replaced}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self._unauth_${cat_name_under}_ids = None
        # self._overriding_${cat_name_under}_ids = None

    # def _get_overriding_${cat_name_under}_ids(self):
    #     if self._overriding_${cat_name_under}_ids is None:
    #         self._overriding_${cat_name_under}_ids = self._get_overriding_catalog_ids('search')
    #     return self._overriding_${cat_name_under}_ids

    def _try_overriding_${cat_name_under_plural}(self, query):
        if self._get_overriding_catalog_ids('search') is not None:
            for ${cat_name_under}_id in self._get_overriding_catalog_ids('search'):
                query._provider_query.match_${cat_name_under}_id(${cat_name_under}_id, match=True)
        return self._query_session.get_${object_name_under_plural}_by_query(query), query

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('search', ${cat_name_under}_id):
            return []  # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        results, query = self._try_overriding_${cat_name_under_plural}(query)
        if self._is_isolated_catalog_view():
            if results.available():
                return results
        if self._hierarchy_session is None or self._query_session is None:
            return results
        if self._unauth_${cat_name_under}_ids is None:
            self._unauth_${cat_name_under}_ids = self._get_unauth_${cat_name_under}_ids(self._qualifier_id)
        for ${cat_name_under}_id in self._unauth_${cat_name_under}_ids:
            query._provider_query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)

    class ${object_name}QueryWrapper(QueryWrapper):
        \"\"\"Wrapper for ${object_name}Queries to override match_${cat_name_under}_id method\"\"\"

        def match_${cat_name_under}_id(self, ${cat_name_under}_id, match=True):
            self._cat_id_args_list.append({'${cat_name_under}_id': ${cat_name_under}_id, 'match': match})"""

    can_search_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return (self._can('${func_name}') or
                bool(self._get_overriding_catalog_ids('${func_name}')))"""

    get_resource_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resource_query_template
        if (not self._can('search') and
                self._is_isolated_catalog_view()):
            raise PermissionDenied()
        else:
            return self.${object_name}QueryWrapper(self._provider_session.${method_name}())"""

    get_resources_by_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resources_by_query_template
        if not hasattr(${arg0_name}, '_cat_id_args_list'):
            raise Unsupported('${arg0_name} not from this session')
        for kwargs in ${arg0_name}._cat_id_args_list:
            if self._can('search', kwargs['${cat_name_under}_id']):
                ${arg0_name}._provider_query.match_${cat_name_under}_id(**kwargs)
        if self._can('search'):
            return self._provider_session.${method_name}(${arg0_name})
        self._check_search_conditions()
        result = self._try_harder(${arg0_name})
        ${arg0_name}._provider_query.clear_${cat_name_under}_terms()
        return result"""


class ResourceSearchSession:

    # This still needs to be updated to work with authz overrides:
    get_resource_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.resource.ResourceSearchSession.get_resource_search_template
        if not self._can('search'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    # This still needs to be updated to work with authz overrides:
    get_resources_by_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.resource.ResourceSearchSession.get_resources_by_search_template
        if not self._can('search'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_manager, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name_replaced}.${object_name}'
        self._overriding_${cat_name_under}_ids = None
        if self._proxy is not None:
            try:
                self._object_catalog_session = provider_manager.get_${object_name_under}_${cat_name_under}_session(self._proxy)
            except (Unimplemented, AttributeError):
                pass
        else:
            try:
                self._object_catalog_session = provider_manager.get_${object_name_under}_${cat_name_under}_session()
                self.get_${cat_name_under}_ids_by_${object_name_under} = self._object_catalog_session.get_${cat_name_under}_ids_by_${object_name_under}
            except (Unimplemented, AttributeError):
                pass

    def _get_overriding_${cat_name_under}_ids(self):
        if self._overriding_${cat_name_under}_ids is None:
            self._overriding_${cat_name_under}_ids = self._get_overriding_catalog_ids('lookup')
        return self._overriding_${cat_name_under}_ids

    def _can_for_${object_name_under}(self, func_name, ${object_name_under}_id):
        \"\"\"Checks if agent can perform function for object\"\"\"
        return self._can_for_object(func_name, ${object_name_under}_id, 'get_${cat_name_under}_ids_for_${object_name_under}')"""

    can_create_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resources
        return self._can('${func_name}')"""

    can_create_resource_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types
        # This would like to be a real implementation someday:
        if ${arg0_name} is None:
            raise NullArgument()  # Just 'cause the spec says to :)
        return self._can('${func_name}')"""

    get_resource_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.create_resource
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_update_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_update_resources
        return (self._can('${func_name}') or
                bool(self._get_overriding_catalog_ids('${func_name}')))"""

    get_resource_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        if not self._can_for_${object_name_under}('update', ${object_name_under}_id):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})

    def duplicate_${object_name_under}(self, ${object_name_under}_id):
        if not self._can('update'):
            raise PermissionDenied()
        return self._provider_session.duplicate_${object_name_under}(${arg0_name})"""

    update_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.update_resource
        if not self._can('update'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_delete_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_delete_resources
        return (self._can('${func_name}') or
                bool(self._get_overriding_catalog_ids('${func_name}')))"""

    can_manage_resource_aliases_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_manage_resource_aliases_template
        return (self._can('alias') or
                bool(self._get_overriding_catalog_ids('alias')))"""

    delete_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_resource
        if not self._can_for_${object_name_under}('delete', ${object_name_under}_id):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_manage_resource_aliases_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_manage_resource_aliases
        return (self._can('${func_name}') or
                bool(self._get_overriding_catalog_ids('${func_name}')))"""

    alias_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.alias_resources
        if not self._can_for_${object_name_under}('alias', ${object_name_under}_id):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class ResourceNotificationSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name_replaced}.${object_name}'
"""

    can_register_for_resource_notifications_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.can_register_for_resource_notifications
        return self._can('${func_name}')"""

    reliable_resource_notifications_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_new_resources
        self._provider_session.${method_name}()"""

    unreliable_resource_notifications_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_new_resources
        self._provider_session.${method_name}()"""

    register_for_new_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_new_resources
        if not self._can('register'):
            raise PermissionDenied()
        self._provider_session.${method_name}()"""

    register_for_changed_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_changed_resources
        if not self._can('register'):
            raise PermissionDenied()
        self._provider_session.${method_name}()"""

    register_for_changed_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_changed_resource
        if not self._can('register'):
            raise PermissionDenied()
        self._provider_session.${method_name}(${arg0_name})"""

    register_for_deleted_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_deleted_resources
        if not self._can('register'):
            raise PermissionDenied()
        self._provider_session.${method_name}()"""

    register_for_deleted_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_deleted_resource
        if not self._can('register'):
            raise PermissionDenied()
        self._provider_session.${method_name}(${arg0_name})"""


class ResourceBinSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')  # This could be better
        self._id_namespace = '${pkg_name_replaced}.${object_name}${cat_name}'
"""

    can_lookup_resource_bin_mappings_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.can_lookup_resource_bin_mappings
        return self._can('${func_name}')"""

    get_resource_ids_by_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resource_ids_by_bin
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bin_template
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_ids_by_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resource_ids_by_bins
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bins
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_bin_ids_by_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_bin_ids_by_resource
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_by_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_bins_by_resource
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""


class ResourceBinAssignmentSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')  # This could be better
        self._id_namespace = '${pkg_name_replaced}.${object_name}${cat_name}'
"""

    can_assign_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources
        return self._can('${func_name}')"""

    can_assign_resources_to_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources_to_bin
        return self._can('${func_name}', qualifier_id=${arg0_name})"""

    get_assignable_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_assignable_bin_ids_for_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids_for_resource
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    assign_resource_to_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    unassign_resource_from_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class ResourceAgentSession:

    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_bin_id()
        self._id_namespace = 'resource.ResourceAgent'
"""

    can_lookup_resource_agent_mappings = """
        return self._can('lookup')"""

    get_resource_id_by_agent = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_resource_id_by_agent(agent_id)"""

    get_resource_by_agent = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_resource_by_agent(agent_id)"""

    get_agent_ids_by_resource = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_agent_ids_by_resource(resource_id)"""

    get_agents_by_resource = """
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.get_agents_by_resource(resource_id)"""


class ResourceAgentAssignmentSession:

    init = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        self._qualifier_id = self._provider_session.get_bin_id()
        self._id_namespace = 'resource.ResourceAgent'
"""

    can_assign_agents = """
        return self._can('assign')"""

    can_assign_agents_to_resource = """
        return False  # don't have enough information yet"""

    assign_agent_to_resource = """
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.assign_agent_to_resource(agent_id, resource_id)"""

    unassign_agent_from_resource = """
        if not self._can('assign'):
            raise PermissionDenied()
        return self._provider_session.unassign_agent_from_resource(agent_id, resource_id)"""


class BinLookupSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name_replaced}.${cat_name}'
"""

    use_comparative_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.use_comparative_bin_view_template
        self._provider_session.${method_name}()"""

    use_plenary_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.use_plenary_bin_view_template
        self._provider_session.${method_name}()"""

    get_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bin_template
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_template
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    get_bins_by_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_by_genus_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_lookup_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.can_lookup_bins_template
        return self._can('${func_name}')"""


class BinAdminSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name_replaced}.${cat_name}'
"""

    can_create_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.can_create_bins_template
        return self._can('${func_name}')"""

    can_create_bin_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_create_bin_with_record_types_template
        # This would like to be a real implementation someday:
        if ${arg0_name} is None:
            raise NullArgument()  # Just 'cause the spec says to :)
        return self._can('create')"""

    get_bin_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    create_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.create_bin_template
        if not self._can('create'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_bin_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_update_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_update_bins
        return self._can('${func_name}')"""

    update_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.update_bin_template
        if not self._can('update'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    can_delete_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_delete_bins
        return self._can('${func_name}')"""

    can_manage_bin_aliases_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_manage_bin_aliases_template
        return self._can('alias')"""

    delete_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.delete_bin_template
        if not self._can('delete'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    alias_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.alias_bin_template
        if not self._can('alias'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg_list})"""


class BinHierarchySession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name_replaced}.${cat_name}'
"""

    can_access_bin_hierarchy_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.can_access_bin_hierarchy
        return self._can('${func_name}')"""

    get_bin_hierarchy_id_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy_id
        return self._provider_session.${method_name}()"""

    get_bin_hierarchy_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    get_root_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_root_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    get_root_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_root_bins
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    has_parent_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.has_parent_bins
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    is_parent_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_parent_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_parent_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_parent_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_parent_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_parent_bins
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    is_ancestor_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_ancestor_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    has_child_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.has_child_bins
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    is_child_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_child_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_child_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_child_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    get_child_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy_id
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    is_descendant_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_descendant_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_bin_node_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_node_ids
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(
            ${arg0_name},
            ${arg1_name},
            ${arg2_name},
            ${arg3_name})"""

    get_bin_nodes_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_nodes
        if not self._can('access'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(
            ${arg0_name},
            ${arg1_name},
            ${arg2_name},
            ${arg3_name})"""


class BinHierarchyDesignSession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name_replaced}.${cat_name}'
        # should this be '${pkg_name}.${cat_name}Hierarchy' ?
"""

    can_modify_bin_hierarchy_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchyDesignSession.can_modify_bin_hierarchy
        return self._can('${func_name}')"""

    add_root_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchyDesignSession.add_root_bin_template
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    remove_root_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""

    add_child_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_bins_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""


class BinQuerySession:

    init_template = """
    def __init__(self, *args, **kwargs):
        osid_sessions.OsidSession.__init__(self, *args, **kwargs)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name_replaced}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name_replaced}.${cat_name}'
"""

    can_search_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinQuerySession.can_search_bins_template
        return self._can('${func_name}')"""

    get_bin_query_template = """
        # Implemented from azosid template for -
        # osid.resource.BinQuerySession.get_bin_query_template
        if not self._can('search'):
            raise PermissionDenied()
        return self._provider_session.${method_name}()"""

    get_bins_by_query_template = """
        # Implemented from azosid template for -
        # osid.resource.BinQuerySession.get_bins_by_query_template
        if not self._can('search'):
            raise PermissionDenied()
        return self._provider_session.${method_name}(${arg0_name})"""
