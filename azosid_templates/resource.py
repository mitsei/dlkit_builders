# resource templates for az_osid

class ResourceProfile:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unsupported"
    ]

    init_template = """
    def __init__(self, interface_name):
        osid_managers.OsidProfile.__init__(self)

    def _get_hierarchy_session(self):
        try:
            return self._provider_manager.get_${cat_name_under}_hierarchy_session(
                Id(authority='${pkg_name_upper}',
                   namespace='CATALOG',
                   identifier='${cat_name_upper}'))
        except Unsupported:
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
        "from ..osid.osid_errors import Unsupported"
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_caps}Profile.__init__(self)

    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager('${pkg_name_upper}', provider_impl) # need to add version argument
"""    

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session()
            query_session.use_federated_${cat_name_under}_view()
        except Unsupported:
            query_session = None
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(),
                self._get_authz_session(),
                hierarchy_session=self._get_hierarchy_session(),
                query_session=query_session)
        except AttributeError:
            raise OperationFailed()"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session_for_${cat_name_under}(${arg0_name})
            query_session.use_federated_${cat_name_under}_view()
        except Unsupported:
            query_session = None
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}),
                self._get_authz_session(),
                hierarchy_session=self._get_hierarchy_session(),
                query_session=query_session)
        except AttributeError:
            raise OperationFailed()"""

    get_resource_admin_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(),
                self._get_authz_session())
        except AttributeError:
            raise OperationFailed()"""

    get_resource_admin_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}),
                self._get_authz_session())
        except AttributeError:
            raise OperationFailed()"""


class ResourceProxyManager:
    import_statements_pattern = [
        "from ..osid.osid_errors import Unsupported"
    ]

    init_template = """
    def __init__(self):
        ${pkg_name_caps}Profile.__init__(self, '${interface_name}')

    def initialize(self, runtime):
        osid_managers.OsidProxyManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_proxy_manager('${pkg_name_upper}', provider_impl) # need to add version argument
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session(proxy)
            query_session.use_federated_${cat_name_under}_view()
        except Unsupported:
            query_session = None
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(proxy),
                self._get_authz_session(),
                proxy,
                hierarchy_session=self._get_hierarchy_session(),
                query_session=query_session)
        except AttributeError:
            raise OperationFailed()"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            query_session = self._provider_manager.get_${object_name_under}_query_session_for_${cat_name_under}(${arg0_name}, proxy)
            query_session.use_federated_${cat_name_under}_view()
        except Unsupported:
            query_session = None
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}, proxy),
                self._get_authz_session(),
                proxy,
                hierarchy_session=self._get_hierarchy_session(),
                query_session=query_session)
        except AttributeError:
            raise OperationFailed()"""

    get_resource_admin_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(proxy),
                self._get_authz_session(),
                proxy)
        except AttributeError:
            raise OperationFailed()"""

    get_resource_admin_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}, proxy),
                self._get_authz_session(),
                proxy)
        except AttributeError:
            raise OperationFailed()"""


class ResourceLookupSession:
    import_statements_pattern = [
        "from ..osid.osid_errors import NotFound"
    ]

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        if 'query_session' in kwargs:
            self._query_session = kwargs['query_session']
        else:
            self._query_session = None
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
        self.use_federated_${cat_name_under}_view()
        self.use_comparative_${object_name_under}_view()

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('lookup', ${cat_name_under}_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list

    def _try_harder(self, query):
        if self._hierarchy_session is None or self._query_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        for ${cat_name_under}_id in self._get_unauth_${cat_name_under}_ids(self._qualifier_id):
            query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._query_session.get_${object_name_under_plural}_by_query(query)
"""

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
        return self._can('${func_name}')"""

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
        self._provider_session.${method_name}()"""

    use_isolated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_isolated_bin_view_template
        self._use_isolated_catalog_view()
        self._provider_session.${method_name}()"""

    get_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            query.match_id(${arg0_name}, match=True)
            results = self._try_harder(query)
            if results.available() > 0:
                return results.next()
            else:
                raise NotFound()"""

    get_resources_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            for ${object_name_under}_id in (${arg0_name}):
                query.match_id(${object_name_under}_id, match=True)
            return self._try_harder(query)"""

    get_resources_by_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            query.match_genus_type(${arg0_name}, match=True)
            return self._try_harder(query)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            query.match_parent_genus_type(${arg0_name}, match=True)
            return self._try_harder(query)"""

    get_resources_by_record_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        if self._can('lookup'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            query.match_record_type(${arg0_name}, match=True)
            return self._try_harder(query)"""

    get_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        if self._can('lookup'):
            return self._provider_session.${method_name}()
        elif self._is_isolated_catalog_view() or self._is_plenary_object_view():
            raise PermissionDenied()
        else:
            query = self._query_session.get_${object_name_under}_query()
            query.match_any(match=True)
            return self._try_harder(query)"""

class ResourceQuerySession:
    import_statements_pattern = [
        'from ..utilities import QueryWrapper',
        'from ..osid.osid_errors import Unsupported'
    ]

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None, **kwargs):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        if 'hierarchy_session' in kwargs:
            self._hierarchy_session = kwargs['hierarchy_session']
        else:
            self._hierarchy_session = None
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
        self.use_federated_${cat_name_under}_view()

    def _get_unauth_${cat_name_under}_ids(self, ${cat_name_under}_id):
        if self._can('search', ${cat_name_under}_id):
            return [] # Don't go further - assumes authorizations inherited
        else:
            unauth_list = [str(${cat_name_under}_id)]
        if self._hierarchy_session.has_child_${cat_name_under_plural}(${cat_name_under}_id):
            for child_${cat_name_under}_id in self._hierarchy_session.get_child_${cat_name_under}_ids(${cat_name_under}_id):
                unauth_list = unauth_list + self._get_unauth_${cat_name_under}_ids(child_${cat_name_under}_id)
        return unauth_list
    
    def _try_harder(self, query):
        if self._hierarchy_session is None:
            # Should probably try to return empty result instead
            # perhaps through a query.match_any(match = None)?
            raise PermissionDenied()
        for ${cat_name_under}_id in self._get_unauth_${cat_name_under}_ids(self._qualifier_id):
            query._provider_query.match_${cat_name_under}_id(${cat_name_under}_id, match=False)
        return self._provider_session.get_${object_name_under_plural}_by_query(query)

    class ${object_name}QueryWrapper(QueryWrapper):
        \"\"\"Wrapper for ${object_name}Queries to override match_${cat_name_under}_id method\"\"\"

        def match_${cat_name_under}_id(self, ${cat_name_under}_id, match=True):
            self.cat_id_args_list.append({'${cat_name_under}_id': ${cat_name_under}_id, 'match': match})
