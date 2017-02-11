# resource templates for kit_osid

class ResourceProfile:
    
    init_template = """
    def __init__(self):
        self._provider_manager = None"""

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
        self._${cat_name_under}_view = DEFAULT
        # This is to initialize self._proxy
        osid.OsidSession.__init__(self, proxy)
        self._sub_package_provider_managers = dict()

    # def _get_view(self, view):
    #     \"\"\"Gets the currently set view\"\"\"
    #     if view in self._views:
    #         return self._views[view]
    #     else:
    #         self._views[view] = DEFAULT
    #         return DEFAULT

    def _set_${cat_name_under}_view(self, session):
        \"\"\"Sets the underlying ${cat_name_under} view to match current view\"\"\"
        if self._${cat_name_under}_view == COMPARATIVE:
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError:
                pass
        else:
            try:
                session.use_plenary_${cat_name_under}_view()
            except AttributeError:
                pass

    def _get_provider_session(self, session_name, proxy=None):
        \"\"\"Gets the session for the provider\"\"\"
        agent_key = self._get_agent_key(proxy)
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            session = self._instantiate_session('get_' + session_name, self._proxy)
            self._set_${cat_name_under}_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _get_sub_package_provider_manager(self, sub_package_name):
        if sub_package_name in self._sub_package_provider_managers:
            return self._sub_package_provider_managers[sub_package_name]
        config = self._runtime.get_configuration()
        parameter_id = Id('parameter:{0}ProviderImpl@dlkit_service'.format(sub_package_name))
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            # need to add version argument
            sub_package = self._runtime.get_manager(sub_package_name.upper(), provider_impl)
        else:
            # need to add version argument
            sub_package = self._runtime.get_proxy_manager(sub_package_name.upper(), provider_impl)
        self._sub_package_provider_managers[sub_package_name] = sub_package
        return sub_package

    def _get_sub_package_provider_session(self, sub_package, session_name, proxy=None):
        \"\"\"Gets the session from a sub-package\"\"\"
        agent_key = self._get_agent_key(proxy)
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            manager = self._get_sub_package_provider_manager(sub_package)
            session = self._instantiate_session('get_' + session_name + '_for_bank',
                                                proxy=self._proxy,
                                                manager=manager)
            self._set_bank_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

    def _instantiate_session(self, method_name, proxy=None, *args, **kwargs):
        \"\"\"Instantiates a provider session\"\"\"
        session_class = getattr(self._provider_manager, method_name)
        if proxy is None:
            try:
                return session_class(bank_id=self._catalog_id, *args, **kwargs)
            except AttributeError:
                return session_class(*args, **kwargs)
        else:
            try:
                return session_class(bank_id=self._catalog_id, proxy=proxy, *args, **kwargs)
            except AttributeError:
                return session_class(proxy=proxy, *args, **kwargs)

    def initialize(self, runtime):
        \"\"\"OSID Manager initialize\"\"\"
        from .primitives import Id
        if self._runtime is not None:
            raise IllegalState('Manager has already been initialized')
        self._runtime = runtime
        config = runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name_replaced}ProviderImpl@dlkit_service')
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
        self.close_sessions()"""

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
        session = self._instantiate_session(method_name='${method_name}', proxy=self._proxy, *args, **kwargs)
        return ${cat_name}(
            self._provider_manager,
            session.get_${cat_name_under}(),
            self._runtime,
            self._proxy, ${method_session_name}=session)"""

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
            self._runtime,
            self._proxy,
            ${return_type_under}=session)"""

    get_resource_admin_session_managertemplate = get_resource_lookup_session_managertemplate

    get_resource_admin_session_for_bin_managertemplate = get_resource_lookup_session_for_bin_managertemplate

    get_resource_admin_session_catalogtemplate = get_resource_lookup_session_catalogtemplate

    get_resource_admin_session_for_bin_catalogtemplate = get_resource_lookup_session_for_bin_catalogtemplate

    get_resource_notification_session_managertemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_manager_template
        if self._session_management != DISABLED:
            self._get_provider_session(\'${return_type_under}\', *args, **kwargs)
        return self"""

    get_resource_notification_session_for_bin_managertemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_for_bin_manager_template
        if self._session_management != DISABLED:
            self._get_provider_session(\'${return_type_under}\', *args, **kwargs)
        return self"""

    get_resource_notification_session_catalogtemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_catalog_template
        session = self._instantiate_session(method_name='${method_name}', proxy=self._proxy, *args, **kwargs)
        return ${cat_name}(
            self._provider_manager,
            session.get_${cat_name_under}(),
            self._runtime,
            self._proxy, ${method_session_name}=session)"""

    get_resource_notification_session_for_bin_catalogtemplate = """
        \"\"\"Pass through to provider ${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_notification_session_for_bin_catalog_template
        if self._proxy:
            session = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        else:
            session = self._provider_manager.${method_name}(${args_kwargs_or_nothing})
        return ${cat_name}(
            self._provider_manager,
            self.get_${cat_name_under}(*args, **kwargs),
            self._runtime,
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
        self._provider_session = provider_session"""

    get_bin_id_template = None

    get_bin_template = None

    can_lookup_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    use_comparative_resource_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._object_views['${object_name_under}'] = COMPARATIVE
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.${method_name}()
            except AttributeError:
                pass"""

    use_plenary_resource_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._object_views[\'${object_name_under}\'] = PLENARY
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.${method_name}()
            except AttributeError:
                pass"""

    use_federated_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._${cat_name_under}_view = FEDERATED
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.${method_name}()
            except AttributeError:
                pass"""

    use_isolated_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._${cat_name_under}_view = ISOLATED
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.${method_name}()
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


class ResourceSearchSession:

    get_resource_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceSearchSession.get_resource_search_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_search_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceSearchSession.get_resources_by_search_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_create_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_create_resources
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    can_create_resource_with_record_types_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_form_for_create_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    create_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.create_resource
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    can_update_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_update_resources
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_form_for_update_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def get_${object_name_under}_form(self, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or '${object_name_under}_record_types' in kwargs:
            return self.get_${object_name_under}_form_for_create(*args, **kwargs)
        else:
            return self.${method_name}(*args, **kwargs)

    def duplicate_${object_name_under}(self, ${object_name_under}_id):
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update
        return self._get_provider_session('${interface_name_under}').duplicate_${object_name_under}(${object_name_under}_id)"""

    update_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource
        # Note: The OSID spec does not require returning updated object
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})

    def save_${object_name_under}(self, ${object_name_under}_form, *args, **kwargs):
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource
        if ${object_name_under}_form.is_for_update():
            return self.update_${object_name_under}(${object_name_under}_form, *args, **kwargs)
        else:
            return self.create_${object_name_under}(${object_name_under}_form, *args, **kwargs)"""

    can_delete_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_delete_resources
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    delete_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.delete_resource
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    alias_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.alias_resources
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ResourceNotificationSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_register_for_resource_notifications_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceNotificationSession.can_register_for_resource_notifications
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    reliable_resource_notifications_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    unreliable_resource_notifications_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    acknowledge_resource_notification_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    register_for_new_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    register_for_changed_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    register_for_changed_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    register_for_deleted_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    register_for_deleted_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ResourceBinSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_lookup_resource_bin_mappings_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.can_lookup_resource_bin_mappings
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_ids_by_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_resource_ids_by_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resource_ids_by_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_resource_ids_by_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_resources_by_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_resources_by_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bin_ids_by_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_bin_ids_by_resource
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bins_by_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinSession.get_bins_by_resource
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""


class ResourceBinAssignmentSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

    can_assign_resources_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    can_assign_resources_to_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.can_assign_resources_to_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_assignable_bin_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_assignable_bin_ids_for_resource_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.get_assignable_bin_ids_for_resource
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    assign_resource_to_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.assign_resource_to_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    unassign_resource_from_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.ResourceBinAssignmentSession.unassign_resource_from_bin
        self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""


class ResourceAgentSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session"""

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
        self._provider_session = provider_session"""

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
        self._${cat_name_under}_view = COMPARATIVE
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.use_comparative_${cat_name_under}_view()
            except AttributeError:
                pass"""

    use_plenary_bin_view_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        self._${cat_name_under}_view = PLENARY
        # self._get_provider_session('${interface_name_under}') # To make sure the session is tracked
        for session in self._get_provider_sessions():
            try:
                session.use_plenary_${cat_name_under}_view()
            except AttributeError:
                pass"""

#    use_comparative_bin_view_template = None

#    use_plenary_bin_view_template = None

    get_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bin
        return ${cat_name}(self._provider_manager,
                           self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}),
                           self._runtime,
                           self._proxy)"""

    get_bins_by_ids_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_genus_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_parent_genus_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_parent_genus_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_record_type_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_record_type
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_provider_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_provider
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_template
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._runtime, self._proxy))
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
        return ${cat_name}(self._provider_manager,
                           self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}),
                           self._runtime,
                           self._proxy)"""

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
        return ${cat_name}(self._provider_manager,
                           self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing}),
                           self._runtime,
                           self._proxy)

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

    alias_bin_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.alias_bin
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


class BinQuerySession:

    can_search_bins_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinQuerySession.can_search_bins_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bin_query_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinQuerySession.get_bin_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""

    get_bins_by_query_template = """
        \"\"\"Pass through to provider ${interface_name}.${method_name}\"\"\"
        # Implemented from kitosid template for -
        # osid.resource.BinQuerySession.get_bins_by_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(${args_kwargs_or_nothing})"""



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
    # WILL THIS EVER BE CALLED DIRECTLY - OUTSIDE OF A MANAGER?
    def __init__(self, provider_manager, catalog, runtime, proxy, **kwargs):
        self._provider_manager = provider_manager
        self._catalog = catalog
        self._runtime = runtime
        osid.OsidObject.__init__(self, self._catalog) # This is to initialize self._object
        osid.OsidSession.__init__(self, proxy) # This is to initialize self._proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = AUTOMATIC
        self._${cat_name_under}_view = DEFAULT
        self._object_views = dict()
        self._operable_views = dict()
        self._containable_views = dict()

    def _set_${cat_name_under}_view(self, session):
        \"\"\"Sets the underlying ${cat_name_under} view to match current view\"\"\"
        if self._${cat_name_under}_view == FEDERATED:
            try:
                session.use_federated_${cat_name_under}_view()
            except AttributeError:
                pass
        else:
            try:
                session.use_isolated_${cat_name_under}_view()
            except AttributeError:
                pass

    def _set_object_view(self, session):
        \"\"\"Sets the underlying object views to match current view\"\"\"
        for obj_name in self._object_views:
            if self._object_views[obj_name] == PLENARY:
                try:
                    getattr(session, 'use_plenary_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_comparative_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_operable_view(self, session):
        \"\"\"Sets the underlying operable views to match current view\"\"\"
        for obj_name in self._operable_views:
            if self._operable_views[obj_name] == ACTIVE:
                try:
                    getattr(session, 'use_active_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_any_status_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _set_containable_view(self, session):
        \"\"\"Sets the underlying containable views to match current view\"\"\"
        for obj_name in self._containable_views:
            if self._containable_views[obj_name] == SEQUESTERED:
                try:
                    getattr(session, 'use_sequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass
            else:
                try:
                    getattr(session, 'use_unsequestered_' + obj_name + '_view')()
                except AttributeError:
                    pass

    def _get_provider_session(self, session_name):
        \"\"\"Returns the requested provider session.

        Instantiates a new one if the named session is not already known.

        "\"\"
        agent_key = self._get_agent_key()
        if session_name in self._provider_sessions[agent_key]:
            return self._provider_sessions[agent_key][session_name]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session_name + '_for_${cat_name_under}')
            if self._proxy is None:
                session = session_class(self._catalog.get_id())
            else:
                session = session_class(self._catalog.get_id(), self._proxy)
            self._set_${cat_name_under}_view(session)
            self._set_object_view(session)
            self._set_operable_view(session)
            self._set_containable_view(session)
            if self._session_management != DISABLED:
                self._provider_sessions[agent_key][session_name] = session
            return session

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
        if '_catalog' in self.__dict__:
            try:
                return self._catalog[name]
            except AttributeError:
                pass
        raise AttributeError

    def close_sessions(self):
        \"\"\"Close all sessions currently being managed by this Manager to save memory."\"\"
        if self._session_management != MANDATORY:
            self._provider_sessions = dict()
        else:
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
        self.close_sessions()"""

