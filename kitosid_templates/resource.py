# resource templates for kit_osid

class ResourceProfile:

    supports_visible_federation_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_visible_federation
        return self._provider_manager.${method_name}(*args, **kwargs)"""

    supports_resource_lookup_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_lookup
        return self._provider_manager.${method_name}(*args, **kwargs)"""

    get_resource_record_types_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.get_resource_record_types
        return self._provider_manager.${method_name}(*args, **kwargs)"""

    supports_resource_record_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceProfile.supports_resource_record_type_template
        return self._provider_manager.${method_name}(*args, **kwargs)"""

class ResourceManager:

    init_template = """
    DEFAULT = 0
    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1
    AUTOMATIC = 0
    MANDATORY = 1
    DISABLED = -1

    def __init__(self, proxy=None):
        import settings
        import importlib
        provider_module = importlib.import_module(settings.${pkg_name_upper}_PROVIDER_MANAGER_PATH, settings.ANCHOR_PATH)
        if proxy is None:
            provider_manager_class = getattr(provider_module, '${interface_name}')
        else:
            provider_manager_class = getattr(provider_module, '${proxy_interface_name}')
        self._provider_manager = provider_manager_class()
        self._provider_sessions = dict()
        self._session_management = self.AUTOMATIC
        self._proxy = proxy
        self._views = dict()
        self._runtime = None

    def _get_view(self, view):
        if view in self._views:
            return self._views[view]
        else:
            self._views[view] = DEFAULT
            return DEFAULT

    def _get_provider_session(self, session):
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            session_instance = self._instantiate_session('get_' + session, self._proxy)
            ## DO WE NEED THESE VIEW INITERS???
            if '${cat_name_under}_view' not in self._views:
                self._views['${cat_name_under}_view'] = self.DEFAULT
            if self._views['${cat_name_under}_view'] == self.COMPARATIVE:
                try:
                    session_instance.use_comparative_${cat_name_under}_view()
                except AttributeError:
                    pass
            else:
                try:
                    session_instance.use_plenary_${cat_name_under}_view()
                except AttributeError:
                    pass
            if self._session_management != self.DISABLED:
                self._provider_sessions[session] = session_instance
            return session_instance

    def _instantiate_session(self, method_name, proxy=None, *args, **kwargs):
        get_session = getattr(self._provider_manager, method_name)
        if proxy is None:
            return get_session(*args, **kwargs)
        else:
            return get_session(proxy=proxy, *args, **kwargs)

    def initialize(self, runtime):
        from .primitives import Id
        if self._runtime is not None:
            raise IllegalState()
        self._runtime = runtime
        config = runtime.get_configuration()
        parameter_id = Id('parameter:${pkg_name}ProviderImpl@dlkit_service')
        provider_impl = config.get_value_by_parameter(parameter_id).get_string_value()
        if self._proxy is None:
            self._provider_manager = runtime.get_manager('${pkg_name_upper}', provider_impl) # need to add version argument
        else:
            self._provider_manager = runtime.get_proxy_manager('${pkg_name_upper}', provider_impl) # need to add version argument

    def close_sessions(self):
        if self._session_management != self.MANDATORY:
            self._provider_sessions = dict()

    def use_automatic_session_management():
        # Session state will be saved unless closed by consumers
        self._session_management = self.AUTOMATIC

    def use_mandatory_session_management(self):
        # Session state will be saved and can not be closed by consumers 
        self._session_management = self.MANDATORY

    def disable_session_management(self):
        # Session state will never be saved
        self._session_management = self.DISABLED
        self.close_sessions()
"""

    get_resource_lookup_session_managertemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_manager_template
        if self._session_management != self.DISABLED:
            load_it = self._get_provider_session(\'${return_type_under}\')
        return self
        # OLD:
        #if self._proxy:
        #    self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        #else:
        #    self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}(*args, **kwargs)
        #return self"""

    get_resource_lookup_session_for_bin_managertemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_manager_template
        if self._session_management != self.DISABLED:
            load_it = self._get_provider_session(\'${return_type_under}\')
        return self
        # OLD:
        #if self._proxy:
        #    self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        #else:
        #    self._provider_sessions[\'${return_type}\'] = self._provider_manager.${method_name}(*args, **kwargs)
        #return self"""

    get_resource_lookup_session_catalogtemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_catalog_template
        session_instance = self._instantiate_session(*args, **kwargs)
        return ${cat_name}(self._provider_manager, self.get_${cat_name_under}(*args, **kwargs), self._proxy, ${return_type_under} = session_instance)
        # OLD:
        #if self._proxy:
        #    session = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        #else:
        #    session = self._provider_manager.${method_name}(*args, **kwargs)
        #return ${cat_name}(self._provider_manager, self.get_${cat_name_under}(*args, **kwargs), self._proxy, ${return_type_under} = session)"""

    get_resource_lookup_session_for_bin_catalogtemplate = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceManager.get_resource_lookup_session_for_bin_catalog_template
        if self._proxy:
            session = self._provider_manager.${method_name}(proxy=self._proxy, *args, **kwargs)
        else:
            session = self._provider_manager.${method_name}(*args, **kwargs)
        return ${cat_name}(self._provider_manager, self.get_${cat_name_under}(*args, **kwargs), self._proxy, ${return_type_under} = session)"""


class ResourceLookupSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    get_bin_id_template = None

    get_bin_template = None

    can_lookup_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_lookup_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    use_comparative_resource_view_template = """
        self._views['${object_name_under}_view'] = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_comparative_${object_name_under}_view()
            except AttributeError():
                pass"""

    use_plenary_resource_view_template = """
        self._views[\'${object_name_under}_view\'] = self.PLENARY
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_plenary_${object_name_under}_view()
            except AttributeError():
                pass"""

    use_federated_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.FEDERATED
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_federated_${cat_name_under}_view()
            except AttributeError():
                pass"""

    use_isolated_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.ISOLATED
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_isolated_${cat_name_under}_view()
            except AttributeError():
                pass"""

    get_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resource_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_by_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_ids_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_by_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_genus_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_by_parent_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_parent_genus_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_by_record_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_by_record_type_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.get_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

class ResourceQuerySession:

    can_search_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.can_search_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resource_query_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.get_item_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resources_by_query_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceQuerySession.get_items_by_query_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""


class ResourceAdminSession:

    init_template = """
    def __init__(self, provider_session):
        self._provider_session = provider_session
"""

    can_create_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceLookupSession.can_create_resources_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    can_create_resource_with_record_types_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.can_create_resource_with_record_types_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resource_form_for_create_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_create_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    create_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.create_resource_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_resource_form_for_update_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)

    def get_${object_name_under}_form(self, *args, **kwargs):
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.get_resource_form_for_update_template
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or '${object_name_under}_record_types' in kwargs:
            return self.get_${object_name_under}_form_for_create(*args, **kwargs)
        else:
            return self.${method_name}(*args, **kwargs)"""

    update_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        # Note: The OSID spec does not require returning updated object
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)

    def save_${object_name_under}(self, ${object_name_under}_form, *args, **kwargs):
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.update_resource_template
        if ${object_name_under}_form.is_for_update():
            return self.update_${object_name_under}(${object_name_under}_form, *args, **kwargs)
        else:
            return self.create_${object_name_under}(${object_name_under}_form, *args, **kwargs)"""

    delete_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.delete_resource_template
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    alias_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceAdminSession.alias_resources_template
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""


class BinLookupSession:


    use_comparative_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.COMPARATIVE
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_comparative_${cat_name_under}_view()
            except AttributeError():
                pass"""

    use_plenary_bin_view_template = """
        self._views[\'${cat_name_under}_view\'] = self.PLENARY
        for session in self._provider_sessions:
            try:
                self._provider_sessions[session].use_plenary_${cat_name_under}_view()
            except AttributeError():
                pass"""

#    use_comparative_bin_view_template = None

#    use_plenary_bin_view_template = None

    get_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bin
#        from .objects import ${cat_name}
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs), self._proxy)"""

    get_bins_by_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_ids
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_genus_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_parent_genus_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_parent_genus_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_record_type_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_record_type
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_by_provider_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_by_provider
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""

    get_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinLookupSession.get_bins_template
#        from .objects import ${cat_name}, ${cat_name}List
        catalogs = self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        cat_list = []
        for cat in catalogs:
            cat_list.append(${cat_name}(self._provider_manager, cat, self._proxy))
        return ${cat_name}List(cat_list)"""


