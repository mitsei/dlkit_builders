# resource templates for kit_osid

class ResourceProfile:
    
    init_template = """
    def __init__(self):
        self._provider_manager = None
"""

    supports_visible_federation_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""

    supports_resource_lookup_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""

    get_resource_record_types_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""

    supports_resource_record_type_template = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_record_type_template
        return self._provider_manager.${method_name}(${args_kwargs_or_nothing})"""

class ResourceManager:

    init_template = """
    def __init__(self, proxy=None):
        self._runtime = None
        self._provider_manager = None
        self._provider_sessions = dict()
        self._session_management = AUTOMATIC
        self._views = dict()
        osid.OsidSession.__init__(self, proxy) # This is to initialize self._proxy

    def _get_view(self, view):
        \"\"\"Gets the currently set view\"\"\"
        if view in self._views:
            return self._views[view]
        else:
            self._views[view] = DEFAULT
            return DEFAULT

    def _get_provider_session(self, session, proxy=None):
        \"\"\"Gets the session for the provider\"\"\"
        if self._proxy is None:
            self._proxy = proxy
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            session_instance = self._instantiate_session('get_' + session, self._proxy)
            ## DO WE NEED THESE VIEW INITERS???
            if '${cat_name_under}_view' not in self._views:
                self._views['${cat_name_under}_view'] = DEFAULT
            if self._views['${cat_name_under}_view'] == COMPARATIVE:
                try:
                    session_instance.use_comparative_${cat_name_under}_view()
                except AttributeError:
                    pass
            else:
                try:
                    session_instance.use_plenary_${cat_name_under}_view()
                except AttributeError:
                    pass
            if self._session_management != DISABLED:
                self._provider_sessions[session] = session_instance
            return session_instance

    def _instantiate_session(self, method_name, proxy=None, *args, **kwargs):
        \"\"\"Instantiates a provider session\"\"\"
        get_session = getattr(self._provider_manager, method_name)
        if proxy is None:
            return get_session(*args, **kwargs)
        else:
            return get_session(proxy=proxy, *args, **kwargs)

    def initialize(self, runtime):
        \"\"\"OSID Manager initialize\"\"\"
        from .primitives import Id
        if self._runtime is not None:
            raise IllegalState('Manager has already been initialized')
        self._runtime = runtime
        config = runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@dlkit_service')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            self._provider_manager = runtime.get_manager('${pkg_name_upper}', provider_impl)
        else:
            # need to add version argument
            self._provider_manager = runtime.get_proxy_manager('${pkg_name_upper}', provider_impl)

    def close_sessions(self):
        \"\"\"Close all sessions, unless session management is set to MANDATORY\"\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()

    def use_automatic_session_management(self):
        \"\"\"Session state will be saved unless closed by consumers\"\"\"
        self._session_management = AUTOMATIC

    def use_mandatory_session_management(self):
        \"\"\"Session state will be saved and can not be closed by consumers\"\"\"
        self._session_management = MANDATORY

    def disable_session_management(self):
        \"\"\"Session state will never be saved\"\"\"
        self._session_management = DISABLED
        self.close_sessions()