"""

    can_search_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return self._can('${func_name}')"""

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
        if not hasattr(${arg0_name}, 'cat_id_args_list'):
            raise Unsupported('${arg0_name} not from this session')
        for kwargs in ${arg0_name}.cat_id_args_list:
            if self._can('search', kwargs['${cat_name_under}_id']):
                ${arg0_name}._provider_query.match_${cat_name_under}_id(**kwargs)
        if self._can('search'):
            return self._provider_session.${method_name}(${arg0_name})
        elif self._is_isolated_catalog_view():
            raise PermissionDenied()
        else:
            result = self._try_harder(${arg0_name})
            ${arg0_name}._provider_query.clear_${cat_name_under}_terms()
            return result"""


class ResourceSearchSession:

    get_resource_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.resource.ResourceSearchSession.get_resource_search_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    get_resources_by_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from azosid template for -
        # osid.resource.ResourceSearchSession.get_resources_by_search_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    can_create_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resources
        return self._can('${func_name}')"""

    can_create_resource_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types
        # This would like to be a real implementation someday:
        if ${arg0_name} == None:
            raise NullArgument() # Just 'cause the spec says to :)
        else:
            return self._can('${func_name}')"""

    get_resource_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.create_resource
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})

    def duplicate_${object_name_under}(self, ${object_name_under}_id):
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.duplicate_${object_name_under}(${arg0_name})"""

    update_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.update_resource
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_resource
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    alias_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.alias_resources
        if not self._can('alias'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

class ResourceNotificationSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
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
        else:
            self._provider_session.${method_name}()"""

    register_for_changed_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_changed_resources
        if not self._can('register'):
            raise PermissionDenied()
        else:
            self._provider_session.${method_name}()"""

    register_for_changed_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_changed_resource
        if not self._can('register'):
            raise PermissionDenied()
        else:
            self._provider_session.${method_name}(${arg0_name})"""

    register_for_deleted_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_deleted_resources
        if not self._can('register'):
            raise PermissionDenied()
        else:
            self._provider_session.${method_name}()"""

    register_for_deleted_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceNotificationSession.register_for_deleted_resource
        if not self._can('register'):
            raise PermissionDenied()
        else:
            self._provider_session.${method_name}(${arg0_name})"""


class ResourceBinSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40ODL.MIT.EDU') # This needs to be done right
        self._id_namespace = '${pkg_name}.${object_name}${cat_name}'
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
        else:
            return self._provider_session.get_${object_name_under}_ids_by_${cat_name_under}(${cat_name_under}_id)"""

    get_resources_by_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bin_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_${object_name_under}_ids_by_${cat_name_under}(${cat_name_under}_id)"""

    get_resource_ids_by_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resource_ids_by_bins
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_${object_name_under}_ids_by_${cat_name_plural_under}(${cat_name_under}_ids)"""

    get_resources_by_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bins
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_${object_name_plural_under}_ids_by_${cat_name_plural_under}(${cat_name_under}_ids)"""

    get_bin_ids_by_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_bin_ids_by_resource
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_${cat_name_under}_ids_by_${object_name_under}(${object_name_under}_id)"""

    get_bins_by_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinSession.get_bins_by_resource
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_${cat_name_plural_under}_by_${object_name_under}(${object_name_under}_id)"""

class ResourceBinAssignmentSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40ODL.MIT.EDU') # This needs to be done right
        self._id_namespace = '${pkg_name}.${object_name}${cat_name}'
"""

    can_assign_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources
        return self._can('${func_name}')"""

    can_assign_resources_to_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources_to_bin
        return self._can('${func_name}', qualifier_id=bin_id)"""

    get_assignable_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assignable_${cat_name_under}_ids()"""

    get_assignable_bin_ids_for_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids_for_resource
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_assignable_${cat_name_under}_ids_for_${object_name_under}(${object_name_under}_id)"""

    assign_resource_to_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.assign_${object_name_under}_to_${cat_name_under}(${object_name_under}_id, ${cat_name_under}_id)"""

    unassign_resource_from_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.unassign_${object_name_under}_from_${cat_name_under}(${object_name_under}_id, ${cat_name_under}_id)"""


class ResourceAgentSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_bin_id()
        self._id_namespace = 'resource.ResourceAgent'
"""

    can_lookup_resource_agent_mappings = """
        return self._can('lookup')"""

    get_resource_id_by_agent = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_resource_id_by_agent(agent_id)"""

    get_resource_by_agent = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_resource_by_agent(agent_id)"""

    get_agent_ids_by_resource = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_agent_ids_by_resource(resource_id)"""

    get_agents_by_resource = """
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.get_agents_by_resource(resource_id)"""


class ResourceAgentAssignmentSession:

    init = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_bin_id()
        self._id_namespace = 'resource.ResourceAgent'
"""

    can_assign_agents = """
        return self._can('assign')"""

    can_assign_agents_to_resource = """
        return False # don't have enough information yet"""

    assign_agent_to_resource = """
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.assign_agent_to_resource(agent_id, resource_id)"""

    unassign_agent_from_resource = """
        if not self._can('assign'):
            raise PermissionDenied()
        else:
            return self._provider_session.unassign_agent_from_resource(agent_id, resource_id)"""


class BinLookupSession:
    
    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name}.${cat_name}'
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
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.get_bins_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

class BinAdminSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name}.${cat_name}'
"""

    can_create_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinLookupSession.can_create_bins_template
        return self._can('${func_name}')"""

    can_create_bin_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.can_create_bin_with_record_types_template
        # This would like to be a real implementation someday:
        if ${arg0_name} == None:
            raise NullArgument() # Just 'cause the spec says to :)
        else:
            return self._can('admin')"""

    get_bin_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    create_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.create_bin_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_bin_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    update_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.update_bin_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.delete_bin_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    alias_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinAdminSession.alias_bin_template
        if not self._can('alias'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class BinHierarchySession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name}.${cat_name}'
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
        else:
            return self._provider_session.${method_name}()"""

    get_root_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_root_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    get_root_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_root_bins
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    has_parent_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.has_parent_bins
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    is_parent_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_parent_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_parent_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_parent_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_parent_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_parent_bins
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    is_ancestor_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_ancestor_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    has_child_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.has_child_bins
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    is_child_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_child_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_child_bin_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_child_bin_ids
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_child_bins_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy_id
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    is_descendant_of_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.is_descendant_of_bin
        if not self._can('access'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    get_bin_node_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.get_bin_node_ids
        if not self._can('access'):
            raise PermissionDenied()
        else:
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
        else:
            return self._provider_session.${method_name}(
                ${arg0_name},
                ${arg1_name},
                ${arg2_name},
                ${arg3_name})"""


class BinHierarchyDesignSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name}.${cat_name}' # should this be '${pkg_name}.${cat_name}Hierarchy' ?
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
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    remove_root_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    add_child_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_bin_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name}, ${arg1_name})"""

    remove_child_bins_template = """
        if not self._can('modify'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class BinQuerySession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        # This needs to be done right
        # Build from authority in config
        self._qualifier_id = Id('${pkg_name}.${cat_name}%3AROOT%40ODL.MIT.EDU')
        self._id_namespace = '${pkg_name}.${cat_name}'
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
        else:
            return self._provider_session.${method_name}()"""

    get_bins_by_query_template = """
        # Implemented from azosid template for -
        # osid.resource.BinQuerySession.get_bins_by_query_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""