# resource templates for az_osid

class ResourceProfile:

    init_template = """
    def __init__(self, interface_name):
        osid_managers.OsidProfile.__init__(self, '${pkg_name}', interface_name)
"""

    new_idea_for_init_template = """
    def __init__(self, provider_manager, authz_session):
        self._provider_manager = provider_manager
        self._authz_session = authz_session
"""    

    supports_visible_federation_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}()"""

    supports_resource_lookup_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}()"""

#    get_resource_record_types = """
        # Implemented from azosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
#        return self._provider_manager.${method_name}()"""

class ResourceManager:

    init_template = """
    def __init__(self):
        ${pkg_name_caps}Profile.__init__(self, '${interface_name}')

    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager('${pkg_name_upper}', provider_impl) # need to add version argument
"""    

    new_idea_for_init_template = """
    def __init__(self):
        from . import settings
        import importlib
        provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        authz_module = importlib.import_module(settings.AUTHZ_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        provider_manager = getattr(provider_module, '${interface_name}')()
        authz_manager = getattr(authz_module, 'AuthorizationManager')()
        authz_session = authz_manager.get_authorization_session()
        #self._provider_manager = Provider${interface_name}()
        #self._authz_session = authz_manager().get_authorization_session()
        ${pkg_name_caps}Profile.__init__(provider_manager, authz_session)
        self._my_runtime = None

    def initialize(self, runtime):
        osid_managers.OsidManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_manager(
            '${pkg_name_upper}',
            provider_impl) # need to add version argument
"""    

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('${return_type} not implemented in authz_adapter')"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}),
                self._authz_session)
        except AttributeError:
            raise OperationFailed('${return_type} not implemented in authz_adapter')"""


class ResourceProxyManager:

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
    new_idea_for_init_template = """
    def __init__(self):
        from . import settings
        import importlib
        provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        authz_module = importlib.import_module(settings.AUTHZ_MANAGER_MODULE_PATH, settings.ANCHOR_PATH)
        provider_manager = getattr(provider_module, '${interface_name}')()
        authz_manager = getattr(authz_module, 'AuthorizationManager')()
        authz_session = authz_manager.get_authorization_session()
        #self._provider_manager = Provider${interface_name}()
        #self._authz_session = authz_manager().get_authorization_session()
        ${pkg_name_caps}Profile.__init__(provider_manager, authz_session)
        self._my_runtime = None

    def initialize(self, runtime):
        osid_managers.OsidProxyManager.initialize(self, runtime)
        config = self._my_runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@authz_adapter')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        self._provider_manager = runtime.get_proxy_manager(
            '${pkg_name_upper}',
            provider_impl) # need to add version argument
"""

    get_resource_lookup_session_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(proxy),
                self._authz_session,
                proxy)
        except AttributeError:
            raise OperationFailed('${return_type} not implemented in authz_adapter')"""

    get_resource_lookup_session_for_bin_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_template
        try:
            return getattr(sessions, '${return_type}')(
                self._provider_manager.${method_name}(${arg0_name}, proxy),
                self._authz_session,
                proxy)
        except AttributeError:
            raise OperationFailed('${return_type} not implemented in authz_adapter')"""


class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
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
        self._provider_session.${method_name}()"""

    use_plenary_resource_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_plenary_resource_view_template
        self._provider_session.${method_name}()"""

    use_federated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_federated_bin_view_template
        self._provider_session.${method_name}()"""

    use_isolated_bin_view_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.use_isolated_bin_view_template
        self._provider_session.${method_name}()"""

    get_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_ids_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_by_record_type_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        if not self._can('lookup'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

class ResourceQuerySession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    can_search_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return self._can('${func_name}')"""

    get_resource_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resource_query_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}()"""

    get_resources_by_query_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceQuerySession.get_resources_by_query_template
        if not self._can('search'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = provider_session.get_${cat_name_under}_id()
        self._id_namespace = '${pkg_name}.${object_name}'
"""

    can_create_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceLookupSession.can_create_resources_template
        return self._can('${func_name}')"""

    can_create_resource_with_record_types_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types_template
        # This would like to be a real implementation someday:
        if ${arg0_name} == None:
            raise NullArgument() # Just 'cause the spec says to :)
        else:
            return self._can('${func_name}')"""

    get_resource_form_for_create_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    create_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.create_resource_template
        if not self._can('create'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    get_resource_form_for_update_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    update_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        if not self._can('update'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    delete_resource_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.delete_resource_template
        if not self._can('delete'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

    alias_resources_template = """
        # Implemented from azosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        if not self._can('alias'):
            raise PermissionDenied()
        else:
            return self._provider_session.${method_name}(${arg0_name})"""

class BinLookupSession:
    
    init_template = """
    def __init__(self, provider_session, authz_session, proxy=None):
        osid_sessions.OsidSession.__init__(self, provider_session, authz_session, proxy)
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
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
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
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
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
        self._id_namespace = '${pkg_name}.${cat_name}'
"""

    can_access_objective_bank_hierarchy_template = """
        # Implemented from azosid template for -
        # osid.resource.BinHierarchySession.can_access_objective_bank_hierarchy
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
        self._qualifier_id = Id('authorization.Qualifier%3AROOT%40dlkit.mit.edu') # This needs to be done right
        self._id_namespace = '${pkg_name}.${cat_name}'
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