"""

    get_resource_lookup_session_managertemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_manager_template
        if self._session_management != DISABLED:
            self._get_provider_session(\'${return_type_under}\', *args, **kwargs)
        return self"""

    get_resource_lookup_session_for_bin_managertemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_manager_template
        if self._session_management != DISABLED:
            self._get_provider_session(\'${return_type_under}\', *args, **kwargs)
        return self"""

    get_resource_lookup_session_catalogtemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_catalog_template
        session_instance = self._instantiate_session(*args, **kwargs)
        return ${cat_name}(
            self._provider_manager,
            self.get_${cat_name_under}(*args, **kwargs),
            self._proxy, ${return_type_under}=session_instance)"""

    get_resource_lookup_session_for_bin_catalogtemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        if self._proxy:
            session = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        else:
            session = self._provider_manager.${method_name}(${args_kwargs_or_nothing})
        return ${cat_name}(
            self._provider_manager,
            self.get_${cat_name_under}(*args, **kwargs),
            self._proxy,
            ${return_type_under}=session)"""


class ResourceProxyManager:

    get_resource_lookup_session_template = """
        \"\"\"Sends control to Manager\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProxyManager.get_resource_lookup_session_template
        return ${package_name_caps}Manager.${method_name}(${args_kwargs_or_nothing})"""

    get_resource_lookup_session_for_bin_template = """
        \"\"\"Sends control to Manager\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceProxyManager.get_resource_lookup_session_for_bin_template
        return ${package_name_caps}Manager.${method_name}(${args_kwargs_or_nothing})"""
        

class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_bin_id_template = None

    get_bin_template = None

    can_lookup_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    use_comparative_resource_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views['${object_name_under}_view'] = COMPARATIVE
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_comparative_${object_name_under}_view()
            except AttributeError:
                pass"""

    use_plenary_resource_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views[\'${object_name_under}_view\'] = PLENARY
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_plenary_${object_name_under}_view()
            except AttributeError:
                pass"""

    use_federated_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views[\'${cat_name_under}_view\'] = FEDERATED
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_federated_${cat_name_under}_view()
            except AttributeError:
                pass"""

    use_isolated_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views[\'${cat_name_under}_view\'] = ISOLATED
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_isolated_${cat_name_under}_view()
            except AttributeError:
                pass"""

    get_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_parent_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_record_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class ResourceQuerySession:

    can_search_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_query_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.get_item_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_query_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.get_items_by_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_create_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_create_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    can_create_resource_with_record_types_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_form_for_create_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    create_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.create_resource_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_form_for_update_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def get_${object_name_under}_form(self, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or '${object_name_under}_record_types' in kwargs:
            return self.get_${object_name_under}_form_for_create(*args, **kwargs)
        else:
            return self.${method_name}(*args, **kwargs)"""

    update_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        # Note: The OSID spec does not require returning updated object
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def save_${object_name_under}(self, ${object_name_under}_form, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        if ${object_name_under}_form.is_for_update():
            return self.update_${object_name_under}(${object_name_under}_form, *args, **kwargs)
        else:
            return self.create_${object_name_under}(${object_name_under}_form, *args, **kwargs)"""

    delete_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.delete_resource_template
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    alias_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class ResourceAgentSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_resource_id_by_agent = """
        return self._get_provider_session('resource_agent_session').get_resource_id_by_agent(*args, **kwargs)"""

    get_resource_by_agent = """
        return self._get_provider_session('resource_agent_session').get_resource_by_agent(*args, **kwargs)"""

    get_agent_ids_by_resource = """
        return self._get_provider_session('resource_agent_session').get_agent_ids_by_resource(*args, **kwargs)"""

    get_agents_by_resource = """
        return self._get_provider_session('resource_agent_session').get_agents_by_resource(*args, **kwargs)"""


class ResourceAgentAssignmentSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_assign_agents = """
        return self._get_provider_session('resource_agent_assignment_session').can_assign_agents()"""

    can_assign_agents_to_resource = """
        return self._get_provider_session('resource_agent_assignment_session').can_assign_agents_to_resource(*args, **kwargs)"""

    assign_agent_to_resource = """
        return self._get_provider_session('resource_agent_assignment_session').assign_agent_to_resource(*args, **kwargs)"""

    unassign_agent_from_resource = """
        return self._get_provider_session('resource_agent_assignment_session').unassign_agent_from_resource(*args, **kwargs)"""


class BinLookupSession:


    use_comparative_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views[\'${cat_name_under}_view\'] = COMPARATIVE
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_comparative_${cat_name_under}_view()
            except AttributeError:
                pass"""

    use_plenary_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._views[\'${cat_name_under}_view\'] = PLENARY
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_plenary_${cat_name_under}_view()
            except AttributeError:
                pass"""

#    use_comparative_bin_view_template = None

#    use_plenary_bin_view_template = None

    get_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bin
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}), self._proxy)"""

    get_bins_by_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_genus_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_parent_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_parent_genus_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_record_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_record_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_provider_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_provider
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_template
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""


class BinAdminSession:

    get_bin_form_for_create_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    create_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.create_bin
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}), self._proxy)"""

    get_bin_form_for_update_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def get_${cat_name_under}_form(self, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or '${cat_name_under}_record_types' in kwargs:
            return self.get_${cat_name_under}_form_for_create(*args, **kwargs)
        else:
            return self.${method_name}(${args_kwargs_or_nothing})"""

    update_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.update_bin
        # OSID spec does not require returning updated catalog
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}), self._proxy)

    def save_${cat_name_under}(self, ${cat_name_under}_form, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.update_bin
        if ${cat_name_under}_form.is_for_update():
            return self.update_${cat_name_under}(${cat_name_under}_form, *args, **kwargs)
        else:
            return self.create_${cat_name_under}(${cat_name_under}_form, *args, **kwargs)"""

    delete_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.delete_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class BinHierarchySession:

    get_bin_hierarchy_id_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy_id
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bin_hierarchy_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    can_access_bin_hierarchy_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.can_access_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_root_bin_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_root_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_root_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_root_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    has_parent_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.has_parent_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_parent_of_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_parent_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_parent_bin_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_parent_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_parent_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_parent_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_ancestor_of_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_ancestor_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    has_child_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.has_child_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_child_of_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_child_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_child_bin_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_child_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_child_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_child_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    is_descendant_of_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_descendant_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bin_node_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_node_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bin_nodes_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_nodes
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

class BinHierarchyDesignSession:

    can_modify_bin_hierarchy_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.can_modify_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def create_${cat_name_under}_hierarchy(self, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Patched in by cjshaw@mit.edu, Jul 23, 2014, added by birdland to template on Aug 8, 2014
        # Is not part of specs for catalog hierarchy design sessions, but may want to be in hierarchy service instead
        # Will not return an actual object, just JSON
        # since a BankHierarchy does not seem to be an OSID thing.
        return self._get_provider_session('${cat_name_under}_hierarchy_design_session').create_${cat_name_under}_hierarchy(*args, **kwargs)

    def delete_${cat_name_under}_hierarchy(self, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Patched in by cjshaw@mit.edu, Jul 23, 2014, added by birdland to template on Aug 8, 2014
        # Is not part of specs for catalog hierarchy design sessions, but may want to be in hierarchy service instead
        # Will not return an actual object, just JSON
        # since a BankHierarchy does not seem to be an OSID thing.
        return self._get_provider_session('${cat_name_under}_hierarchy_design_session').delete_${cat_name_under}_hierarchy(*args, **kwargs)"""

    add_root_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.add_root_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_root_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_root_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    add_child_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.add_child_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_child_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_child_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    remove_child_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_child_bins
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""



class ResourceList:

    get_next_resource_template = """
        \"\"\"Gets next object\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        else:
            return next_item
            
    def next(self):
        \"\"\"next method for enumerator\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        next_item = osid.OsidList.next(self)
        return next_item"""
            
    get_next_resources_template = """
        \"\"\"gets next n objects from list\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resources
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            i = 0
            while i < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except StopIteration:
                    break
                i += 1
            return next_list"""


class Bin:

    init_template = """
    ##
    # WILL THIS EVER BE CALLED DIRECTLY - OUTSIDE OF A MANAGER?
    def __init__(self, provider_manager, catalog, proxy, **kwargs):
#        if provider_manager:
        self._provider_manager = provider_manager
#        else:
#            import settings
#            import importlib
#            provider_module = importlib.import_module(settings.PROVIDER_MANAGER_MODULE_PATH)
#            provider_manager_class = getattr(provider_module, '${pkg_name_caps}Manager')
#            self._provider_manager = provider_manager_class()
        self._catalog = catalog
        osid.OsidObject.__init__(self, self._catalog) # This is to initialize self._object
        osid.OsidSession.__init__(self, proxy) # This is to initialize self._proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = AUTOMATIC
        osid.OsidObject.__init__(self, catalog) # This is to initialize self._object
        self._views = dict()

    def _get_provider_session(self, session):
        \"\"\"Returns the requested provider session."\"\"
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session + '_for_${cat_name_under}')
            if self._proxy is None:
                session_instance = session_class(self._catalog.get_id())
            else:
                session_instance = session_class(self._catalog.get_id(), self._proxy)
            if '${cat_name_under}_view' in self._views:
                if self._views['${cat_name_under}_view'] == FEDERATED:
                    session_instance.use_federated_${cat_name_under}_view()
                else:
                    session_instance.use_isolated_${cat_name_under}_view()
            if self._session_management != DISABLED:
                self._provider_sessions[session] = session_instance
            return session_instance

    def get_${cat_name_under}_id(self):
        \"\"\"Gets the Id of this ${cat_name_under}."\"\"
        return self._catalog_id

    def get_${cat_name_under}(self):
        \"\"\"Strange little method to assure conformance for inherited Sessions."\"\"
        return self

    def get_objective_hierarchy_id(self):
        \"\"\"WHAT am I doing here?\"\"\"
        return self._catalog_id

    def get_objective_hierarchy(self):
        \"\"\"WHAT am I doing here?\"\"\"
        return self

    def __getattr__(self, name):
        if '_catalog' in self.__dict__ and name in self._catalog:
            return self._catalog[name]
        raise AttributeError

    def close_sessions(self):
        \"\"\"Close all sessions currently being managed by this Manager to save memory."\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()
        raise IllegalState()

    def use_automatic_session_management(self):
        \"\"\"Session state will be saved until closed by consumers."\"\"
        self._session_management = AUTOMATIC

    def use_mandatory_session_management(self):
        \"\"\"Session state will always be saved and can not be closed by consumers."\"\"
        # Session state will be saved and can not be closed by consumers 
        self._session_management = MANDATORY

    def disable_session_management(self):
        \"\"\"Session state will never be saved."\"\"
        self._session_management = DISABLED
        self.close_sessions()
"""