class BinAdminSession:

    get_bin_form_for_create_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_create
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    create_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.create_bin
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs), self._proxy)"""

    get_bin_form_for_update_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)

    def get_${cat_name_under}_form(self, *args, **kwargs):
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.get_bin_form_for_update_template
        # This method might be a bit sketchy. Time will tell.
        if isinstance(args[-1], list) or '${cat_name_under}_record_types' in kwargs:
            return self.get_${cat_name_under}_form_for_create(*args, **kwargs)
        else:
            return self.${method_name}(*args, **kwargs)"""

    update_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.update_bin
        # OSID spec does not require returning updated catalog
        return ${cat_name}(self._provider_manager, self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs), self._proxy)

    def save_${cat_name_under}(self, ${cat_name_under}_form, *args, **kwargs):
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.update_bin
        if ${cat_name_under}_form.is_for_update():
            return self.update_${cat_name_under}(${cat_name_under}_form, *args, **kwargs)
        else:
            return self.create_${cat_name_under}(${cat_name_under}_form, *args, **kwargs)"""

    delete_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinAdminSession.delete_bin
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

class BinHierarchySession:

    get_bin_hierarchy_id_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy_id
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_bin_hierarchy_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    can_access_bin_hierarchy_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.can_access_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_root_bin_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_root_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_root_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_root_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    has_parent_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.has_parent_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    is_parent_of_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_parent_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_parent_bin_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_parent_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_parent_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_parent_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    is_ancestor_of_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_ancestor_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    has_child_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.has_child_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    is_child_of_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_child_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_child_bin_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_child_bin_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_child_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_child_bins
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    is_descendant_of_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.is_descendant_of_bin
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_bin_node_ids_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_node_ids
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    get_bin_nodes_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchySession.get_bin_nodes
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

class BinHierarchyDesignSession:

    can_modify_bin_hierarchy_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.can_modify_bin_hierarchy
        return self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)
        
    def create_${cat_name_under}_hierarchy(self, *args, **kwargs):
        # Patched in by cjshaw@mit.edu, Jul 23, 2014, added by birdland to template on Aug 8, 2014
        # Is not part of specs for catalog hierarchy design sessions, but may want to be in hierarchy service instead
        # Will not return an actual object, just JSON
        # since a BankHierarchy does not seem to be an OSID thing.
        return self._get_provider_session('${cat_name_under}_hierarchy_design_session').create_${cat_name_under}_hierarchy(*args, **kwargs)

    def delete_${cat_name_under}_hierarchy(self, *args, **kwargs):
        # Patched in by cjshaw@mit.edu, Jul 23, 2014, added by birdland to template on Aug 8, 2014
        # Is not part of specs for catalog hierarchy design sessions, but may want to be in hierarchy service instead
        # Will not return an actual object, just JSON
        # since a BankHierarchy does not seem to be an OSID thing.
        return self._get_provider_session('${cat_name_under}_hierarchy_design_session').delete_${cat_name_under}_hierarchy(*args, **kwargs)"""

    add_root_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.add_root_bin
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    remove_root_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_root_bin
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    add_child_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.add_child_bin
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    remove_child_bin_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_child_bin
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""

    remove_child_bins_template = """
        # Implemented from kitosid template for -
        # osid.resource.BinHierarchyDesignSession.remove_child_bins
        self._get_provider_session('${interface_name_under}').${method_name}(*args, **kwargs)"""



class ResourceList:

    get_next_resource_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        import sys
#        from osid_kit.osid_errors import IllegalState, OperationFailed
        try:
            next_item = self.next()
        except StopIteration:
            raise IllegalState('no more elements available in this list')
        except: #Need to specify exceptions here
            raise OperationFailed()
        else:
            return next_item
            
    def next(self):
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resource
        from .osid import OsidList
        try:
            next_item = OsidList.next(self)
        except:
            raise
        return next_item"""
            
    get_next_resources_template = """
        # Implemented from kitosid template for -
        # osid.resource.ResourceList.get_next_resources
        import sys
#        from osid_kit.osid_errors import IllegalState, OperationFailed
        if ${arg0_name} > self.available():
            # !!! This is not quite as specified (see method docs) !!!
            raise IllegalState('not enough elements available in this list')
        else:
            next_list = []
            x = 0
            while x < ${arg0_name}:
                try:
                    next_list.append(self.next())
                except: #Need to specify exceptions here
                    raise OperationFailed()
                x = x + 1
            return next_list"""


class Bin:

    init_template = """
    DEFAULT = 0
    COMPARATIVE = 0
    PLENARY = 1
    FEDERATED = 0
    ISOLATED = 1
    AUTOMATIC = 0
    MANDATORY = 1
    DISABLED = -1

                        ## THINK. WILL THIS EVER BE CALLED DIRECTLY
                        ## OUTSIDE OF A MANAGER?
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
        self._proxy = proxy
        self._catalog_id = catalog.get_id()
        self._provider_sessions = kwargs
        self._session_management = self.AUTOMATIC
        self._osid_object = self._catalog # This so that the inherited osid 
                                          # methods work.  Don't ask.
        self._views = dict()

    def _get_provider_session(self, session):
        if session in self._provider_sessions:
            return self._provider_sessions[session]
        else:
            session_class = getattr(self._provider_manager, 'get_' + session + '_for_${cat_name_under}')
            if self._proxy is None:
                session_instance = session_class(self._catalog.get_id())
            else:
                session_instance = session_class(self._catalog.get_id(), self._proxy)
            if '${cat_name_under}_view' in self._views:
                if self._views['${cat_name_under}_view'] == self.FEDERATED:
                    session_instance.use_federated_${cat_name_under}_view()
                else:
                    session_instance.use_isoloated_${cat_name_under}_view()
            if self._session_management != self.DISABLED:
                self._provider_sessions[session] = session_instance
            return session_instance

    def get_${cat_name_under}_id(self):
        return self._catalog_id
    
    def get_${cat_name_under}(self):
        return self

    def get_objective_hierarchy_id(self):
        return self._catalog_id
    
    def get_objective_hierarchy(self):
        return self

    def __getattr__(self, name):
        if '_catalog' in self.__dict__ and name in self._catalog:
            return self._catalog[name]
        raise AttributeError

    def close_sessions(self):
        self._provider_sessions = dict()

    def use_automatic_session_management(self):
        # Session state will be saved unless closed by consumers
        self._session_management = self.AUTOMATIC

    def use_mandatory_session_management(self):
        # Session state will be saved and can not be closed by consumers 
        self._session_management = self.MANDATORY

    def disable_session_management(self):
        # Session state will never be saved
        self._session_management = self.DISABLED
        self.close_sessions()
"""

